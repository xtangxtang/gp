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

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
today = datetime.today().strftime('%Y-%m-%d')

# today = "2023-07-10"  

############ 获得每天的大盘涨跌数
captial_df = pd.DataFrame()
csv_file = f"../gp_daily/all/{today}-alldaily.csv"
if not os.path.exists(csv_file):
    print(f"{csv_file} not exist, return")
    exit()    

df = pd.read_csv(f"{csv_file}")
df['涨跌'] = df['涨跌'].replace("--", np.nan)
df = df.dropna(subset=['涨跌'])
df['涨跌'] = df['涨跌'].astype(float)

up_count = len(df[df['涨跌'] > 0])
down_count = len(df[df['涨跌'] < 0])

print(f"上涨的数：{up_count}")
print(f"下跌的数：{down_count}")

bins = [-float('inf'), -0.1, -0.05, 0, 0.05, 0.1, float('inf')]
labels = ['<-10%', '-10%~-5%', '-5%~0%', '0%~5%', '5%~10%', '>10%']

df['涨跌幅(%)'] = df['涨跌幅(%)'].astype(float)
df['涨跌幅区间'] = pd.cut(df['涨跌幅(%)'], bins=bins, labels=labels)

up_10 = len(df[df['涨跌幅(%)'] > 10])
up_5 = len(df[(df['涨跌幅(%)'] > 5) & (df['涨跌幅(%)'] <= 10)])
up_0 = len(df[(df['涨跌幅(%)'] >= 0) & (df['涨跌幅(%)'] <= 5)])
down_5 = len(df[(df['涨跌幅(%)'] < 0) & (df['涨跌幅(%)'] >= -5)])
down_10 = len(df[(df['涨跌幅(%)'] < -5) & (df['涨跌幅(%)'] >= -10)])
down_more_10 = len(df[df['涨跌幅(%)'] < -10])


print(f"上涨10%以上的数：{up_10}")
print(f"上涨5%以上的数：{up_5}")
print(f"上涨0%以上的数：{up_0}")
print(f"下跌5%之内的数：{down_5}")
print(f"下跌10%之内的数：{down_10}")
print(f"下跌超过10%的数：{down_more_10}")

############ 获得每天的大盘资金净流入
captial_df = pd.DataFrame()
csv_file = f"../capital/gg2/{today}-gg2.csv"
if not os.path.exists(csv_file):
    print(f"{csv_file} not exist, return")
    exit()

net_flow_df = pd.read_csv(f"{csv_file}")
# 计算流入资金总和
total_inflow = net_flow_df['流入资金(元)'].sum()

# 计算流出资金总和
total_outflow = net_flow_df['流出资金(元)'].sum()

# 计算流动资金的总和减去流出资金的总和
net_flow = total_inflow - total_outflow
net_flow = convert_scientific_to_chinese(net_flow)
print(net_flow)

############ 获得每天的大盘主力资金净流入
captial_df = pd.DataFrame()
csv_file = f"../capital/all/all-capital.csv"
if not os.path.exists(csv_file):
    print(f"{csv_file} not exist, return")
    exit()

zhuli_df = pd.read_csv(f"{csv_file}")    

# 根据日期获取当天的数据行
row = zhuli_df[zhuli_df['日期'] == today].reset_index(drop=True)
# print(row)

# 提取需要的列数据
desired_columns = ['日期', '上证收盘价', '上证涨跌幅', '深证收盘价', '深证涨跌幅', '主力净流入净额', '主力净流入净占比']
desireddata = row[desired_columns]

data = {
    '日期': [today],
    '上证收盘价': [desireddata['上证收盘价'].values[0]],
    '上证涨跌幅': [desireddata['上证涨跌幅'].values[0]],
    '深证收盘价': [desireddata['深证收盘价'].values[0]],
    '深证涨跌幅': [desireddata['深证涨跌幅'].values[0]],
    '上涨的数': [len(df[df['涨跌幅(%)'] > 0])],
    '下跌的数': [len(df[df['涨跌幅(%)'] < 0])],
    '上涨10%以上的数': [up_10],
    '上涨5%以上的数': [up_5],
    '上涨0%以上的数': [up_0],
    '下跌5%之内的数': [down_5],
    '下跌10%之内的数': [down_10],
    '下跌超过10%的数': [down_more_10],
    '资金净流入': [net_flow],
    '主力净流入净额': [desireddata['主力净流入净额'].values[0]],
    '主力净流入净占比': [desireddata['主力净流入净占比'].values[0]],    
}

result_df = pd.DataFrame(data)
result_df.set_index("日期",inplace=True)

try:
    old_df = pd.read_csv('daily_all_report.csv', index_col="日期")
    merged_df = pd.concat([result_df, old_df]).drop_duplicates()
except FileNotFoundError:
    merged_df = result_df   

print(merged_df)
merged_df.to_csv('daily_all_report.csv')





# counts = [down_more_10, down_10, down_5, up_0, up_5, up_10]

# plt.bar(labels, counts)
# plt.title('每日上涨下跌统计')
# plt.xlabel('涨跌幅区间')
# plt.ylabel('数量')
# plt.show()