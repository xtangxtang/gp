from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time
from datetime import datetime
import os
import pandas as pd
import threading

stop_time = "15:00:00"

def get_daily(symbols):
    # symbols=["sh688981","sz300491"]
    colnames=["成交时间", "成交价", "涨跌幅", "价格变动", "成交量(手)", "成交额(元)", "性质"] 
    i = 0
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    while (current_time < stop_time):
        for sysmbol in symbols:
            print("sysmbol: " + sysmbol)
            print("i " + str(i))
            if os.path.exists(f"{sysmbol}.csv") == False :
                f = open(f"{sysmbol}.csv", "w")
                total_detail_df = pd.DataFrame()
            else :
                total_detail_df = pd.read_csv(f"{sysmbol}.csv", delimiter=",")
                total_detail_df = total_detail_df.set_index("成交时间") 
            try:
                url = f"https://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol={sysmbol}"
                html = requests.get(url, timeout=10).content
                df_tmp = pd.read_html(html)
            except:
                print("got exception")
                continue
            detail_df_tmp = df_tmp[3].set_index("成交时间")     

            total_detail_df = pd.concat([detail_df_tmp,total_detail_df]).drop_duplicates()
            total_detail_df.to_csv(f"{sysmbol}.csv")

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time) 
        time.sleep(10)
        i = i + 1

def create_folder(symbols):
    for sysmbol in symbols:
        if not os.path.exists(f"gp_daily/{sysmbol}"):
            os.makedirs(sysmbol)


df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
symbols_zhuban = df_zhuban["A股代码"]
symbols_zhuban = list(symbols_zhuban)
# print(symbols_zhuban)
create_folder(symbols_zhuban)

df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
symbols_kcb = df_kcb["A股代码"]
symbols_kcb = list(symbols_kcb)
# print(symbols_kcb)
create_folder(symbols_kcb)

df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
symbols_sz = df_sz["A股代码"]
symbols_sz = list(symbols_sz)
# print(symbols_sz)
create_folder(symbols_sz)

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)




