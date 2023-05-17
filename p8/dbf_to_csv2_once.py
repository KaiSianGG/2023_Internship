""" 檢查DBF轉CSV使用 """

# 完整 - dbf_to_csv2

from dbfread import DBF, FieldParser, InvalidValue
import csv 

# 這個類別繼承了dbfread.FieldParser類別
class MyFieldParser(FieldParser):
    def parse(self, field, data):
        try:
            return FieldParser.parse(self, field, data) # 呼叫父類別的parse方法進行資料解析
        except ValueError:
            return InvalidValue(data) # 如果解析出錯，回傳InvalidValue物件

# 使用自定義的FieldParser類別來讀取DBF檔案
table = DBF('ALL_CD\\BK228\\VOU_4.DBF', parserclass=MyFieldParser, encoding='ANSI')

invalid_value_record_count = 0
with open('test.csv', 'w', encoding="ANSI", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(table.field_names) # 寫入CSV檔案的欄位名稱
    for i, record in enumerate(table):
        status = True
        for name, value in record.items():
            if isinstance(value, InvalidValue):
                # 處理無效值的資料列
                # 是一種格式化字串中的一部分，它表示要在該位置插入一個值的repr形式
                print('records[{}][{!r}] == {!r}'.format(i+2, name, value))
                invalid_value_record_count+=1
                status = False
        if status:
            writer.writerow(list(record.values()))

f.close()
print(invalid_value_record_count, "個錯誤")