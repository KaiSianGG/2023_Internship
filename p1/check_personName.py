########################### 2.檢查資料庫原本的名字和李育師伯給的名字匹配有沒有相同，沒有的則輸出成新的csv檔案 ###########################

import csv
import pandas as pd

header = ["_id", "old_name", "memberNo", "cicheng", "new_name"]

df = pd.read_csv("C:/Users/User/Downloads/persons.csv", names=header)

print(df)
# for index, row in df.iterrows():
#         print(row['old_name'], row['new_name']) 

count = 0
with open("楷軒new.csv", "w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()

    # df.iterrows() 遍历DataFrame的每一行
    for index, row in df.iterrows():
        if (row['old_name'] != row['new_name']):
            count += 1
            writer.writerow({"_id": row["_id"], "old_name": row["old_name"],
                            "memberNo": row["memberNo"], "cicheng": row["cicheng"], "new_name": row["new_name"]})
print(count)

