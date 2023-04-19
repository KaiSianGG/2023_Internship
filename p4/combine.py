import csv
import pandas as pd
import os
import numpy as np

''' 步驟1: 載入csv檔案 '''

folder = "C:/Users/User/Documents/Internship/p4/專案3：新授證慈委參與活動狀況"
csv_files = []

for f in os.listdir(folder):
    if f.endswith(".csv"):
        csv_files.append(f)
# print(csv_files)

def read_data(df):
    data = []
    rows = []
    row_num, column_num = df.shape
    for index,row in df.iterrows():
        for i in range(column_num):
            # 使用loc函數訪問每一列的每一欄資料，加入到rows
            rows.append(row.loc[df.columns[i]])
        data.append(rows) # 再將rows陣列加入到data
        rows = [] # 清空rows
    return data

basic_info = read_data(pd.read_csv(os.path.join(folder,csv_files[2])))
cadre = read_data(pd.read_csv(os.path.join(folder,csv_files[0])))
activity = read_data(pd.read_csv(os.path.join(folder,csv_files[1])))

''' 步驟2: 寫入新的csv檔案 '''

with open("C:/Users/User/Documents/Internship/p4/final.csv", "w", newline="", encoding="utf-8-sig") as wf:
    header = ['國別','姓名','性別','法號','出生年','合心','和氣','委員授證年','慈誠授證年','慈濟經歷','活動分類','活動大類','活動']
    writer = csv.DictWriter(wf, fieldnames=header)
    writer.writeheader() # 寫入表頭

    for i in range(len(basic_info)): # 跑5213次
        print(i, basic_info[i][0]) 

        # 2.1: 慈濟經歷
        cadre_str = ""
        for j in range(len(cadre)): # 跑885次
            if cadre[j][0] == basic_info[i][0]:
                cadre_str += f", {cadre[j][2]}"

        # 2.2: 活動分類、活動大類、活動
        activities = ""
        big_category = {}
        small_category = {}

        for x in range(len(activity)): # 跑446014次
            if activity[x][0] == basic_info[i][0]: # 參與活動記錄id是該志工id

                if isinstance(activity[x][1], str): # 判斷是不是字串，因爲資料中有NaN
                    year = activity[x][1][0:4] # 抓取年份
                    if year not in ["2021","2022","2023"]: # 判斷年份不是這3年就跳過
                        continue
                else:
                    continue

                # 活動
                activities += f", {activity[x][1]}"

                # 活動大類
                if year in big_category:
                    if activity[x][3] in big_category[year]:
                        big_category[year][activity[x][3]] += 1
                    else:
                        big_category[year][activity[x][3]] = 1
                else:
                    big_category[year] = {activity[x][3]:1}

                # 活動小類
                if activity[x][2] in small_category:
                    small_category[activity[x][2]] += 1
                else:
                    small_category[activity[x][2]] = 1
        
        # 物件轉換成小類、大類字串
        small = ""
        for key, value in small_category.items():
            small += f", {key}:{value}次"

        big = ""
        for year, value in big_category.items():
            for key, val in value.items():
                big += f", {year}:{key}:{val}次"

        # print(big_category)

        basic_info[i].append(cadre_str)
        basic_info[i].append(small)
        basic_info[i].append(big)
        basic_info[i].append(activities)

        # 輸入一列到combine.csv
        writer.writerow({
            '國別':basic_info[i][1], 
            '姓名':basic_info[i][2], 
            '性別':basic_info[i][3],
            '法號':basic_info[i][4],
            '出生年':basic_info[i][5],
            '合心':basic_info[i][6],
            '和氣':basic_info[i][7],
            '委員授證年':basic_info[i][8],
            '慈誠授證年':basic_info[i][9],
            '慈濟經歷':basic_info[i][10],
            '活動分類':basic_info[i][11],
            '活動大類':basic_info[i][12],
            '活動':basic_info[i][13]
        })