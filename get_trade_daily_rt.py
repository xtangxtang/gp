from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time
from datetime import datetime
import os
import pandas as pd
import threading
import argparse, random
from fake_useragent import UserAgent

stop_time = "15:00:00"
start_time = "09:15:00"

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]



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
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")         
        if current_time <= start_time:
            current_time = now.strftime("%H:%M:%S")
            print("Current Time =", current_time)            
            continue
        # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        whoa = 450
        throttle = 10
        for sysmbol in symbols:
            time.sleep(throttle)
            print("sysmbol: " + sysmbol)
            csv_dir = f"{working_path}/gp_daily/{sysmbol}"
            os.chdir(csv_dir)
            csv_file = f"{csv_dir}/{today_time}.csv"            
            # if last_symbol != "" and sysmbol < last_symbol:
            #     continue
            # os.chdir(working_path + "/gp_daily/" + sysmbol)
            if os.path.exists(csv_file) == False :
                # f = open(f"{today_time}.csv", "w")
                total_detail_df = pd.DataFrame(columns=colnames)
                total_detail_df.to_csv(csv_file)
            else :
                try:
                    total_detail_df = pd.read_csv(csv_file, delimiter=",")
                except:
                    print(f"got exception while reading {sysmbol} csv file")
                    continue                  
            total_detail_df = total_detail_df.set_index("成交时间")
            retry = 0  
            url = f"http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol={sysmbol}"
            while True:
                try: 
                    # html = requests.get(url, timeout=20, headers=headers).content
                    ua=UserAgent()
                    # print('User-Agent :' + ua.random)
                    hdr = {'User-Agent': ua.random,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}                    
                    response=requests.get(url, timeout=20, headers=hdr)
                    while response.status_code == 429:
                        print(response.content)
                        print(response.headers)
                        time.sleep(whoa)
                        response=requests.get(url)
                    html = response.content                  
                except Exception as e:
                    print(f"got exception while reading {sysmbol} url" + str(e))
                    if retry < 3:
                        retry = retry + 1
                        continue
                    else:
                        break
                break
            # df_tmp = pd.DataFrame(columns=colnames)
            try:
                df_tmp = pd.read_html(html) 
                detail_df_tmp = df_tmp[3].set_index("成交时间")                
            except Exception as e:
                print(f"got exception while looping {sysmbol}: " + str(e))
                # print(df_tmp)
                # exit(0)
                time.sleep(15)
                continue 
            total_detail_df = pd.concat([detail_df_tmp,total_detail_df]).drop_duplicates()
            total_detail_df.to_csv(csv_file)
            print(f"finish {sysmbol}")
           
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--MultipleThreads", help="MultipleThreads")
    parser.add_argument("-s", "--StockType", help="StockType")

    chunks_num =50
    working_path = os.getcwd()
    args = parser.parse_args()

    MultipleThreads = int(args.MultipleThreads)
    StockType = int(args.StockType)

    print(f"MultipleThreads: {MultipleThreads}")
    print(f"StockType: {StockType}")

    now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%-m-%-d')      
    # today_time = "2022-06-01"


    print(datetime.today().strftime('%Y_%-m_%-d'))
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

    df_gplist = symbols_zhuban + symbols_kcb + symbols_sz

    df_gplist_cks = list(divide_chunks(df_gplist, int(len(symbols_zhuban)/chunks_num)))
    df_gplist_threads = []
    for i in range(chunks_num):    
        t = threading.Thread(target=get_daily, args=(df_gplist_cks[i], working_path))
        t.name = f"sh_zhuban_{i}"
        print(t.getName())
        df_gplist_threads.append(t)

    for i in range(chunks_num):
        print("i " + str(i))
        df_gplist_threads[i].start()
        os.chdir(working_path)
        
    for i in range(chunks_num):
        df_gplist_threads[i].join()
        os.chdir(working_path)    

#     if MultipleThreads != 1:
#         # get_daily(["sz300491"], working_path, "2023-05-30")
#         if StockType == 1:
#             print(datetime.today().strftime('%Y_%-m_%-d'))
#             df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
#             df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
#             symbols_zhuban = df_zhuban["A股代码"]
#             symbols_zhuban = list(symbols_zhuban)
#             print(symbols_zhuban)
#             create_folder(symbols_zhuban)
#             get_daily(symbols_zhuban, working_path)
#         elif StockType == 2:
#             os.chdir(working_path)
#             df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
#             df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
#             symbols_kcb = df_kcb["A股代码"]
#             symbols_kcb = list(symbols_kcb)
#             # print(symbols_kcb)
#             create_folder(symbols_kcb)
#             get_daily(symbols_kcb, working_path)
#         elif StockType == 3:
#             os.chdir(working_path)
#             df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
#             df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
#             symbols_sz = df_sz["A股代码"]
#             symbols_sz = list(symbols_sz)
#             # print(symbols_sz)
#             create_folder(symbols_sz)
#             get_daily(symbols_sz, working_path)
#     else:
#         if StockType == 1:
#             working_path = os.getcwd()
#             print(datetime.today().strftime('%Y_%-m_%-d'))
#             df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
#             df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
#             symbols_zhuban = df_zhuban["A股代码"]
#             symbols_zhuban = list(symbols_zhuban)
#             # print(symbols_zhuban)
#             create_folder(symbols_zhuban)
#             symbols_zhuban_cks = list(divide_chunks(symbols_zhuban, int(len(symbols_zhuban)/chunks_num)))
#             symbols_zhuban_threads = []
#             for i in range(chunks_num):    
#                 t = threading.Thread(target=get_daily, args=(symbols_zhuban_cks[i], working_path))
#                 t.name = f"sh_zhuban_{i}"
#                 print(t.getName())
#                 symbols_zhuban_threads.append(t)

