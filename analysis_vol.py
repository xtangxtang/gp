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
from datetime import datetime
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def analysis_vol(today_time=""):
    dir_list = os.listdir("gp_daily")
    working_path = os.getcwd()
    os.chdir("gp_daily")
    
    col_names=["symbols"]

    volfile = f"analysis_volum/analysis_volum.csv"

    vol_df = pd.DataFrame(columns=col_names)
    vol_df.set_index("symbols")

    for symbol in dir_list:
      print(f"{symbol}")
      datefiles = os.listdir(symbol)
      os.chdir(symbol)
      for datef in datefiles:
        dataset = pd.read_csv(datef, delimiter=",")
        if dataset.empty:
          continue
        date = os.path.splitext(datef)[0]  
        if today_time != "" and date != today_time:    
          continue
        sliced_df = dataset.loc[:,["成交额(元)","性质"]]
        # print(sliced_df.head)
        group_zxj = dataset.groupby("性质").agg({'成交额(元)': ['sum']})
        print("group_zxj")
        print(group_zxj) 
        # cjbs_list =  np.array(list(group_zxj.iloc[:, 0]))
        # print("cjbs_list")
        # print(cjbs_list)

        net_buy = group_zxj.loc['买盘'] - group_zxj.loc['卖盘']
        net_buy = net_buy.values[0]
        print(f"net_buy: {net_buy}")
        exist_col_names = vol_df.columns.values.tolist()
        if (vol_df["symbols"] == symbol).any():
          if date in exist_col_names:
            vol_df.loc[vol_df["symbols"] == symbol, date] = net_buy
            print("0 entropy_df: ")
            print(vol_df)
          else:
            vol_df[date]=""
            vol_df.loc[vol_df["symbols"] == symbol, date] = net_buy
            print("1 entropy_df: ")
            print(vol_df)            
        else:
          if date in exist_col_names:
            vol_df.loc[len(vol_df)] = symbol
            vol_df.loc[vol_df["symbols"] == symbol, date] = net_buy
            print("2 entropy_df: ")
            print(vol_df)  
          else:
            vol_df.loc[len(vol_df)] = symbol
            vol_df[date]=""
            vol_df.loc[vol_df["symbols"] == symbol, date] = net_buy
            print("3 entropy_df: ")
            print(vol_df) 
        
      os.chdir("../")
    print("finally:") 
    print(vol_df)
    vol_df.set_index("symbols")

    os.chdir(working_path)
    pre_vol_df = pd.DataFrame(columns=col_names)
    if os.path.exists(volfile):
       print("volfile: " + volfile)
       pre_vol_df = pd.read_csv(volfile, delimiter=",")
       
    pre_vol_df = pre_vol_df.set_index("symbols")
    print("pre_vol_df:")
    print(pre_vol_df)
    vol_df = vol_df.set_index("symbols")
    vol_df = pd.concat([pre_vol_df,vol_df], axis=1).drop_duplicates()
    print(vol_df)
    vol_df.to_csv(working_path+"/analysis_volum/analysis_volum.csv", index_label="symbols")
    os.chdir(working_path)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--Date", help="Date")
    # parser.add_argument("-pd", "--PlotDaily", help="PlotDaily")

    # today_time = datetime.today().strftime('%Y-%m-%d')  
    # print(f"today_time: {today_time}")
    # daytime="2023-06-02"
    # analysis_vol(daytime)

    start_date = date(2023, 6, 2)
    end_date = date(2023, 6, 8)
    for single_date in daterange(start_date, end_date):
        daytime = single_date.strftime("%Y-%m-%d")
        print("daytime "+daytime)
        weekno = single_date.weekday()
        
        if weekno < 5:
            print("Today is a Weekday")
            analysis_vol(daytime)
        else:  
            # 5 Sat, 6 Sun
            print("Today is a Weekend")        

    