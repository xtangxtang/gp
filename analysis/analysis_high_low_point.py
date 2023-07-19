import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from scipy.signal import argrelextrema
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error

# 收集和预处理数据
df = pd.read_csv('/mnt/nvme0n1/gp/gp_daily/sh603290/2023-07-14.csv')
prices = df['成交价'].values
df["涨跌幅"] = df["涨跌幅"].str.strip("%").astype(float)
changes = df['涨跌幅'].values
scaler = StandardScaler()  
prices = scaler.fit_transform(prices.reshape(-1, 1))


# 定义线性回归模型
# model = SGDRegressor(max_iter=1000, tol=1e-3)


# # 梯度下降寻优 
# model.fit(X, prices)  

# 定义 SGDRegressor
sgd_reg = SGDRegressor()
X = np.arange(len(prices)).reshape(-1, 1)
y = prices
# 记录loss
losses = []
for _ in range(1000):
  sgd_reg.partial_fit(X, y)
  y_pred = sgd_reg.predict(X)
  
  # 使用均方误差作为loss函数
  curr_loss = mean_squared_error(y, y_pred)
  losses.append(curr_loss)

# 找到波动最大的时刻作为转折点
turning_points = argrelextrema(losses, np.greater)  
print(turning_points)

# 根据涨跌幅判断高低点
for t in turning_points:
    if changes[t] > 0:
        print(f"{t} is a low point")
    else:
        print(f"{t} is a high point")