#             for i in range(chunks_num):
#                 print("i " + str(i))
#                 symbols_zhuban_threads[i].start()
#                 os.chdir(working_path)
                
#             for i in range(chunks_num):
#                 symbols_zhuban_threads[i].join()
#                 os.chdir(working_path)
#         elif StockType == 2:
#             os.chdir(working_path)
#             df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
#             df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
#             symbols_kcb = df_kcb["A股代码"]
#             symbols_kcb = list(symbols_kcb)
#             # print(symbols_kcb)
#             create_folder(symbols_kcb)
#             symbols_kcb_cks = list(divide_chunks(symbols_kcb, int(len(symbols_kcb)/chunks_num)))
#             symbols_kcb_threads = []
#             for i in range(chunks_num):
#                 t = threading.Thread(target=get_daily, args=(symbols_kcb_cks[i], working_path))
#                 t.name = f"sh_kcb_{i}"
#                 print(t.getName())    
#                 symbols_kcb_threads.append(t)

#             for i in range(chunks_num):
#                 print("i " + str(i))
#                 symbols_kcb_threads[i].start()
#                 os.chdir(working_path) 

#             for i in range(chunks_num):
#                 symbols_kcb_threads[i].join()
#                 os.chdir(working_path)
#         elif StockType == 3:
#             os.chdir(working_path)
#             df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
#             df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
#             symbols_sz = df_sz["A股代码"]
#             symbols_sz = list(symbols_sz)
#             # print(symbols_sz)
#             create_folder(symbols_sz)
#             symbols_sz_cks = list(divide_chunks(symbols_sz, int(len(symbols_sz)/chunks_num)))
#             symbols_sz_threads = []
#             for i in range(chunks_num):
#                 t = threading.Thread(target=get_daily, args=(symbols_sz_cks[i], working_path))
#                 t.name = f"sz_{i}"
#                 print(t.getName())  
#                 symbols_sz_threads.append(t)
#             # th3 = threading.Thread(target=get_daily, args=(symbols_sz, working_path, ))
#             # th3.start() 
#             for i in range(chunks_num):
#                 print("i " + str(i))
#                 symbols_sz_threads[i].start()
#                 os.chdir(working_path)
                

#             for i in range(chunks_num):
#                 symbols_sz_threads[i].join()
#                 os.chdir(working_path)



# # chunks_num =10
# # working_path = os.getcwd()
# # print(datetime.today().strftime('%Y_%-m_%-d'))
# # df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
# # df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
# # symbols_zhuban = df_zhuban["A股代码"]
# # symbols_zhuban = list(symbols_zhuban)
# # # print(symbols_zhuban)
# # create_folder(symbols_zhuban)
# # symbols_zhuban_cks = list(divide_chunks(symbols_zhuban, int(len(symbols_zhuban)/chunks_num)))
# # symbols_zhuban_threads = []
# # for i in range(chunks_num):    
# #     t = threading.Thread(target=get_daily, args=(symbols_zhuban_cks[i], working_path, ))
# #     t.name = f"sh_zhuban_{i}"
# #     print(t.getName())
# #     symbols_zhuban_threads.append(t)


# # os.chdir(working_path)
# # df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
# # df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
# # symbols_kcb = df_kcb["A股代码"]
# # symbols_kcb = list(symbols_kcb)
# # # print(symbols_kcb)
# # create_folder(symbols_kcb)
# # symbols_kcb_cks = list(divide_chunks(symbols_kcb, int(len(symbols_kcb)/chunks_num)))
# # symbols_kcb_threads = []
# # for i in range(chunks_num):
# #     t = threading.Thread(target=get_daily, args=(symbols_kcb_cks[i], working_path, ))
# #     t.name = f"sh_kcb_{i}"
# #     print(t.getName())    
# #     symbols_kcb_threads.append(t)


# # # th2 = threading.Thread(target=get_daily, args=(symbols_kcb, working_path, ))
# # # th2.start() 

# # os.chdir(working_path)
# # df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
# # df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
# # symbols_sz = df_sz["A股代码"]
# # symbols_sz = list(symbols_sz)
# # # print(symbols_sz)
# # create_folder(symbols_sz)
# # symbols_sz_cks = list(divide_chunks(symbols_sz, int(len(symbols_sz)/chunks_num)))
# # symbols_sz_threads = []
# # for i in range(chunks_num):
# #     t = threading.Thread(target=get_daily, args=(symbols_sz_cks[i], working_path, ))
# #     t.name = f"sz_{i}"
# #     print(t.getName())  
# #     symbols_sz_threads.append(t)
# # # th3 = threading.Thread(target=get_daily, args=(symbols_sz, working_path, ))
# # # th3.start() 
# # for i in range(chunks_num):
# #     print("i " + str(i))
# #     symbols_zhuban_threads[i].start()
# #     os.chdir(working_path)
# #     symbols_kcb_threads[i].start()
# #     os.chdir(working_path)
# #     symbols_sz_threads[i].start()
# #     os.chdir(working_path)
    

# # for i in range(chunks_num):
# #     symbols_zhuban_threads[i].join()
# #     os.chdir(working_path)
# #     symbols_kcb_threads[i].join()
# #     os.chdir(working_path)
# #     symbols_sz_threads[i].join()
# #     os.chdir(working_path)





