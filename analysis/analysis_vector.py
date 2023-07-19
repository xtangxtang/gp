# 导入需要的库
import numpy as np 
from chroma import open

# 连接Chroma
client = open()

# 生成模拟交易数据
times = [9:30, 9:31, 9:32, 10:00, 10:05,...] # 时间
changes = [0.5%, 1.2%, -0.2%,...] # 涨跌幅 
turnovers = [1.5%, 2.1%, 0.8%,...] # 换手率

# 构造向量
vectors = [[t, c, r] for t, c, r in zip(times, changes, turnovers)]
vectors = [np.array(v) for v in vectors] 

# 插入向量数据
client.insert('stock_trades', 
              [{'time': t, 'code': 'AAPL', 'vector': v}
               for t, v in zip(times, vectors)])

# 后续查询分析...