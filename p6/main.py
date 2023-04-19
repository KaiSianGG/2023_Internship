""" 第一版：針對 clientName, summary, description 檢查資料是否存在控制字元 """

from pymongo import MongoClient
import re
import csv
import unicodedata

# 連結 MongoDB
client = MongoClient("mongodb://localhost:27017")
database = client["clientcaserecord"]
collection = database["socialworker"]
# 測試連結結果
try:
    database.command("serverStatus")
except Exception as e:
    print(e)
else:
    print("You are connected!")

array = []
count = 0
# \xXX 為 ASCII 控制字元的跳脫字元
regex_pattern = re.compile(r'\\x[0-9a-zA-Z]{2}')

# 造字區 [\uE000-\uF8FF]
# XML 无法识别的 ASCII 控制字符的列表, 沒有tab、換行、ENTER
# 資料中有 \xa0、\xad、\x8f 沒影響
control_chars = ['\\x00',
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
                 '\\x1f'
                 #  '\\x7f', # DEL
                 #  '\\xa0', # 非斷開空白符號
                 #  '\\xad', # 軟連接符號
                 #  '\\x8f'  # 應用程式命令符號
                 ]

for doc in collection.find({}, {'_id':1, 'clientName':1, 'summary':1, 'description':1}):
    id = doc["_id"]
    clientcaseno = doc["clientCaseNo"]
    for key in doc.keys():
        value = repr(doc[key])  # 資料字串
        if r'\x' in value:
            # set 的 key 為不重複，所以套用來移除重複的 \xXX
            code = list(set(regex_pattern.findall(value)))
            # set & set 交集， 判斷是否是控制字元
            control_c = set(code) & set(control_chars)
            if control_c:
                # replace_str = re.sub(regex_pattern, '', value) # re.sub用于替换字符串中的匹配项，替換掉 \xXX 為空
                reg = '|'.join(map(re.escape, list(control_c))) # 這行能夠完全針對控制字元做出 pattern
                # re.sub用于替换字符串中的匹配项，替換掉 \xXX 為空
                replace_str = re.sub(reg, '', value)
                count += 1
                array.append([id, clientcaseno, key, list(control_c), repr(doc[key]), replace_str])

print("共", count, "有問題")

with open("result2.csv", "w", encoding="utf-8-sig", newline="") as f:
    header = ['id', 'clientcaseno', 'field', 'control_char', 'original_str', 'replace_str']
    writer = csv.writer(f, delimiter=',')  # 逗號分割
    writer.writerow(header)

    for row in array:
        writer.writerow(row)

