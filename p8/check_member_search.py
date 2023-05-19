""" 輸入模式查詢 版本1 """

# 遇到的問題：
# 1. 編碼問題，這裏直接忽略無法正常編碼的字元
# 2. 控制字元問題，這裏先以二進制方式讀取内容后將\x00移除，再轉變成字串繼續處理

import os
import csv

Id = ["N0520064", "X0585070", "X1101825"]

def check_member(root_dir, memberId):
    count = 0
    column = "ME_NO"
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder) # 每個 CD 文件夾
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file) # 文件夾中的每個檔案

            # rb 二進制形式讀取檔案
            with open (file_path, "rb") as f:
                try:
                    content = f.read() # 讀取所有内容
                    content = content.replace(b'\x00', b'')  # 刪除NUL字元
                    content = content.decode("utf-8-sig", errors="ignore") # 將 byte 轉變陳 str
                    c_reader = csv.DictReader(content.splitlines())
                    # list = [r for r in c_reader if r[column] == memberId]

                    for index, r in enumerate(c_reader):
                        try:
                            # print(index, r)
                            if r[column] == memberId:
                                count+=1
                                print(f"{count}. ME_NO: {r[column]}, location: {os.path.relpath(file_path, root_dir)}, index: {index+2}")
                        except:
                            continue
                except PermissionError:
                    print(file_path, "失敗")
                    pass
    if count == 0:
        print("⚠ 沒有找到該委員號的任何資料!")


root_dir = './CD'
print(f"csv檔案根目錄為: {root_dir}")
while True:
    memberId = input("--------------------------------\n請輸入查詢記錄的委員號: ")
    if memberId == "q":
        print("⚠ 停止查詢...")
        break
    check_member(root_dir, memberId)

