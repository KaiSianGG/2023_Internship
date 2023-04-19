########################### 3.根據手動篩選的資料更新資料表内的資料 ###########################

import pymongo
from bson.objectid import ObjectId
import csv
import unicodedata

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['person_diff']
collection = db['persons']

count = 0
with open ("./project1/楷軒new_deleteSpace.csv", "r", encoding="utf-8-sig") as csvf:
    reader = csv.DictReader(csvf)

    for row in reader:
        count+=1
        id = row["_id"]

        # 修改新的名詞串接委員號與慈誠號
        new_name = f"{row['new_name']}_{row['memberNo']}_{row['cicheng']}"
        print(new_name, end=" ")

        query = {"_id":ObjectId(id)} # 針對csv檔案中要修改的人的id
        update = {"$set":{"personName":new_name}} # 修改名字
        result = collection.update_one(query, update)

        print("match counted: ", result.matched_count, end=" ")
        print("match modified:", result.modified_count)
print(f"一共有 {count} 更新筆數")

# 檢查資料庫 personName 是否存在無法正常編碼
total = 0 

print("\n檢查還有造字的筆數：")
all_data = collection.find()
for data in all_data:
    name = data["personName"]
    id = data["_id"]
    for char in name:
        try:
            char_name = unicodedata.name(char)
        except ValueError:
            total+=1
            print(f"_id: {id}, name: {name}")

print(f"一共還有 {total} 造字")

