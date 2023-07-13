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

def generate_days_gg_capital_report(date, by_date):
    directory = "个股资金分析/all/"

    # 创建一个空的 DataFrame 用于保存结果
    result_df = pd.DataFrame()

    # 遍历目录中的 CSV 文件
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory, file_name)
            
            # 读取 CSV 文件
            df = pd.read_csv(file_path)
            
            df['日期'] = pd.to_datetime(df['日期'])
            # 按照日期降序排序
            df = df.sort_values('日期', ascending=False)
            
            # 找出指定日期之前的最近10行数据
            specified_date = pd.to_datetime(date) 
            recent_10_days = df[df['日期'] <= specified_date].head(by_date)
            
            # 计算净买入率的总和
            recent_10_days['净买入率'] = recent_10_days['净买入率'].str.rstrip('%').astype(float) / 100        
            net_buy_sum = recent_10_days['净买入率'].sum()
            # print(net_buy_sum)
            
            # 如果净买入率总和大于0，则添加股票简称到结果 DataFrame
            if net_buy_sum > 0.01:
                stock_names = recent_10_days['股票简称'].unique()
                latest_price = recent_10_days.iloc[0]['最新价']
                prev_close = recent_10_days.iloc[-1]['最新价']
                
                price_change = (latest_price - prev_close) / prev_close
                
                net_buy_ratio = abs(net_buy_sum / price_change)
                
                data = pd.DataFrame({
                    '股票简称': stock_names,
                    f'{by_date}日净买入率总和': net_buy_sum,
                    f'{by_date}日最新价涨跌幅': price_change,                    
                    f'{by_date}日净买入率/涨跌幅': net_buy_ratio
                })
                result_df = pd.concat([result_df, data], ignore_index=True)

    # 去除重复的股票简称
    result_df = result_df.drop_duplicates()

    # 按照净买入率/涨跌幅总和从高到低排序
    result_df1 = result_df.sort_values(f'{by_date}日净买入率/涨跌幅', ascending=False)
    # 按照净买入率总和从高到低排序
    result_df2 = result_df.sort_values(f'{by_date}日净买入率总和', ascending=False)

    # 将净买入率总和转换回百分比格式
    result_df1[f'{by_date}日净买入率总和'] = (result_df1[f'{by_date}日净买入率总和'] * 100).round(2).astype(str) + '%'    
    result_df1[f'{by_date}日最新价涨跌幅'] = (result_df1[f'{by_date}日最新价涨跌幅'] * 100).round(2).astype(str) + '%' 
    # 打印结果
    print(result_df1.head(50))
    result_df1.to_csv(f"个股资金每日报告/{date}/{by_date}日净买入率涨跌幅.csv", index=False)

    # 将净买入率总和转换回百分比格式
    result_df2[f'{by_date}日净买入率总和'] = (result_df2[f'{by_date}日净买入率总和'] * 100).round(2).astype(str) + '%'    
    result_df2[f'{by_date}日最新价涨跌幅'] = (result_df2[f'{by_date}日最新价涨跌幅'] * 100).round(2).astype(str) + '%' 
    # 打印结果
    print(result_df2.head(50))
    result_df2.to_csv(f"个股资金每日报告/{date}/{by_date}日净买入率.csv", index=False)    
    

if __name__ == '__main__':
    gg2_dir = "../capital/gg2/"
    gg_alldaily_dir = "../gp_daily/all/"

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    # today_time = "2023-07-12"

    # 读取文件目录1下的CSV文件
    # read_csv_files(gg2_dir, gg_alldaily_dir, today_time)
    # conver_ltsz()

    gnzl_dir = "个股资金分析/all"

    directory = f"个股资金每日报告/{today_time}"

    # 检查目录是否存在
    if not os.path.exists(directory):
        # 创建目录
        os.makedirs(directory)
        
    generate_days_gg_capital_report(today_time, 30)
    generate_days_gg_capital_report(today_time, 10)
    generate_days_gg_capital_report(today_time, 5)
    generate_days_gg_capital_report(today_time, 1)

