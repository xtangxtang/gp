import os
import glob
from datetime import datetime
import pandas as pd
import pysnowball as ball
import argparse
import pandas as pd

def calculate_sum(file_name, date_str, delta_time, path='.'):
    # 读取 CSV 文件
    df = pd.read_csv(f'{path}/{file_name}')
    
    # 将日期列转换为 datetime 类型
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 筛选出给定日期前 10 行的数据
    mask = df['日期'] <= date_str
    data = df.loc[mask].head(delta_time)
    print(data)
    
    # 计算净额(亿元)和净买入率总和
    net_amount_sum = round(data['净额(亿元)'].sum(), 2)
    net_buy_rate_sum = round(data['净买入率'].str.rstrip('%').astype('float').sum(), 2)
    
    net_buy_rate_sum = f'{net_buy_rate_sum}%'
    
    print(f'{delta_time}日净额(亿元)总和: {net_amount_sum}')
    print(f'{delta_time}日净买入率总和: {net_buy_rate_sum}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--Symbol", help="股票代码")
    parser.add_argument("-d", "--Bydate", help="日期")
    parser.add_argument("-p", "--Period", help="天数")

    args = parser.parse_args()
    symbol = args.Symbol
    bydate = args.Bydate
    period = args.Period

    gnzl_dir = "个股资金分析/all"

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')

    symbol = symbol + ".csv"
    period = int(period)  

    calculate_sum(symbol, bydate, period, gnzl_dir)

    # ball.set_token('xq_a_token=059ca42bb432441cdb7c65fcd755ac80e61f4e36;')
    # print(ball.cash_flow('SH600000'))
