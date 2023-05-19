""" 檢查DBF轉CSV使用 """
# 完整 - dbf_to_csv_complete.py

from dbfread import DBF, FieldParser, InvalidValue
import csv

# 這個類別繼承了dbfread.FieldParser類別
class MyFieldParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data)  # 呼叫父類別的parse方法進行資料解析
        except ValueError:
            return InvalidValue(data)  # 根據你選擇的編碼格式，如果解析出錯，回傳InvalidValue物件

# 使用自定義的FieldParser類別來讀取DBF檔案
# 一個DBF檔案做轉換CSV
table = DBF('ALL_CD\\BK242\\852\\tzcol\\COL_E.DBF', parserclass=MyFieldParser, encoding='ANSI')

# 計算有多少資料有誤
invalid_value_record_count = 0

# 測試轉出來的csv
with open('test.csv', 'w', encoding="ANSI", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(table.field_names)  # 寫入CSV檔案的欄位名稱

    for i, record in enumerate(table):
        # 預設每列是需要寫入CSV
        status = True

        # 檢查資料是否有問題
        for name, value in record.items():
            if isinstance(value, InvalidValue):
                # 處理無效值的資料列
                # !r 是一種格式化字串中的一部分，它表示要在該位置插入一個值的repr形式
                # i+2 的原因是檔案第一列是表頭所以不算,在檔案來看是+1才開始算，程式loop是從0開始所以再+1，程式才會告訴你檔案中有問題的正確位置
                print('records[{}][{!r}] == {!r}'.format(i+2, name, value))
                invalid_value_record_count += 1
                status = False # 若有問題就會設定不寫入該行

        # 沒問題的就會寫入CSV
        if status:
            writer.writerow(list(record.values()))

f.close()
print(invalid_value_record_count, "個錯誤")
