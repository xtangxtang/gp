import numpy as np
import pandas as pd
import seaborn as sns
import warnings
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextWarning
from fitter import Fitter, get_common_distributions, get_distributions
import numpy as np
from scipy.stats import entropy
from math import log, e
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date, timedelta

# Customize matplotlib
warnings.filterwarnings("ignore", message="Glyph 146 missing from current font.")

def entropy1(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  return entropy(counts, base=base)

def entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value,counts = np.unique(labels, return_counts=True)
  probs = counts / n_labels
  n_classes = np.count_nonzero(probs)

  if n_classes <= 1:
    return 0

  ent = 0.

  # Compute entropy
  base = e if base is None else base
  for i in probs:
    ent -= i * log(i, base)

  return ent

def entropy3(labels, base=None):
  vc = pd.Series(labels).value_counts(normalize=True, sort=False)
  base = e if base is None else base
  return -(vc * np.log(vc)/np.log(base)).sum()

def entropy4(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  norm_counts = counts / counts.sum()
  base = e if base is None else base
  return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()

def analysis_entropy(today_time=""):
    dir_list = os.listdir("gp_daily")
    working_path = os.getcwd()
    os.chdir("gp_daily")
    
    col_names=["symbols"]

    entr_file = f"entropy/entropy.csv"

    entropy_df = pd.DataFrame(columns=col_names)
    entropy_df.set_index("symbols")

    for symbol in dir_list:
      print(f"{symbol}")
      datefiles = os.listdir(symbol)
      os.chdir(symbol)
      for datef in datefiles:
        dataset = pd.read_csv(datef, delimiter=",")
        date = os.path.splitext(datef)[0]  
        if today_time != "" and date != today_time:    
          continue
        sliced_df = dataset.loc[:,["成交价","成交量(手)"]]
        # print(sliced_df.head)
        group_zxj = dataset.groupby("成交价").agg({'成交量(手)': ['sum']})
        # print(group_zxj) 
        bin_num=len(group_zxj.index)
        # print(f"bin_num {bin_num}")
        cjbs_list =  np.array(list(group_zxj.iloc[:, 0]))
        # print(cjbs_list)
        
        entr = entropy(cjbs_list)
        # print(f"    {date} entropy: {entr}")
        # entr = entropy1(cjbs_list)
        # print("entropy1: " + str(entr))
        # entr = entropy2(cjbs_list)
        # print("entropy2: " + str(entr))
        # entr = entropy3(cjbs_list)
        # print("entropy3: " + str(entr))
        # entr = entropy4(cjbs_list)
        # print("entropy4: " + str(entr)) 
        exist_col_names = entropy_df.columns.values.tolist()
        if (entropy_df["symbols"] == symbol).any():
          if date in exist_col_names:
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("0 entropy_df: ")
            print(entropy_df)
          else:
            entropy_df[date]=""
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("1 entropy_df: ")
            print(entropy_df)            
        else:
          if date in exist_col_names:
            entropy_df.loc[len(entropy_df)] = symbol
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("2 entropy_df: ")
            print(entropy_df)  
          else:
            entropy_df.loc[len(entropy_df)] = symbol
            entropy_df[date]=""
            entropy_df.loc[entropy_df["symbols"] == symbol, date] = entr
            print("3 entropy_df: ")
            print(entropy_df) 
      os.chdir("../")
    
    os.chdir(working_path)
    pre_entropy_df = pd.DataFrame(columns=col_names)
    if os.path.exists(entr_file):
       print("entr_file: " + entr_file)
       pre_entropy_df = pd.read_csv(entr_file, delimiter=",")
       
    pre_entropy_df = pre_entropy_df.set_index("symbols")
    print("pre_entropy_df:")
    print(pre_entropy_df)
    entropy_df = entropy_df.set_index("symbols")
    entropy_df = pd.concat([pre_entropy_df,entropy_df], axis=1).drop_duplicates()
    print(entropy_df)
    entropy_df.to_csv(working_path+"/entropy/entropy.csv", index_label="symbols")
    os.chdir(working_path)  
  
# def draw_daily_line(symbol, date):
#   dir_list = os.listdir("gp_daily")
#   cwd = os.getcwd()
#   os.chdir("gp_daily")

#   if not os.path.exists(symbol):
#     print(f"{symbol} is not in directory: " + os.getcwd())
#   os.chdir(symbol)
#   csv_file = date + ".csv"
#   daily_df = pd.read_csv(csv_file, delimiter=",")
#   daily_df.drop(daily_df[daily_df["成交价"] == 0.00].index, inplace = True)
  
#   print(daily_df)
#   fig1 = make_subplots(specs=[[{"secondary_y": True}]])
#   fig1.add_trace(go.Scatter(x=daily_df.index,y=daily_df['成交价'],name='Price'),secondary_y=False)
#   fig1.add_trace(go.Bar(x=daily_df.index,y=daily_df['成交量(手)'],name='成交量(手)'),secondary_y=True)
#   # fig1.update_yaxes(range=[0,7000000000],secondary_y=True)
#   # fig1.update_yaxes(visible=False, secondary_y=True)
#   fig1.show()

#   daily_df.hist(column="成交价").show()
#   os.chdir(cwd)

# def  correlation_analysis():
#   file_names = [...]  # 填写您的CSV文件路径和文件名列表

#   data_frames = []  # 存储每个CSV文件的数据帧

#   for file_name in file_names:
#       data = pd.read_csv(file_name)
#       data_frames.append(data)

#   correlation_matrix = pd.DataFrame()  # 存储相关性矩阵

#   for i in range(len(data_frames)):
#       for j in range(i+1, len(data_frames)):
#           df1 = data_frames[i]
#           df2 = data_frames[j]
          
#           # 计算两个数据帧之间的相关性（使用适当的方法，如Pearson相关系数）
#           correlation = df1.corrwith(df2)
          
#           # 将相关性结果存储到相关性矩阵中
#           correlation_matrix[f"{file_names[i]} - {file_names[j]}"] = correlation

#   # 创建热图
#   plt.figure(figsize=(10, 8))
#   sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)

#   # 添加标题和标签
#   plt.title("Correlation Matrix")
#   plt.xlabel("Files")
#   plt.ylabel("Files")

#   # 展示热图
#   plt.show()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-d", "--Date", help="Date")
  # parser.add_argument("-pd", "--PlotDaily", help="PlotDaily")
  
  today_time = datetime.today().strftime('%Y-%m-%d')  
  print(f"today_time: {today_time}")

  # today_time="2023-06-07"
  analysis_entropy(today_time)
  # draw_daily_line("sz002169","2023-06-02")

  # start_date = date(2023, 6, 2)
  # end_date = date(2023, 6, 13)
  # for single_date in daterange(start_date, end_date):
  #     daytime = single_date.strftime("%Y-%m-%d")
  #     print("daytime "+daytime)
  #     weekno = single_date.weekday()
      
  #     if weekno < 5:
  #         print("Today is a Weekday")
  #         analysis_entropy(daytime)
  #     else:  
  #         # 5 Sat, 6 Sun
  #         print("Today is a Weekend")   