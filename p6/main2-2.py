""" 第二版之二：全部掃描檢查是否有問題, 使用 unicodedata 判斷控制字元 """

import re
import csv
import unicodedata
from pymongo import MongoClient
from bson.objectid import ObjectId

# 連結 MongoDB
client = MongoClient("mongodb://localhost:27017")
database = "p6"
collection = "visitrecordvolunteer"

# 測試連結結果
db_list = client.list_database_names()
if database in db_list:
    db = client[database]
    col_names = db.list_collection_names()
    if collection in col_names:
        col = db[collection]
        print("連接成功")
    else:
        print("Collection does not exist")
        exit()
else:
    print("Database does not exist")
    exit()

error = []
count = 0

# 找出控制字元的資料，並移除控制字元
def check_control_char(id, ccn, key, n):
    control_c = set()
    replace_str = ""
    global count
    # 可通過 xml 的控制字元
    # good_char = ["\\x7f", "\\xa0", "\\x8f", "\\xad", "\\x00"]

    # 這些也是經過搜尋和測試得出來要篩選的
    control_c = [  # '\\x00', # 空字元
        '\\x01',
        '\\x02',
        '\\x03',
        '\\x04',
        '\\x05',
        '\\x06',
        '\\x07',
        '\\x08',
        #  '\\x09', # \t
        #  '\\x0a', # \n
        '\\x0b',
        '\\x0c',
        #  '\\x0d', # \r
        '\\x0e',
        '\\x0f',
        '\\x10',
        '\\x11',
        '\\x12',
        '\\x13',
        '\\x14',
        '\\x15',
        '\\x16',
        '\\x17',
        '\\x18',
        '\\x19',
        '\\x1a',
        '\\x1b',
        '\\x1c',
        '\\x1d',
        '\\x1e',
        '\\x1f',
        #  '\\x7f', # DEL
        #  '\\xa0', # 非斷開空白符號
        #  '\\xad', # 軟連接符號
        #  '\\x8f'  # 應用程式命令符號
        '\\x8d',
        '\\x90'
    ]

    # 歷遍字串中的所有字元
    # 這個 value 是用來檢查控制字元用的, value 會移除資料中的\r\t\n
    value = ''.join([c for c in n if c not in ['\r', '\t', '\n']])
    # repr會產生單引號，要移除單引號，不然會影響後續設計 pattern 造成沒辦法移除控制字元
    control_c = {repr(c).replace('\'', '') for c in value if unicodedata.category(c) == 'Cc' and (r'\x' + hex(ord(c))[2:].zfill(2) in control_c)}

    # print(control_c)
    if control_c:
        # re.sub用於替换字符串中的匹配项，凡 \xXX 都會被移除
        # replace_str = re.sub(regex_pattern, '', value)

        # 以下兩行能夠完全針對控制字元做出 pattern，re.sub 根據 pattern 移除控制字元
        reg = '|'.join(map(re.escape, list(control_c)))
        replace_str = re.sub(reg, '', repr(n))
        count += 1
        error.append([id, ccn, key, list(control_c), n, repr(n), eval(replace_str), replace_str])


# 如果是 list ，判斷 list 裏面的字串，有可能會有dict，但是目前沒有list中list
def is_list(id, ccn, key, arr):
    for index, i in enumerate(arr):
        if isinstance(i, str) and r'\x' in repr(i):
            check_control_char(id, ccn, f"{key}.{index}", i)

        if isinstance(i, dict):
            is_dict(id, ccn, f"{key}.{index}", i)

        if isinstance(i, list):
            is_list(id, ccn, f"{key}.{index}", i)


# 如果是 dict, value 有可能是字串、object、list
def is_dict(id, ccn, key, obj):
    for field, value in obj.items():
        if isinstance(value, str) and r'\x' in repr(value):
            check_control_char(id, ccn, f"{key}.{field}", value)

        if isinstance(value, dict):
            is_dict(id, ccn, f"{key}.{field}", value)

        if isinstance(value, list):
            is_list(id, ccn, f"{key}.{field}", value)


""" 程式開始 """
print("開始搜尋控制字元的資料...")
for doc in col.find({}, {"recordDate": 0, "createDate": 0, 'visitDate': 0}):
    id = doc["_id"]
    ccn = doc["clientCaseNo"]

    # document 中第一層判斷
    for key, value in doc.items():
        if key == "_id" or key == "clientCaseNo":
            continue
        # 如果是 string
        elif isinstance(value, str) and r"\x" in repr(value):
            check_control_char(id, ccn, key, value)
        # 如果是 list
        elif isinstance(value, list):
            is_list(id, ccn, key, value)
        # 如果是 dict
        elif isinstance(value, dict):
            is_dict(id, ccn, key, value)

print("共", count, "筆數有問題\n")

""" 輸出 csv 檔案 """
with open(f"main2-2_{collection}.csv", "w", encoding="utf-8-sig", newline="") as f:
    header = ['id', 'clientcaseno', 'key', 'control_char', 'original_str', 'repr_str', 'replace_str', 'repr_replace_str']
    writer = csv.writer(f, delimiter=',')  # 逗號分割
    writer.writerow(header)

    for row in error:
        writer.writerow(row)
