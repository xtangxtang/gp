import pandas as pd
import os
from datetime import datetime

def conver_ltsz():
    directory = "./个股资金分析/all/"

    # 遍历目录中的 CSV 文件
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            
            # 读取 CSV 文件
            df = pd.read_csv(file_path)
            
            # 对指定列进行除法运算
            df["流通市值"] = df["流通市值"] / 100000000
            
            # 更改列名
            df.rename(columns={"流通市值": "流通市值(亿)"}, inplace=True)
            
            # 保存修改后的 DataFrame 到 CSV 文件
            df.to_csv(file_path, index=False)


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
    print(simplified_number)
    # simplified_number += decimals[decimal_index]
    simplified_number += units[unit_index]
    
    return simplified_number

def extract_date_prefix(file_name):
    date_prefix = file_name.split('-')[0]
    return date_prefix

def find_file(start_str, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith(start_str):
                return os.path.join(root, file)        
    return None

def read_csv_files(gg2_dir1, all_daily_dir2, date):
    gg2_file = find_file(date, gg2_dir1)
    if gg2_file:
        print(f'找到文件: {gg2_file}')
    else:
        print('未找到文件') 
        exit()

    gg_daily_file = find_file(date, all_daily_dir2)
    if gg_daily_file:
        print(f'找到文件: {gg_daily_file}')
    else:
        print('未找到文件')
        exit()               

    all_data = pd.DataFrame()

    gg2_data = pd.read_csv(gg2_file, index_col='代码')
    gg_daily_data = pd.read_csv(gg_daily_file, index_col='代码')

    # all_data = pd.concat([gg2_data, gg_daily_data], axis=1)
    all_data = pd.merge(gg2_data, gg_daily_data, on="代码", how="inner")
    all_data = all_data.dropna()
    all_data = all_data.drop(["名称", "现价", "涨跌幅(%)", "涨跌", "换手(%)", "成交额"], axis=1)
    all_data["净额(元)"] = all_data["流入资金(元)"] - all_data["流出资金(元)"]

    # 计算净买入率
    all_data["净买入率"] = all_data["净额(元)"] / all_data["流通市值"]

    # 将"净买入率"列插入到"净额(元)"列后面
    column_order = list(all_data.columns)
    # column_order.insert(column_order.index("净额(元)") + 1, "净买入率")    
    all_data = all_data[column_order]
    all_data.insert(0, "日期", date)  

    # all_data = all_data.drop(all_data.columns[-1], axis=1)
    


    # 将列名转换为中文单位
    all_data = all_data.rename(columns={
        "流入资金(元)": "流入资金(亿元)",
        "流出资金(元)": "流出资金(亿元)",
        "净额(元)": "净额(亿元)",
        "成交额(元)": "成交额(亿元)"
    })

    all_data['流入资金(亿元)'] = all_data['流入资金(亿元)'] / 100000000
    all_data['流出资金(亿元)'] = all_data['流出资金(亿元)'] / 100000000  
    all_data['净额(亿元)'] = all_data['净额(亿元)'] / 100000000 
    all_data['成交额(亿元)'] = all_data['成交额(亿元)'] / 100000000 

    # 将"净买入率"列转换为数值格式
    all_data["净买入率"] = pd.to_numeric(all_data["净买入率"], errors='coerce')
    print(all_data["净买入率"])

    # 将净买入率转换为百分比形式
    all_data["净买入率"] = all_data["净买入率"].apply(lambda x: '{:.2%}'.format(x))

    # 提取并删除"净买入率"列
    net_buy_rate = all_data.pop("净买入率")

    # 将"净买入率"列插入到"净额(亿元)"列后面
    all_data.insert(all_data.columns.get_loc("净额(亿元)") + 1, "净买入率", net_buy_rate)

    print(all_data)

    for index, row in all_data.iterrows():
        filename = str(index) + ".csv"  # 以索引值作为文件名
        filename = "个股资金分析/all/" + filename
        new_row = pd.DataFrame(row).T
        new_row.reset_index(drop=True, inplace=True)
        if os.path.isfile(filename):
            existing_data = pd.read_csv(filename)
            existing_data = existing_data.append(new_row)
            existing_data.sort_values(by='日期', ascending=False, inplace=True)
            existing_data.to_csv(filename, index=False)
        else:
            row_data = pd.DataFrame(row).T  # 将当前行数据转换为 DataFrame
            row_data.to_csv(filename, index=False)  # 将数据保存到文件


if __name__ == '__main__':
    gg2_dir = "../capital/gg2/"
    gg_alldaily_dir = "../gp_daily/all/"

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    # 读取文件目录1下的CSV文件
    data1 = read_csv_files(gg2_dir, gg_alldaily_dir, today_time)
    # conver_ltsz()

