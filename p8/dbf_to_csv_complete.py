""" DBF轉檔csv 版本2 用這個 """
# 跳過有invalid value的資料，繼續輸出csv

from dbfread import DBF, FieldParser, InvalidValue
import sys
import os 
import csv

class MyFieldParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)
        except ValueError:
            return InvalidValue(data)

# 第二層或更多判斷
def is_file(path, name):
    # 確定是DBF檔案
    if path.endswith('.DBF'):
        # 寫入CD文件夾, CD/BK220/...
        filename = target_dir + "/" + name + ".csv" # CD/BK220/D84_TZ_AREA.csv
        print(path, "->", filename)

        # 讀取DBF檔案
        table = DBF(path, parserclass=MyFieldParser, encoding='ANSI', ignore_missing_memofile=True)

        # 寫入CSV檔案
        with open(filename, 'w', encoding='ANSI', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(table.field_names)
            for i, record in enumerate(table):
                status = True
                for name, value in record.items():
                    if isinstance(value, InvalidValue):
                        # print('records[{}][{!r}] == {!r}'.format(i+2, name, value))
                        status = False
                if status:
                    writer.writerow(list(record.values()))

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
            cname = name + "_" + foldername # BK220/D84_TZ
            is_dir(fpath, cname) # fpath = CD_0511/BK220/D84/TZ
            cname = name

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
while True:
    print("*** 如果要結束執行檔請在以下兩個輸入框中輸入q ***\n")

    root = input('DBF檔案根目錄：') # CD
    target_dir = input('儲存CSV目錄：')
    if root == "q" or target_dir == "q":
        break

    if os.path.exists(root):
        if os.path.exists(target_dir):
            print("現在開始處理...")
            for idx, cd in enumerate(os.listdir(root)):
                if not os.path.exists(os.path.join(target_dir, cd)):
                    os.mkdir(os.path.join(target_dir, cd))

                path = os.path.join(root, cd)
                print(f"========================================================================\n{idx+1}. {path}")
                f_list(path)
            # break
        else:
            print("儲存CSV目錄不存在\n")
            continue
    else:
        print("DBF檔案根目錄不存在\n")
        continue

sys.exit("\n*** 結束，拜拜 ***")


