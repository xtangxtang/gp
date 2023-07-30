import os
import pandas as pd
from datetime import datetime

# 获取当前日期
today = datetime.now().strftime('%Y-%m-%d')
today = "2023-07-21"


# 构造 CSV 文件名
csv_filename = f"{today}-alldaily.csv"

# 完整的文件路径
csv_filepath = os.path.join('../gp_daily/all/', csv_filename)

# 检查文件是否存在并读取
if os.path.exists(csv_filepath):
    # 读取 CSV 文件
    df = pd.read_csv(csv_filepath)

    # 将 '涨跌幅(%)' 列转换为数值类型
    df['涨跌幅(%)'] = pd.to_numeric(df['涨跌幅(%)'], errors='coerce')    

    # 筛选涨跌幅大于 9.90% 的代码和名称
    filtered_df = df[df['涨跌幅(%)'] > 9.90][['代码', '名称']]

    print(filtered_df)
else:
    print(f"文件 {csv_filepath} 不存在")
