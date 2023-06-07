from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time
from datetime import datetime
import os
import pandas as pd
import threading
from selenium import webdriver
import argparse
from fake_useragent import UserAgent
import shutil

def get_daily(symbols, working_path, __time=""):
    colnames=["成交时间", "成交价", "涨跌幅", "价格变动", "成交量(手)", "成交额(元)", "性质"] 
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/gp_daily")

    if __time == "":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        today_time = datetime.today().strftime('%Y-%m-%d')  
    else:
        today_time = __time

    print(f"today: {today_time}")
    throttle = 2
    for sysmbol in symbols:
        print("sysmbol: " + sysmbol)
        time.sleep(throttle)
        csv_dir = f"{working_path}/gp_daily/{sysmbol}"
        if os.path.exists(csv_dir) == False:
            os.mkdir(csv_dir)
        os.chdir(csv_dir)
        csv_file = f"{csv_dir}/{today_time}.csv"
        if os.path.exists(csv_file):
            tmp_df = pd.read_csv(csv_file, delimiter=",")
            if not tmp_df.empty :
                last_row = tmp_df.iloc[-1]
                print(f"{sysmbol} {today_time}.csv" + last_row["成交时间"] )
                if last_row["成交时间"] < "15:00:00":
                    # exit(2)
                    print(csv_file + last_row["成交时间"] + " is not 15:00:00, remove file" )
                    os.remove(csv_file)                
                else:
                    continue
            else:
                os.remove(csv_file)
            # try:
            #     total_detail_df = pd.read_csv(f"{today_time}.csv", delimiter=",")
            # except:
            #     print(f"got exception while reading {sysmbol} csv file")
            #     os.chdir(working_path)
            #     continue   
        total_detail_df = pd.DataFrame(columns=colnames)
        total_detail_df.to_csv(csv_file)                 
        total_detail_df = total_detail_df.set_index("成交时间")
        retry = 0        
        page_range = range(100, 0, -1)        
        for i in page_range:
            url = f"http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol={sysmbol}&date={today_time}&page={i}"
            while True:
                try: 
                    ua=UserAgent()
                    # print('User-Agent :' + ua.random)
                    hdr = {'User-Agent': ua.random,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive'}                    
                    html=requests.get(url, timeout=20, headers=hdr).content 
                except Exception as e:
                    print(f"got exception while reading {sysmbol} url" + str(e))
                    if retry < 3:
                        retry = retry + 1
                        time.sleep(5)
                        continue
                    else:
                        break 
                break               
            try:                        
                df_tmp = pd.read_html(html)
                # print(df_tmp)
                if (df_tmp[3]['成交时间'].eq('该股票没有交易数据')).any():
                    print("retry index " + str(i))
                    continue
                print(df_tmp[3])              

                # open(file_name, 'w').close()
                detail_df_tmp = df_tmp[3].set_index("成交时间")     
                total_detail_df = pd.concat([detail_df_tmp,total_detail_df]).drop_duplicates()
            except Exception as e:
                print(f"got exception while looping {sysmbol}: " + str(e))
                print(df_tmp)
                # exit(0)
                time.sleep(15)
                continue
        total_detail_df = total_detail_df.iloc[::-1]
        total_detail_df.to_csv(csv_file)
        print(f"finish {sysmbol}")        

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        os.chdir(working_path)
        # time.sleep(10)
    os.chdir(working_path)

def create_folder(symbols):
    for sysmbol in symbols:
        if not os.path.exists(f"gp_daily/{sysmbol}"):
            os.makedirs(f"gp_daily/{sysmbol}")

def rename_file():
    dir_list = os.listdir("gp_daily")
    cwd = os.getcwd()
    os.chdir("gp_daily")
    for symb_dir in dir_list:
        os.chdir(symb_dir)
        if os.path.exists("2023-6-2.csv"):
            os.rename("2023-6-2.csv", "2023-06-02.csv")
        os.chdir("../")
    os.chdir(cwd)    

def remove_files_not_self_list(self_gplist):
    dir_list = os.listdir("gp_daily")
    cwd = os.getcwd()
    os.chdir("gp_daily")
    for file in dir_list:
        if file in self_gplist:            
            continue
        else:
            if os.path.exists(file):
                shutil.rmtree(file)
                print("remove :" + file)    

    os.chdir(cwd)

def divide_chunks(l, n):     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]                    



