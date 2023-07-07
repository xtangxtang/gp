from bs4 import BeautifulSoup
import requests, json
import csv
import pandas as pd
import time
from datetime import datetime, timedelta
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
    return float(value)  # 转换为浮点型   

## 获得个股主力资金
def get_daily_gg(working_path):
    # url = "http://data.eastmoney.com/zjlx/detail.html"
    # url = "https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0"
    # url = "http://q.10jqka.com.cn/"

    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/capital/gg/{today_time}-gg.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    
    page_range = range(1, 104)
    for pagenum in page_range:
        url = f"http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery11230782769932894602_1686965932465&fid=f62&po=1&pz=50&pn={pagenum}&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A0%2Bt%3A6%2Bf%3A!2%2Cm%3A0%2Bt%3A13%2Bf%3A!2%2Cm%3A0%2Bt%3A80%2Bf%3A!2%2Cm%3A1%2Bt%3A2%2Bf%3A!2%2Cm%3A1%2Bt%3A23%2Bf%3A!2%2Cm%3A0%2Bt%3A7%2Bf%3A!2%2Cm%3A1%2Bt%3A3%2Bf%3A!2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
        ua=UserAgent()
        # print('User-Agent :' + ua.random)
        hdr = {'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}                    
        html_json=requests.get(url, timeout=20, headers=hdr).content
        html_json = str(html_json,encoding="utf8")
        # print(html)
        # html_json = "xxxx[符号之前的所有字符去掉"
        index = html_json.find('[')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[index:]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串

        index = html_json.find(']')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[:index+1]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串        
        # print(html_json)    
        table = pd.read_json(html_json, dtype={'f12': str})
        table = table.drop(columns=['f1','f204','f205','f206'])


        # 对索引列应用函数
        table['f12'] = table['f12'].apply(add_prefix)

        table.set_index('f12',inplace=True)
        table.index.name = '代码'
        column_names=['最新价','今日涨跌幅','UNKNOWN','名称','今日主力净流入(净额)','今日超大单净流入(净额)',
                      '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
                      '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)','今日小单净流入(净占比)',
                      'UNKOWN2', '今日主力净流入(净占比)']
        table.columns=column_names
        new_cols = ['名称','最新价','今日涨跌幅','今日主力净流入(净额)','今日主力净流入(净占比)','今日超大单净流入(净额)',
                      '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
                      '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)','今日小单净流入(净占比)',
                      'UNKOWN2', 'UNKNOWN']
        table=table[new_cols]
        captial_df = pd.concat([captial_df,table]).drop_duplicates()

        print(captial_df.last)
    # captial_df.index = captial_df.index.astype("str")
    # captial_df.index = captial_df['代码'].astype('str')
    captial_df.reset_index()
    captial_df.to_csv(csv_file, encoding="utf-8")

## 获得板块主力资金
def get_daily_bk(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/capital/bk/{today_time}-bk.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    
    page_range = range(1, 3)
    for pagenum in page_range:
        url = f"http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112302932912477603822_1687050151034&fid=f62&po=1&pz=50&pn={pagenum}&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A2&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
        ua=UserAgent()
        # print('User-Agent :' + ua.random)
        hdr = {'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}                    
        html_json=requests.get(url, timeout=20, headers=hdr).content
        html_json = str(html_json,encoding="utf8")
        # print(html)
        # html_json = "xxxx[符号之前的所有字符去掉"
        index = html_json.find('[')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[index:]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串

        index = html_json.find(']')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[:index+1]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串        
        # print(html_json)    
        table = pd.read_json(html_json)
        table = table.drop(columns=['f1','f13','f124', 'f204','f205','f206'])

        table.set_index('f12',inplace=True)
        table.index.name = '代码'
        column_names=['最新价','今日涨跌幅','名称','今日主力净流入(净额)','今日超大单净流入(净额)',
                      '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
                      '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)',
                      '今日小单净流入(净占比)','今日主力净流入(净占比)']
        table.columns=column_names
        new_cols = ['名称','最新价','今日涨跌幅','今日主力净流入(净额)','今日主力净流入(净占比)','今日超大单净流入(净额)',
                      '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
                      '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)','今日小单净流入(净占比)']
        table=table[new_cols]
        captial_df = pd.concat([captial_df,table]).drop_duplicates()

        print(captial_df.last)
    # captial_df.index = captial_df.index.astype("str")
    # captial_df.index = captial_df['代码'].astype('str')
    captial_df.reset_index()
    captial_df.to_csv(csv_file, encoding="utf-8")    

## 获得概念主力资金
def get_daily_gn(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/capital/gn/{today_time}-gn.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    
    page_range = range(1, 10)
    for pagenum in page_range:
        url = f"http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery1123040653573332124626_1687052636278&fid=f62&po=1&pz=50&pn={pagenum}&np=1&fltt=2&invt=2&ut=b2884a393a59ad64002292a3e90d46a5&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
        ua=UserAgent()
        # print('User-Agent :' + ua.random)
        hdr = {'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}                    
        html_json=requests.get(url, timeout=20, headers=hdr).content
        html_json = str(html_json,encoding="utf8")
        # print(html)
        # html_json = "xxxx[符号之前的所有字符去掉"
        index = html_json.find('[')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[index:]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串

        index = html_json.find(']')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[:index+1]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串        
        # print(html_json)    
        table = pd.read_json(html_json)
        table = table.drop(columns=['f1','f13','f124', 'f204','f205','f206'])
        table.set_index('f12',inplace=True)
        table.index.name = '代码'
        column_names=['最新价','今日涨跌幅','名称','今日主力净流入(净额)','今日超大单净流入(净额)',
                      '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
                      '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)',
                      '今日小单净流入(净占比)','今日主力净流入(净占比)']
        table.columns=column_names
        new_cols = ['名称','最新价','今日涨跌幅','今日主力净流入(净额)','今日主力净流入(净占比)','今日超大单净流入(净额)',
                      '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
                      '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)','今日小单净流入(净占比)']
        table=table[new_cols]
        captial_df = pd.concat([captial_df,table]).drop_duplicates()

        print(captial_df.last)
    # captial_df.index = captial_df.index.astype("str")
    # captial_df.index = captial_df['代码'].astype('str')
    captial_df.reset_index()
    captial_df.to_csv(csv_file, encoding="utf-8")    

def get_all_captial(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")   

    colnames=["日期", "上证收盘价", "上证涨跌幅", "深证收盘价", "深证涨跌幅", "主力净流入净额", "主力净流入净占比", 
                "超大单净流入净额", "超大单净流入净占比", "大单净流入净额", "大单净流入净占比", "中单净流入净额", "中单净流入净占比", 
                "小单净流入净额", "小单净流入净占比"]    

    url = f"http://data.eastmoney.com/zjlx/dpzjlx.html"
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
    # print(pd.read_html(html))
    time.sleep(5)
    # table = pd.read_html(html)[0]
    # print(table) 
    # table = pd.read_html(html)[1]
    # print(table)   
    table = pd.read_html(html)[2]    
    table.columns=colnames
    table.set_index(["日期"], inplace=True)

    csv_file = f"{working_path}/capital/all/all-capital.csv"
    if os.path.exists(csv_file):
        captial_df = pd.read_csv(csv_file, index_col="日期")
        captial_df = pd.concat([table, captial_df]).drop_duplicates()          
    else:
        captial_df = table
    
    print(captial_df)
    captial_df.to_csv(csv_file, encoding="utf-8")
    driver.close()
    display.stop()

def get_north_hy_capital(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")

    now = datetime.now()
    
    # current_time = yesterday.strftime("%H:%M:%S")
    
    date_time = datetime.today()
    date_time = date_time - timedelta(days=1)
    date_time = date_time.strftime('%Y-%m-%d')
    # date_time = "2023-07-05"
    print("Current Time =", date_time)

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/capital/north/{date_time}-north-hy.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)

    page_range = range(1, 3)
    for pagenum in page_range:
        url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112308415029166620654_1687959194413&sortColumns=ADD_MARKET_CAP&sortTypes=-1&pageSize=50&pageNumber={pagenum}&reportName=RPT_MUTUAL_BOARD_HOLDRANK_WEB&columns=ALL&quoteColumns=f3~05~SECURITY_CODE~INDEX_CHANGE_RATIO&quoteType=0&source=WEB&client=WEB&filter=(BOARD_TYPE%3D%225%22)(TRADE_DATE%3D%27{date_time}%27)(INTERVAL_TYPE%3D%221%22)"
        ua=UserAgent()
        # print('User-Agent :' + ua.random)
        hdr = {'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}                    
        html_json=requests.get(url, timeout=20, headers=hdr).content
        html_json = str(html_json,encoding="utf8")
        # print(html)
        # html_json = "xxxx[符号之前的所有字符去掉"
        index = html_json.find('[')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[index:]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串

        index = html_json.find(']')  # 查找 '[' 符号的索引位置
        if index != -1:
            html_json = html_json[:index+1]  # 获取 '[' 之后的所有字符
        else:
            html_json = html_json  # 如果字符串中没有 '[' 符号，则结果为原字符串        

        table = pd.read_json(html_json)
        table = table.drop(columns=['BOARD_INNER_CODE',
                                    'BOARD_TYPE', 
                                    'ORIG_BOARD_CODE',
                                    'INTERVAL_TYPE',
                                    'MAXADD_SECUCODE',
                                    'MINADD_SECUCODE',
                                    'MAXADD_RATIO_SECUCODE',
                                    'MINADD_RATIO_SECUCODE',
                                    'IS_NEW',
                                    'SECURITY_CODE',
                                    'MAXHOLD_MARKETCAP_NAME',
                                    'MAXHOLD_MARKETCAP_SECUCODE'
                                    ])        
        # table.set_index('f12',inplace=True)        
        column_names=['行业代码',
                      '行业名称',
                      '涨跌幅%',
                      '日期',
                      '北向资金今日新增持股个数',
                      '北向资金今日总持股个数',
                      '北向资金今日新增市值',
                      '北向资金今日新增市值增幅%',
                      '行业总市值',
                      '北向资金今日买入该行业占今日行业资金比',
                      '北向资金今日买入该行业占北向资金比',
                      '北向累计今日总买入市值',
                      '北向累计今日总买入市值占累计北向资金比',
                      '北向累计今日总持股市值占板块市值比',
                      '北向今日增持最大市值股代码',
                      '北向今日增持最大市值股名称',
                      '北向今日减持最大市值股代码',
                      '北向今日减持最大市值股名称',
                      '北向今日增持最大比例股名称',
                      '北向今日增持最大比例股代码',
                      '北向今日减持最大比例股代码',
                      '北向今日减持最大比例股名称',
                      '北向累计持股市值最大股代码',]
        table.columns=column_names
        table.set_index("行业代码", inplace=True)
        # new_cols = ['名称',
        #             '最新价',
        #             '今日涨跌幅'd'今日主力净流入(净额)','今日主力净流入(净占比)','今日超大单净流入(净额)',
        #                 '今日超大单净流入(净占比)','今日大单净流入(净额)','今日大单净流入(净占比)',
        #                 '今日中单净流入(净额)', '今日中单净流入(净占比)','今日小单净流入(净额)','今日小单净流入(净占比)']
        # table=table[new_cols]
        captial_df = pd.concat([captial_df, table]).drop_duplicates()

        print(captial_df.last)
    # captial_df.index = captial_df.index.astype("str")
    # captial_df.index = captial_df['代码'].astype('str')
    # captial_df.reset_index()
    captial_df.to_csv(csv_file, encoding="utf-8", index="行业代码")        

# def get_north_hy_captial(working_path):
#     os.chdir(working_path)
#     print("working_path " + working_path)
#     os.chdir(working_path + "/capital")   

#     # colnames=["日期", "上证收盘价", "上证涨跌幅", "深证收盘价", "深证涨跌幅", "主力净流入净额", "主力净流入净占比", 
#     #             "超大单净流入净额", "超大单净流入净占比", "大单净流入净额", "大单净流入净占比", "中单净流入净额", "中单净流入净占比", 
#     #             "小单净流入净额", "小单净流入净占比"]    

#     url = f"https://data.eastmoney.com/hsgtcg/hy.html"
#     from pyvirtualdisplay import Display
#     from pyvirtualdisplay.xephyr import XephyrDisplay 
#     display = Display(visible=0, size=(1920, 1080)) 
#     # display = XephyrDisplay() 
#     display.start()
#     ua = UserAgent()
#     userAgent = ua.chrome
#     chrome_options = Options()
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument(f'user-agent={userAgent}')
#     driver = webdriver.Chrome ('/usr/bin/chromedriver',options = chrome_options)
#     driver.get(url)         

#     html = driver.page_source
#     # print(pd.read_html(html))
#     # print("---------------------------------------------------------------")
#     # time.sleep(5)
#     # table = pd.read_html(html)[0]
#     # print("---------------------------------------------------------------")
#     # print(table) 
#     # table = pd.read_html(html)[1]
#     # print("---------------------------------------------------------------")
#     # print(table)   
#     table1 = pd.read_html(html)[1]    
#     print(table1)
#     return 
#     # table.columns=colnames
#     table.set_index(["日期"], inplace=True)

#     csv_file = f"{working_path}/capital/all/all-capital.csv"
#     if os.path.exists(csv_file):
#         captial_df = pd.read_csv(csv_file, index_col="日期")
#         captial_df = pd.concat([table, captial_df]).drop_duplicates()          
#     else:
#         captial_df = table
    
#     print(captial_df)
#     captial_df.to_csv(csv_file, encoding="utf-8")
#     driver.close()    


## 获得个股资金流入和流出
def get_daily_gg2(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/capital/gg2/{today_time}-gg2.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    
    page_range = range(1, 101)
    for pagenum in page_range:
        url = f"http://data.10jqka.com.cn/funds/ggzjl/field/zdf/order/desc/page/{pagenum}/ajax/1/free/1/"
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
        table = table.astype({"股票代码": str})

        # 对索引列应用函数
        table['股票代码'] = table['股票代码'].str.zfill(6)     
        table['股票代码'] = table['股票代码'].apply(add_prefix)

        table = table.drop(columns=['序号'])
        table.rename(columns={"股票代码": "代码"}, inplace=True)
        table.set_index('代码',inplace=True)   

        columns_to_convert = ['流入资金(元)', '流出资金(元)', '净额(元)', '成交额(元)']
        table[columns_to_convert] = table[columns_to_convert].applymap(convert_chinese_number)       

        captial_df = pd.concat([captial_df,table]).drop_duplicates()      
        print(captial_df.last)
        driver.close()
        display.stop()
        
    captial_df.to_csv(csv_file, encoding="utf-8")    
    print(captial_df)

## 获得个股融资融券
def get_daily_rzrq(working_path):
    os.chdir(working_path)
    print("working_path " + working_path)
    os.chdir(working_path + "/capital")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    today_time = datetime.today().strftime('%Y-%m-%d')  

    captial_df = pd.DataFrame()
    csv_file = f"{working_path}/capital/rzrq/{today_time}-rzrq.csv"
    if os.path.exists(csv_file):
        os.remove(csv_file)
    
    page_range = range(1, 35)
    for pagenum in page_range:
        url = f"http://data.10jqka.com.cn/market/rzrq/board/ls/field/rzjmr/order/desc/page/{pagenum}/ajax/1/"
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
        column_names=['序号', '代码', '股票名称', '融资余额', '融资买入额', '融资偿还额', '融资净买入', '余量', '卖出量', '偿还量', '融券净卖出', '融资融券余额(元)', '历史']
        table.columns=column_names
        table = table.drop(columns=['序号', '余量', '卖出量', '偿还量', '融券净卖出','历史'])
        table = table.astype({"代码": str})
        table['代码'] = table['代码'].str.zfill(6)     
        table['代码'] = table['代码'].apply(add_prefix)        
        print(table)
 
        table.set_index('代码',inplace=True)   

        columns_to_convert = ['融资余额', '融资买入额', '融资偿还额', '融资净买入', '融资融券余额(元)']
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

    # print("===============================>get_daily_gg")
    # get_daily_gg(working_path)
    # print("===============================>get_daily_bk")
    # get_daily_bk(working_path)
    # print("===============================>get_daily_gn")
    # get_daily_gn(working_path)
    # print("===============================>get_daily_gg2")
    # get_daily_gg2(working_path)
    # print("===============================>get_daily_rzrq")
    # get_daily_rzrq(working_path)
    # print("===============================>get_all_captial")
    # get_all_captial(working_path)    
    # print("===============================>get_north_hy_capital")
    get_north_hy_capital(working_path)

