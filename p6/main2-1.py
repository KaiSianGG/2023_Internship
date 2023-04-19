""" 第二版：全部掃描檢查資料是否存在控制字元 """

# 疑點1：& 這個符號不能通過xml，不知系統是不是可以辨識出 &
# 疑點2：\x00是控制字元，即是空字元，可通過xml，這個部分要篩選出來嗎

import re
import csv
import unicodedata
from pymongo import MongoClient
from bson.objectid import ObjectId

# 連結 MongoDB
client = MongoClient("mongodb://localhost:27017")
database = "p6"
collection = "clientcaserecordsocialworker"

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
    value = repr(n) # 轉換成python直譯器看的
    control_c = {}
    replace_str = ""
    global count
    regex_pattern = re.compile(r'\\x[0-9a-zA-Z]{2}')

    # 這些也是經過搜尋和測試得出來要篩選的
    control_chars = ['\\x00', # 空字元
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

    if r'\x' in value:
        # set 特性是不重複，所以套用來移除重複的 \xXX
        code = set(regex_pattern.findall(value))
        # set & set 交集， 判斷是否是控制字元
        control_c = set(code) & set(control_chars)
        if control_c:
            # re.sub用於替换字符串中的匹配项，凡 \xXX 都會被移除
            # replace_str = re.sub(regex_pattern, '', value)

            # 以下兩行能夠完全針對控制字元做出 pattern，re.sub 根據 pattern 移除控制字元
            reg = '|'.join(map(re.escape, list(control_c)))
            replace_str = re.sub(reg, '', value)

            count += 1
            error.append([id, ccn, key, list(control_c), n, value, eval(replace_str), replace_str])


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
d = 0
print("開始搜尋控制字元的資料...")
# 不判斷日期的部分，因爲日期是系統產生的，而且會影響到抓出控制字元
for doc in col.find({}, {"createDate":0, "recordDate":0, "visitDate":0}):
    # print(d)
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
    d+=1

print("共", count, "筆數有問題\n")

""" 輸出 csv 檔案 """
with open(f"./control_character csv/{collection}.csv", "w", encoding="utf-8-sig", newline="") as f:
    header = ['id', 'clientcaseno', 'key', 'control_char', 'original_str', 'repr_str', 'replace_str', 'repr_replace_str']
    writer = csv.writer(f, delimiter=',')  # 逗號分割
    writer.writerow(header)

    for row in error:
        writer.writerow(row)

""" update 每個從 MongoDB 找到錯誤的資料 """
"""modify_count = 0
for row in error:
    # 這個的部分是刪除 row[5] 中的單引號
    # value = str(row[5]).replace('\'', '')

    query = {"_id":ObjectId(row[0])}
    new_value = {"$set":{f"{row[2]}":f"{row[6]}"}}
    result = col.update_one(query, new_value)

    if result.matched_count==1 and result.matched_count == result.modified_count:
        modify_count+=1
        print(row[0], "更新成功")
    else:
        print(row[0], "沒有更新成功")

print("一共更新了", modify_count, "筆")"""