if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-m", "--MultipleThreads", help="MultipleThreads")
    # parser.add_argument("-s", "--StockType", help="StockType")

    chunks_num =5
    working_path = os.getcwd()
    # args = parser.parse_args()

    # MultipleThreads = int(args.MultipleThreads)
    # StockType = int(args.StockType)

    # print(f"MultipleThreads: {MultipleThreads}")
    # print(f"StockType: {StockType}")

    # now = datetime.now()
    # # current_time = now.strftime("%H:%M:%S")
    # # print("Current Time =", current_time)
    # today_time = datetime.today().strftime('%Y-%-m-%-d')      
    # # today_time = "2022-06-01"


    # print(datetime.today().strftime('%Y_%-m_%-d'))
    # df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
    # df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
    # symbols_zhuban = df_zhuban["A股代码"]
    # symbols_zhuban = list(symbols_zhuban)
    # # print(symbols_zhuban)
    # create_folder(symbols_zhuban)

    # df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
    # df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
    # symbols_kcb = df_kcb["A股代码"]
    # symbols_kcb = list(symbols_kcb)
    # # print(symbols_kcb)
    # create_folder(symbols_kcb)  

    # df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
    # df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
    # symbols_sz = df_sz["A股代码"]
    # symbols_sz = list(symbols_sz)
    # # print(symbols_sz)
    # create_folder(symbols_sz)

    # self_gplist = symbols_zhuban + symbols_kcb + symbols_sz
    # rename_file()
    # exit(0)
    self_gplist = ["sz300491", "sh688316", "sh605358", "sh603348", "sh688981",
                    "sh688008", "sh688123", "sh688146", "sh688268", "sz300236",
                    "sh688208", "sz300693", "sz001314", "sz002169", "sh688663", 
                    "sh688170", "sh688137", "sz300842", "sh688293", "sh688305", 
                    "sz300484", "sh688255", "sz300706", "sh688126", "sh688503", 
                    "sh688063", "sz300568", "sh688390", "sh688041", "sz300751",
                    "sh688256", "sz300415", "sz300428", "sh603290", "sh603986", 
                    "sh688158", "sh603881", "sz300346", "sh603650", "sh688012",
                    "sz300001"]
    
    # chunks_num =5
    remove_files_not_self_list(self_gplist)

    today_time = ""
    self_gplist_cks = list(divide_chunks(self_gplist, int(len(self_gplist)/chunks_num)))
    self_gplist_threads = []
    for i in range(chunks_num):    
        t = threading.Thread(target=get_daily, args=(self_gplist_cks[i], working_path, today_time))
        t.name = f"sh_zhuban_{i}"
        print(t.getName())
        self_gplist_threads.append(t)

    for i in range(chunks_num):
        print("i " + str(i))
        self_gplist_threads[i].start()
        os.chdir(working_path)
        
    for i in range(chunks_num):
        self_gplist_threads[i].join()
        os.chdir(working_path)  

    get_daily(self_gplist, working_path, "")

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-m", "--MultipleThreads", help="MultipleThreads")
    # parser.add_argument("-s", "--StockType", help="StockType")

    # chunks_num =3
    # working_path = os.getcwd()
    # args = parser.parse_args()

    # MultipleThreads = int(args.MultipleThreads)
    # StockType = int(args.StockType)

    # print(f"MultipleThreads: {MultipleThreads}")
    # print(f"StockType: {StockType}")

    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    # # today_time = datetime.today().strftime('%Y-%-m-%-d')      
    # today_time = "2022-06-01"

    # if MultipleThreads != 1:
    #     # get_daily(["sz300491"], working_path, "2023-05-30")
    #     if StockType == 1:
    #         print(datetime.today().strftime('%Y_%-m_%-d'))
    #         df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
    #         df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
    #         symbols_zhuban = df_zhuban["A股代码"]
    #         symbols_zhuban = list(symbols_zhuban)
    #         print(symbols_zhuban)
    #         create_folder(symbols_zhuban)
    #         get_daily(symbols_zhuban, working_path, today_time)
    #     elif StockType == 2:
    #         os.chdir(working_path)
    #         df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
    #         df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
    #         symbols_kcb = df_kcb["A股代码"]
    #         symbols_kcb = list(symbols_kcb)
    #         # print(symbols_kcb)
    #         create_folder(symbols_kcb)
    #         get_daily(symbols_kcb, working_path, today_time)
    #     elif StockType == 3:
    #         os.chdir(working_path)
    #         df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
    #         df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
    #         symbols_sz = df_sz["A股代码"]
    #         symbols_sz = list(symbols_sz)
    #         # print(symbols_sz)
    #         create_folder(symbols_sz)
    #         get_daily(symbols_sz, working_path, today_time)
    # else:
    #     if StockType == 1:
    #         working_path = os.getcwd()
    #         print(datetime.today().strftime('%Y_%-m_%-d'))
    #         df_zhuban = pd.read_excel('gp_list/sh_zhuban.xls')
    #         df_zhuban['A股代码'] = 'sh' + df_zhuban['A股代码'].astype(str)
    #         symbols_zhuban = df_zhuban["A股代码"]
    #         symbols_zhuban = list(symbols_zhuban)
    #         # print(symbols_zhuban)
    #         create_folder(symbols_zhuban)
    #         symbols_zhuban_cks = list(divide_chunks(symbols_zhuban, int(len(symbols_zhuban)/chunks_num)))
    #         symbols_zhuban_threads = []
    #         for i in range(chunks_num):    
    #             t = threading.Thread(target=get_daily, args=(symbols_zhuban_cks[i], working_path, today_time))
    #             t.name = f"sh_zhuban_{i}"
    #             print(t.getName())
    #             symbols_zhuban_threads.append(t)

    #         for i in range(chunks_num):
    #             print("i " + str(i))
    #             symbols_zhuban_threads[i].start()
    #             os.chdir(working_path)
                
    #         for i in range(chunks_num):
    #             symbols_zhuban_threads[i].join()
    #             os.chdir(working_path)
    #     elif StockType == 2:
    #         os.chdir(working_path)
    #         df_kcb = pd.read_excel('gp_list/sh_kcb.xls')
    #         df_kcb['A股代码'] = 'sh' + df_kcb['A股代码'].astype(str)
    #         symbols_kcb = df_kcb["A股代码"]
    #         symbols_kcb = list(symbols_kcb)
    #         # print(symbols_kcb)
    #         create_folder(symbols_kcb)
    #         symbols_kcb_cks = list(divide_chunks(symbols_kcb, int(len(symbols_kcb)/chunks_num)))
    #         symbols_kcb_threads = []
    #         for i in range(chunks_num):
    #             t = threading.Thread(target=get_daily, args=(symbols_kcb_cks[i], working_path, today_time))
    #             t.name = f"sh_kcb_{i}"
    #             print(t.getName())    
    #             symbols_kcb_threads.append(t)

    #         for i in range(chunks_num):
    #             print("i " + str(i))
    #             symbols_kcb_threads[i].start()
    #             os.chdir(working_path) 

    #         for i in range(chunks_num):
    #             symbols_kcb_threads[i].join()
    #             os.chdir(working_path)
    #     elif StockType == 3:
    #         os.chdir(working_path)
    #         df_sz = pd.read_excel('gp_list/sz.xlsx',converters={'A股代码':str})
    #         df_sz['A股代码'] = 'sz' + df_sz['A股代码'].astype(str)
    #         symbols_sz = df_sz["A股代码"]
    #         symbols_sz = list(symbols_sz)
    #         # print(symbols_sz)
    #         create_folder(symbols_sz)
    #         symbols_sz_cks = list(divide_chunks(symbols_sz, int(len(symbols_sz)/chunks_num)))
    #         symbols_sz_threads = []
    #         for i in range(chunks_num):
    #             t = threading.Thread(target=get_daily, args=(symbols_sz_cks[i], working_path, today_time))
    #             t.name = f"sz_{i}"
    #             print(t.getName())  
    #             symbols_sz_threads.append(t)
    #         # th3 = threading.Thread(target=get_daily, args=(symbols_sz, working_path, ))
    #         # th3.start() 
    #         for i in range(chunks_num):
    #             print("i " + str(i))
    #             symbols_sz_threads[i].start()
    #             os.chdir(working_path)
                

    #         for i in range(chunks_num):
    #             symbols_sz_threads[i].join()
    #             os.chdir(working_path)






