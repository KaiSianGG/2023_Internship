""" 修改欄位名稱 - 單一檔案處理 非必要 """

# 當程式轉檔CSV無法順利轉檔，只能靠手動另存時
# 手動另存CSV才需要用到
# 欄位名稱 ME_NO,C,8 -> ME_NO

import csv
import re
import os

path = 'BK246_A89_tzcol_COLU_L.csv'
pattern = re.compile(r'\\x00')

print(path, "處理中...")
# 讀取原始檔案內容
rows = []
with open(path, 'r', encoding='big5', errors='ignore', newline="") as infile:
    content = infile.readlines()
    header = content[0] # 取得表頭
    # print(type(content))
    # target = content[26454]
    # infile.close()

    for idx, value in enumerate(content):
        if idx == 0: # index 0 為表頭，這裏跳過
            continue
        value = repr(value)
        if r'\x00' in value:
            replace_value = re.sub(pattern, "", value)
            rows.append(eval(replace_value).replace('\r\n','').split(','))
        else: 
            rows.append(eval(value).replace('\r\n','').split(','))
# print(repr(target))
# if r'\x00' in repr(target):
#     replace_value = re.sub(pattern, "", repr(target))
#     print(replace_value)

# 修改表頭
new_header = header.replace('\",\"', "|").replace('\"', "").split("|")
new_header = [i.split(',')[0] for i in new_header]
infile.close()

# 將修改後的內容寫入新檔案
with open(path, 'w', encoding='big5', errors='surrogateescape', newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(new_header)
    writer.writerows(rows)  # 寫入除了表頭以外的內容
outfile.close()
new_header = []

print("處理完成")