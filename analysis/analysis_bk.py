import pandas as pd
import time
import os
import numpy as np
from datetime import datetime
import glob
import re

# 转换函数
def convert_scientific_to_chinese(number):
    units = ['', '万', '亿']
    # decimals = ['', '十', '百', '千']
    number_str = str(number)
    length = len(number_str)
    
    if length <= 4:
        return number_str
    
    unit_index = (length - 1) // 4
    decimal_index = (length - 1) % 4
    
    simplified_number = number_str[:decimal_index + 1]
    # simplified_number += decimals[decimal_index]
    simplified_number += units[unit_index]
    
    return simplified_number

def analysis_capital(by_date, in_dir, out_dir, omit_str):
    print(f"by_date:{by_date}")
    if by_date == "":
        by_date = "1900-01-01"    
    
    by_date = datetime.strptime(by_date, '%Y-%m-%d').date()
    # 创建一个空列表，用于存储 CSV 文件名
    file_list = []

    # 遍历目录中的所有文件
    for filename in os.listdir(in_dir):
        # 筛选出以 ".csv" 结尾的文件
        if filename.endswith(".csv"):
            # 将文件名添加到列表中
            file_list.append(os.path.join(directory, filename))

    # 创建一个空字典，用于存储不同名称的数据
    data_dict = {}

    # 遍历文件列表
    for file in file_list:
        # 提取文件名中的日期部分
        filename = os.path.basename(file)
        print(filename)
        date_str = filename.replace(f"{omit_str}.csv", "")   
        print(date_str)
        date = datetime.strptime(date_str, '%Y-%m-%d').date() 
        if date < by_date:
            continue

        # 读取 CSV 文件
        df = pd.read_csv(file)
        df['日期'] = date_str
        # df.set_index(["日期"], inplace=True)
        print(df.head())
        
        
        # 遍历每行数据
        for index, row in df.iterrows():
            # 获取名称列的值
            name = row['名称']
            
            # 如果名称不在字典中，创建一个新的空DataFrame，并将其作为值存储在字典中
            if name not in data_dict:
                data_dict[name] = pd.DataFrame(columns=df.columns)
            
            # 将当前行添加到相应名称的DataFrame中
            data_dict[name] = data_dict[name].append(row)
        
    # 保存数据到不同文件
    # for name, data in data_dict.items():
    #     name = name.replace(f"/", "-")         
    #     print(f"name: {name}")
    #     filename = f"{out_dir}/{name}.csv"
    #     # 规范化文件名        
    #     data.sort_values(by='日期', ascending=False, inplace=True)
    #     data.set_index(["日期"], inplace=True)
    #     data.to_csv(filename)
    #     print(f"保存 {name} 数据到 {filename}")


    for name, data in data_dict.items():
        name = name.replace(f"/", "-") 
        print(f"name: {name}")
        filename = f"{out_dir}/{name}.csv"

        if os.path.exists(filename):
            # 读取已存在的 CSV 文件数据
            existing_data = pd.read_csv(filename)
            # existing_data['日期'] = pd.to_datetime(existing_data['日期'])
            # print("existing_data")
            # print(existing_data)

            # 合并数据并去除重复项
            merged_data = pd.concat([existing_data, data]).drop_duplicates()
            # print("merged_data")
            # print(merged_data)
            merged_data.sort_values(by='日期', ascending=False, inplace=True)
            merged_data.set_index(["日期"], inplace=True)                   

            # 保存合并后的数据到 CSV 文件
            merged_data.to_csv(filename)
            print(f"合并 {name} 数据并保存到 {filename}")
        else:
            # 直接保存数据到 CSV 文件
            data.sort_values(by='日期', ascending=False, inplace=True)
            data.set_index(["日期"], inplace=True)                  
            data.to_csv(filename)      
            print(f"保存 {name} 数据到 {filename}")

def analysis_continue(dir, out_dir, continue_day):
    # 定义CSV文件路径
    csv_files = glob.glob(f'{dir}/*.csv')

    # # 创建一个空的DataFrame来存储所有数据
    # all_data = pd.DataFrame()

    # # 读取所有CSV文件并合并数据
    # for file in csv_files:
    #     df = pd.read_csv(file)
    #     # print(df)
    #     # all_data = all_data.append(df)

    #     # 将日期列转换为日期类型
    #     df['日期'] = pd.to_datetime(df['日期'])

    #     # 找出最近10日中今日主力净流入净额为正的名称
    #     recent_10_days = df['日期'].sort_values(ascending=False).unique()[:10]
    #     positive_data = df[df['日期'].isin(recent_10_days)  & (df['今日主力净流入(净额)'] > 0)][['日期', '名称', '今日主力净流入(净额)']]
    #     # print(positive_data)

    #     row_count = len(positive_data)
    #     # print(f"行数: {row_count}")

    #     if row_count >= 3:
    #         print(positive_data)

    # 创建一个空的DataFrame来存储所有数据
    all_data = pd.DataFrame()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    date_time = datetime.today().strftime('%Y-%m-%d')        

    # 读取所有CSV文件并合并数据
    for file in csv_files:
        df = pd.read_csv(file)
        # all_data = all_data.append(df)

        # 将日期列转换为日期类型
        df['日期'] = pd.to_datetime(df['日期'])

        # 找出最近10日中今日主力净流入净额为正的名称
        recent_10_days = df['日期'].sort_values(ascending=False).unique()[:continue_day]
        positive_data = df[df['日期'].isin(recent_10_days)][['日期', '名称', '今日主力净流入(净额)']]
        if positive_data['今日主力净流入(净额)'].sum() > 0:
            print(positive_data['名称'][0] +": " + str(convert_scientific_to_chinese((positive_data['今日主力净流入(净额)'].sum()))))
            tmpdf = pd.DataFrame({'日期': date_time, '概念名称': positive_data['名称'][0], '净流入': positive_data['今日主力净流入(净额)'].sum()}, index=[0])
            tmpdf.set_index(['日期'], inplace=True)
            all_data = all_data.append(tmpdf)

    if len(all_data) > 0:
        all_data.sort_values(by='净流入', ascending=False, inplace=True)
        all_data['净流入'] = all_data['净流入'].apply(convert_scientific_to_chinese)
        print(all_data)
        all_data.to_csv(f"{out_dir}/{date_time}-{continue_day}日-主力净流入.csv")

if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    date_time = datetime.today().strftime('%Y-%m-%d')    
    # date_time=""
    # 指定目录路径
    directory = f"../capital/bk"  # 替换为你实际的目录路径    
    analysis_capital(date_time, directory, "板块主力资金", "-bk")

    directory = f"../capital/gn"  # 替换为你实际的目录路径 
    analysis_capital(date_time, directory, "概念主力资金", "-gn")

    directory = f"./概念主力资金/"  # 替换为你实际的目录路径 
    out_dir= f"./概念主力资金分析/"
    analysis_continue(directory, out_dir, 10)

    directory = f"./板块主力资金/"  # 替换为你实际的目录路径 
    out_dir= f"./板块主力资金分析/"
    analysis_continue(directory, out_dir, 10)   

    directory = f"./概念主力资金/"  # 替换为你实际的目录路径 
    out_dir= f"./概念主力资金分析/"
    analysis_continue(directory, out_dir, 5)

    directory = f"./板块主力资金/"  # 替换为你实际的目录路径 
    out_dir= f"./板块主力资金分析/"
    analysis_continue(directory, out_dir, 5)        