########################### 1.將person資料表的personName拆分成姓名、委員號、慈誠號，輸出一個csv檔案 ###########################

import csv
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['person']
db_collection = db['persons']

all_data = db_collection.find()

'''for i in all_data:
  name = i['personName']
  if name.find("_") != -1:
      # words = name.replace("_", " ")
      word = name.split("_")
      print(word)
  else:
      print(name)'''

with open("黃楷軒.csv", "w", newline="", encoding="utf-8-sig") as csv_file:
    fieldName = ["_id", "name", "member_no", "cicheng"]
    # 將dictionary寫入csv
    writer = csv.DictWriter(csv_file, fieldnames=fieldName)
    # 寫入欄位名稱
    writer.writeheader()

    for data in all_data:  # 50445 次
        id = data["_id"]
        name = data["personName"]

        # 篩選有底綫的name
        # 沒找到的話會返回-1
        if name.find("_") != -1:
            name_arr = name.split("_")  # 分割底綫的部分，變成一個list
            # list 裏有三個值，代表有姓名、委員號、慈誠號
            if len(name_arr) == 3:
                writer.writerow(
                    {"_id": data["_id"], "name": name_arr[0], "member_no": name_arr[1], "cicheng": name_arr[2]}
                )
        else:
            continue
