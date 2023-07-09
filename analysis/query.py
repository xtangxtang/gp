import os
import glob
from datetime import datetime
import pandas as pd

def get_days_gg_capital(date, by_date):
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
                
                net_buy_ratio = net_buy_sum / price_change
                
                data = pd.DataFrame({
                    '股票简称': stock_names,
                    f'{by_date}日净买入率总和': net_buy_sum,
                    f'{by_date}日最新价涨跌幅': price_change,                    
                    f'{by_date}日净买入率/涨跌幅': net_buy_ratio
                })
                result_df = pd.concat([result_df, data], ignore_index=True)

    # 去除重复的股票简称
    result_df = result_df.drop_duplicates()

    # 按照净买入率总和从高到低排序
    # result_df = result_df.sort_values('净买入率总和', ascending=False)

    result_df = result_df.sort_values(f'{by_date}日净买入率/涨跌幅', ascending=False)

    # 将净买入率总和转换回百分比格式
    result_df[f'{by_date}日净买入率总和'] = (result_df[f'{by_date}日净买入率总和'] * 100).round(2).astype(str) + '%'    

    result_df[f'{by_date}日最新价涨跌幅'] = (result_df[f'{by_date}日最新价涨跌幅'] * 100).round(2).astype(str) + '%' 

    # 打印结果
    print(result_df)


if __name__ == '__main__':
    gnzl_dir = "个股资金分析/all"

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    get_days_gg_capital("2023-07-07", 10)
