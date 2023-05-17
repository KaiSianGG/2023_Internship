""" 非輸入模式查詢 """

# 遇到的問題：
# 1. 編碼問題，這裏直接忽略無法正常編碼的字元
# 2. 控制字元問題，這裏先以二進制方式讀取内容后將\x00移除，再轉變成字串繼續處理

import os
import csv

root_dir = 'CD'
target_data = []
column = "ME_NO"
memberId = ["N0520064", "X0585070", "X1101825"]

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # rb 二進制形式讀取檔案
        with open (file_path, "rb") as f:
            content = f.read() # 讀取所有内容
            content = content.replace(b'\x00', b'')  # 刪除NUL字元
            content = content.decode("utf-8-sig", errors="ignore") # 將 byte 轉變陳 str
            c_reader = csv.DictReader(content.splitlines())
            # list = [r for r in c_reader if r[column] == memberId]

            for index, r in enumerate(c_reader):
                try:
                    # print(index, r)
                    if r[column] in memberId:
                        target_data.append({"ME_NO": r[column], "location": os.path.relpath(file_path, root_dir), "index": index+1})
                except:
                    continue
                
print("找到", len(target_data), "筆")
count = 0
for data in target_data:
    count+=1
    file = open(os.path.join(root_dir, data["location"]), "r", errors="ignore")
    reader = csv.DictReader(file, delimiter=",")
    # 委員號、目錄、引數
    print(f"{count}. 委員號：{data['ME_NO']}, 位置：{data['location']}, idx：{data['index']}")
    for index, row in enumerate(reader):
        if index == data["index"]-1:
            print(row)
            break
