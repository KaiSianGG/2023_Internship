""" 修改欄位名稱 - 目錄處理 非必要 """

# 當程式轉檔CSV無法順利轉檔，只能靠手動另存時
# 手動另存CSV才需要用到
# 欄位名稱 ME_NO,C,8 -> ME_NO

import os
import csv
import pandas as pd
import chardet
import re

root = "CD"
pattern = re.compile(r'\\x00')
folder_list = ["BK208", "BK231", "BK232", "BK236"]

for folder in os.listdir(root): # 根目錄的所有資料夾
    if folder in folder_list:   # 找到指定的資料夾
        folder_path = os.path.join(root, folder)
        for file in os.listdir(folder_path): # 資料夾内的所有檔案
            if file.endswith(".csv"): # 確認是csv檔案
                fpath = os.path.join(folder_path, file)
                print(fpath)

                # 讀取原始檔案內容
                rows = []
                with open(fpath, 'r', encoding='big5', errors='surrogateescape', newline="") as infile: # 原本的檔案是big5的編碼
                    content = infile.readlines()
                    header = content[0] # 取得表頭

                    for idx, value in enumerate(content):
                        if idx == 0: # index 0 為表頭，跳過
                            continue
                        value = repr(value)
                        if r'\x00' in value:
                            replace_value = re.sub(pattern, "", value)
                            rows.append(eval(replace_value).replace('\r\n','').split(','))
                        else: 
                            rows.append(eval(value).replace('\r\n','').split(','))

                # 修改表頭
                new_header = header.replace('\",\"', "|").replace('\"', "").split("|")
                new_header = [i.split(',')[0] for i in new_header]
                infile.close()

                # 將修改後的內容寫入新檔案
                with open(fpath, 'w', encoding='utf-8-sig', errors='surrogateescape', newline="") as outfile: # 輸出檔案選擇使用utf-8-sig
                    writer = csv.writer(outfile)
                    writer.writerow(new_header)
                    writer.writerows(rows)  # 寫入除了表頭以外的內容
                outfile.close()
                new_header = []