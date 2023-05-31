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
start_time = "09:25:00"

def get_daily(symbols, working_path):
    colnames=["成交时间", "成交价", "涨跌幅", "价格变动", "成交量(手)", "成交额(元)", "性质"] 
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/gp_daily")
    i = 0
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y_%-m_%-d')

    last_symbol = ""
    file_name = "logs/" + threading.current_thread().getName()    
    if os.path.isfile(file_name):
        with open(file_name) as f:
            last_symbol = f.readline().strip('\n')
    print(f"{file_name} last symbol {last_symbol}")    

    while (current_time < stop_time):
        if current_time <= start_time:
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)            
            continue
        for sysmbol in symbols:
            print("sysmbol: " + sysmbol)
            if last_symbol != "" and sysmbol < last_symbol:
                continue
            os.chdir(working_path + "/gp_daily/" + sysmbol)
            if os.path.exists(f"{today_time}.csv") == False :
                # f = open(f"{today_time}.csv", "w")
                total_detail_df = pd.DataFrame(columns=colnames)
                total_detail_df.to_csv(f"{today_time}.csv")
            else :
                try:
                    total_detail_df = pd.read_csv(f"{today_time}.csv", delimiter=",")
                except:
                    print(f"got exception while reading {sysmbol} csv file")
                    os.chdir(working_path)
                    continue                    
                total_detail_df = total_detail_df.set_index("成交时间") 
            try:
                url = f"https://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol={sysmbol}"
                html = requests.get(url, timeout=20).content
                df_tmp = pd.read_html(html)                
            except:
                print(f"got exception while reading {sysmbol} url")
                os.chdir(working_path)
                last_symbol = sysmbol
                # open(file_name, 'w').close()
                with open(file_name, 'w') as the_file:
                    the_file.write(f'{sysmbol}\n')
                exit(2)
            detail_df_tmp = df_tmp[3].set_index("成交时间")     
            total_detail_df = pd.concat([detail_df_tmp,total_detail_df]).drop_duplicates()
            total_detail_df.to_csv(f"{today_time}.csv")
            print(f"finish {sysmbol}")

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            # print("Current Time =", current_time)
            os.chdir(working_path) 
        # time.sleep(10)
        i = i + 1
    os.chdir(working_path)

def create_folder(symbols):
    for sysmbol in symbols:
        if not os.path.exists(f"gp_daily/{sysmbol}"):
            os.makedirs(f"gp_daily/{sysmbol}")

def divide_chunks(l, n):     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]                    


chunks_num =3
working_path = os.getcwd()
print(datetime.today().strftime('%Y_%-m_%-d'))
df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
symbols_zhuban = df_zhuban["A股代码"]
symbols_zhuban = list(symbols_zhuban)
# print(symbols_zhuban)
create_folder(symbols_zhuban)
symbols_zhuban_cks = list(divide_chunks(symbols_zhuban, int(len(symbols_zhuban)/chunks_num)))
symbols_zhuban_threads = []
for i in range(chunks_num):    
    t = threading.Thread(target=get_daily, args=(symbols_zhuban_cks[i], working_path, ))
    t.name = f"sh_zhuban_{i}"
    print(t.getName())
    symbols_zhuban_threads.append(t)


os.chdir(working_path)
df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
symbols_kcb = df_kcb["A股代码"]
symbols_kcb = list(symbols_kcb)
# print(symbols_kcb)
create_folder(symbols_kcb)
symbols_kcb_cks = list(divide_chunks(symbols_kcb, int(len(symbols_kcb)/chunks_num)))
symbols_kcb_threads = []
for i in range(chunks_num):
    t = threading.Thread(target=get_daily, args=(symbols_kcb_cks[i], working_path, ))
    t.name = f"sh_kcb_{i}"
    print(t.getName())    
    symbols_kcb_threads.append(t)


# th2 = threading.Thread(target=get_daily, args=(symbols_kcb, working_path, ))
# th2.start() 

os.chdir(working_path)
df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
symbols_sz = df_sz["A股代码"]
symbols_sz = list(symbols_sz)
# print(symbols_sz)
create_folder(symbols_sz)
symbols_sz_cks = list(divide_chunks(symbols_sz, int(len(symbols_sz)/chunks_num)))
symbols_sz_threads = []
for i in range(chunks_num):
    t = threading.Thread(target=get_daily, args=(symbols_sz_cks[i], working_path, ))
    t.name = f"sz_{i}"
    print(t.getName())  
    symbols_sz_threads.append(t)
# th3 = threading.Thread(target=get_daily, args=(symbols_sz, working_path, ))
# th3.start() 
for i in range(chunks_num):
    print("i " + str(i))
    symbols_zhuban_threads[i].start()
    os.chdir(working_path)
    symbols_kcb_threads[i].start()
    os.chdir(working_path)
    symbols_sz_threads[i].start()
    os.chdir(working_path)
    

for i in range(chunks_num):
    symbols_zhuban_threads[i].join()
    os.chdir(working_path)
    symbols_kcb_threads[i].join()
    os.chdir(working_path)
    symbols_sz_threads[i].join()
    os.chdir(working_path)

# th1.start() 
# os.chdir(working_path)
# th2.start() 
# os.chdir(working_path)
# th3.start() 
# os.chdir(working_path)
# th1.join()
# th2.join()
# th3.join()
# print(datetime.today().strftime('%Y_%-m_%-d'))
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)




