from bs4 import BeautifulSoup
import requests, json
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
import urllib.request as urllib2
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
import mechanize
from lxml.etree import fromstring
import json
import re
import numpy

      
# 添加前缀的函数
def add_prefix(column):
    if column.startswith('6'):
        return 'sh' + column
    elif column.startswith(('0', '3')):
        return 'sz' + column
    else:
        return column
    
def convert_chinese_number(value):
    pattern = r'([\d.]+)(亿|万)'
    match = re.search(pattern, value)
    if match:
        number = float(match.group(1))
        unit = match.group(2)
        if unit == '亿':
            return number * 100000000  # 亿对应的数值
        elif unit == '万':
            return number * 10000  # 万对应的数值
    try:
        ret = float(value)  # 转换为浮点型   
    except:
        ret = numpy.nan
    return ret

## 获得个股每天收盘数据
def get_daily(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/gp_daily")

    if 'TODAY' in os.environ:
        today_time = os.environ['TODAY']
        print(f"TODAY 环境变量的值为: {today_time}")
    else:
        print("TODAY 环境变量不存在")    
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        today_time = datetime.today().strftime('%Y-%m-%d')  

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/gp_daily/all/{today_time}-alldaily.csv"
    if os.path.exists(csv_file):
        print(f"{csv_file} exist, return")
        return
    
    page_range = range(1, 260)
    for pagenum in page_range:
        url = f"http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/{pagenum}/ajax/1/"
        from pyvirtualdisplay import Display
        from pyvirtualdisplay.xephyr import XephyrDisplay 
        display = Display(visible=0, size=(1920, 1080)) 
        # display = XephyrDisplay() 
        display.start()
        ua = UserAgent()
        userAgent = ua.chrome
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent={userAgent}')
        driver = webdriver.Chrome ('/usr/bin/chromedriver',options = chrome_options)
        driver.get(url)         

        html = driver.page_source
        time.sleep(2)
        table = pd.read_html(html)[0]

        table = table.drop(columns=['序号', '加自选'])
        table = table.astype({"代码": str})
        table['代码'] = table['代码'].str.zfill(6)     
        table['代码'] = table['代码'].apply(add_prefix)        
 
        table.set_index('代码',inplace=True)   

        columns_to_convert = ['成交额', '流通股', '流通市值']
        table[columns_to_convert] = table[columns_to_convert].applymap(convert_chinese_number)       

        captial_df = pd.concat([captial_df,table]).drop_duplicates()      
        print(captial_df.last)
        driver.close()
        display.stop()
        
    captial_df.to_csv(csv_file, encoding="utf-8")    
    print(captial_df)

if __name__ == "__main__":

    chunks_num =5
    working_path = os.getcwd()

    retry= 0
    while(retry != 20):
        try:
            print("===============================>get_daily")
            get_daily(working_path)
        except Exception:
            time.sleep(1)
            retry = retry + 1
        break

    

    

