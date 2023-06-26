import pandas as pd
import time
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
today = datetime.today().strftime('%Y-%m-%d')  

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
down_5 = len(df[(df['涨跌幅(%)'] < 5) & (df['涨跌幅(%)'] >= -5)])
down_10 = len(df[(df['涨跌幅(%)'] < -5) & (df['涨跌幅(%)'] >= -10)])
down_more_10 = len(df[df['涨跌幅(%)'] < -10])


print(f"上涨10%以上的数：{up_10}")
print(f"上涨5%以上的数：{up_5}")
print(f"上涨0%以上的数：{up_0}")
print(f"下跌5%之内的数：{down_5}")
print(f"下跌10%之内的数：{down_10}")
print(f"下跌超过10%的数：{down_more_10}")

data = {
    '日期': [today],
    '上涨的数': [len(df[df['涨跌幅(%)'] > 0])],
    '下跌的数': [len(df[df['涨跌幅(%)'] < 0])],
    '上涨10%以上的数': [up_10],
    '上涨5%以上的数': [up_5],
    '上涨0%以上的数': [up_0],
    '下跌5%之内的数': [down_5],
    '下跌10%之内的数': [down_10],
    '下跌超过10%的数': [down_more_10]
}

result_df = pd.DataFrame(data)
result_df.set_index("日期",inplace=True)

try:
    old_df = pd.read_csv('daily_all_report.csv', index_col="日期")
except FileNotFoundError:
    old_df = pd.DataFrame()    

merged_df = pd.concat([old_df, result_df]).drop_duplicates()

merged_df.to_csv('daily_all_report.csv')





# counts = [down_more_10, down_10, down_5, up_0, up_5, up_10]

# plt.bar(labels, counts)
# plt.title('每日上涨下跌统计')
# plt.xlabel('涨跌幅区间')
# plt.ylabel('数量')
# plt.show()