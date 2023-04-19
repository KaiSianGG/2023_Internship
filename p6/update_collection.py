""" 在這之前先要執行main2-1.py 或 main2-2.py 產出 csv 檔案 """
""" update 每個從 MongoDB 找到錯誤的資料 """

import csv
import bson.objectid
from bson.objectid import ObjectId
from pymongo import MongoClient

# 連結 MongoDB
client = MongoClient("mongodb://localhost:27017")
database = "p6"
collection = "visitrecordsocialworkercomment"
file_path = f"./control_character csv/{collection}.csv"

# 測試連結結果
db_list = client.list_database_names()
if database in db_list:
    db = client[database]
    col_names = db.list_collection_names()
    if collection in col_names:
        col = db[collection]
        print("connection successful")
    else: 
        print("Collection does not exist")
        exit()
else:
    print("Database does not exist")
    exit()

modify_count = 0

with open(file_path, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    next(reader) # 跳過第一列（表頭）

    for row in reader:
        if not bson.ObjectId.is_valid(row[0]):
            print(row[0], "不符合ObjectId的格式")
            continue
        
        query = {"_id":ObjectId(row[0])} # 根據指定的 id 去做篩選
        new_value = {"$set":{row[2]:row[6]}} # 修改 key 的值變成移除控制字元的值
        result = col.update_one(query, new_value)

        # 找到該筆資料，並且也有修改
        if result.matched_count==1 and result.matched_count == result.modified_count:
            modify_count+=1
            print(row[0], "更新成功")
        else:
            print(row[0], "沒有更新成功")

    print("一共更新了", modify_count, "筆")