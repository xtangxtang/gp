import pandas as pd
import time
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from cn2an import an2cn

# 转换函数
def convert_scientific_to_chinese(number):
    if number < 0:
        return "-" + str(int(abs(number / 1e8))) + "亿"
    else:
        return str(int(number / 1e8)) + "亿"

if 'TODAY' in os.environ:
    today = os.environ['TODAY']
    print(f"TODAY 环境变量的值为: {today_time}")
else:
    print("TODAY 环境变量不存在")    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today = datetime.today().strftime('%Y-%m-%d')  

# today = "2023-07-28"  

captial_df = pd.DataFrame()
csv_file = f"../capital/同花顺行业/{today}-hy.csv"
if not os.path.exists(csv_file):
    print(f"{csv_file} not exist, return")
    exit()    

hy_df = pd.read_csv(f"{csv_file}")
hy_df = hy_df.drop(columns=["Unnamed: 0", "公司家数", "领涨股", "涨跌幅.1",  "当前价(元)"])
hy_df['成交额'] = hy_df['流入资金(亿)'] + hy_df['流出资金(亿)']
print(hy_df)

csv_file = f"../gp_daily/all/{today}-alldaily.csv"
df = pd.read_csv(csv_file)
total_volume = df['成交额'].sum()
total_volume = convert_scientific_to_chinese(total_volume)
total_volume = float(total_volume.replace("亿", ""))
print(total_volume)

# 计算 "成交额占比%" 列并添加到 DataFrame
hy_df['成交额占比%'] = (hy_df['成交额'] / total_volume) * 100
hy_df['成交额占比%'] = hy_df['成交额占比%'].round(2)  # 保留两位小数
hy_df = hy_df.sort_values(by='成交额占比%', ascending=False)
hy_df.to_csv(f"同花顺行业资金/{today}-hy.csv")
print(hy_df)

