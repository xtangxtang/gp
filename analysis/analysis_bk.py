import pandas as pd
import time
import os
import numpy as np
from datetime import datetime

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
            existing_data['日期'] = pd.to_datetime(existing_data['日期'])

            # 合并数据并去除重复项
            merged_data = pd.concat([existing_data, data]).drop_duplicates(subset='日期')
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

if __name__ == '__main__':
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    # date_time = datetime.today().strftime('%Y-%m-%d')    
    date_time=""
    # 指定目录路径
    directory = f"../capital/bk"  # 替换为你实际的目录路径    
    analysis_capital(date_time, directory, "板块主力资金", "-bk")

    directory = f"../capital/gn"  # 替换为你实际的目录路径 
    analysis_capital(date_time, directory, "概念主力资金", "-gn")