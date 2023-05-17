""" DBF轉檔csv 版本1 """
# 無法順利轉檔會列出失敗的DBF，需要自行手動另存

from dbfread import DBF
import os 
import csv

# 第二層或更多判斷
def is_file(path, name):
    # 確定是DBF檔案
    if path.endswith('.DBF'):
        # 寫入CD文件夾, CD/BK220/...
        filename = target_dir + "/" + name + ".csv" # CD/BK220/D84_TZ_AREA.csv
        print(path, "->", filename, end=" ")

        # 讀取DBF檔案
        table = DBF(path, encoding='big5', char_decode_errors='surrogateescape', ignore_missing_memofile=True)

        # 寫入CSV檔案
        with open(filename, 'w', encoding='big5', newline='', errors="surrogateescape") as f:
            try:
                writer = csv.writer(f)
                writer.writerow(table.field_names) # 寫入表頭
                for idx, record in enumerate(table):
                    writer.writerow(list(record.values()))
                print("✔")
            except:
                error_file.append(path)
                error_destination.append(filename)
                print("❌")
        f.close()

# 第二層或更多判斷
def is_dir(path, name):
    for f in os.listdir(path):
        fpath = os.path.join(path, f) # CD_0511/BK220/D84/TZ        CD_0511/BK220/D84/TZ/AREA.DBF

        if os.path.isfile(fpath):
            cname = name + "_" + f.split('.')[0] #                   BK220/D84_TZ_AREA
            # fpath 是資料路徑， name是要變成csv的路徑
            is_file(fpath, cname)
            cname = name

        if os.path.isdir(fpath):
            foldername = os.path.basename(fpath)
            name = name + "_" + foldername # BK220/D84_TZ
            is_dir(fpath, name) # fpath = CD_0511/BK220/D84/TZ

# 第一層判斷
def f_list(path):
    # 取得CD名, BK220
    base_cd_name = os.path.basename(path)
    # CD底下的文件夾和檔案
    for f in os.listdir(path):
        fpath = os.path.join(path, f) # CD_0511/BK220/D84

        # 如果是檔案
        if os.path.isfile(fpath):
            name = base_cd_name + "/" + f.split('.')[0]
            # fpath 是資料路徑， name是要變成csv的路徑
            is_file(fpath, name)

        # 如果是文件夾
        if os.path.isdir(fpath):
            name = base_cd_name + "/" + f  # BK220/D84
            is_dir(fpath, name) # fpath = CD_0511/BK220/D84

""" 程式開始 """
root = 'CD_0511'
target_dir = 'CD'
error_file = []
error_destination = []

for cd in os.listdir(root):
    if not os.path.exists(os.path.join(target_dir, cd)):
        os.mkdir(os.path.join(target_dir, cd))

    path = os.path.join(root, cd) # data source
    # print("現在處理 ", path)
    f_list(path)

print("共", len(error_file), "沒辦法順利轉換csv\n\n")
print("來源\n", error_file, "\n\n")
print("來源\n", error_destination, "\n\n")














# table = DBF('CD_0511/BK202/COL/A79COL.DBF', encoding='big5', char_decode_errors='surrogateescape', ignore_missing_memofile=True)
# with open('test.csv', 'w', encoding='big5', newline='', errors="surrogateescape") as f:
#     writer = csv.writer(f)
#     writer.writerow(table.field_names)
#     for idx, record in enumerate(table):
#         try:
#             writer.writerow(list(record.values()))
#         except:
#             # print(idx, "行有問題")
#             # for idx, value in enumerate(list(record.values())):
#             #     repr_value = repr(value)
#             #     fixed_data = ast.literal_eval('"' + repr_value + '"')
#             #     print(eval(fixed_data))
#             pass
                

                

