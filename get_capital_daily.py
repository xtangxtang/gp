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


def get_daily3():
    ua=UserAgent()
    # print('User-Agent :' + ua.random)
    hdr = {'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'} 
    # url = "http://q.10jqka.com.cn/"                  
    # url = "https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0"
    url = "http://data.eastmoney.com/zjlx/detail.html"
    html=requests.get(url, timeout=30, headers=hdr).content
    df_tmp = pd.read_html(html)
    print(df_tmp)

    soup=BeautifulSoup(html,'html.parser')
    next_link = soup.find("a", string="下一页")
    print(next_link.get('href'))


def get_daily2():
    ua=UserAgent()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('User-Agent:' +  ua.random)
    driver = webdriver.Chrome('/mnt/nvme0n1/chromedriver',chrome_options=chrome_options)

    url = "http://data.eastmoney.com/zjlx/detail.html"
    # url = 'https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0'
    # url = "http://q.10jqka.com.cn/"   

    # 打开网页
    # driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))
    # print(table)

    # 获取表格数据
    html_content = table.get_attribute('outerHTML')
    df = pd.read_html(html_content)[0]  # 假设表格是页面上的第一个表格
    # print(df)    

    # pages = driver.find_elements_by_xpath('//*[@id="pageList"]/div/ul/li[9]/a')
    # print("len(pages):" + str(len(pages)))
    # for i in range(len(pages)):
    #     print(pages[i].get_attribute("id"))
    #     try :
    #         WebDriverWait(driver, 10).until(EC.staleness_of(pages[i]))
    #         pages[i].click()

    #         wait = WebDriverWait(driver, 10)
    #         table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))
    #         print(table)            
    #     except:
    #         print("could not click")
    #         pass    

    # return

    # 等待表格加载完成
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))
    print(table)

    # 获取表格数据
    html_content = table.get_attribute('outerHTML')
    df = pd.read_html(html_content)[0]  # 假设表格是页面上的第一个表格
    print(df)
    print("--------------------------------------------")
    # alink = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pageList"]/div/ul/li[9]/a')))
    # print("alink " + str(alink.text))
    # click = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[8]/div[2]/div[6]/div[1]/div[3]/div[1]/a[11]')))
    # print("click")
    next_page_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"下一页")]')))
    next_page_link.click()
    wait.until(EC.staleness_of(table))  # 等待表格刷新
    table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))    

    # # 循环点击下一页直到没有下一页链接为止
    # while True:
    #     try:
    #         next_page_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"下一页")]')))
    #         next_page_link.click()
    #         wait.until(EC.staleness_of(table))  # 等待表格刷新
    #         table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))
    #         html_content = table.get_attribute('outerHTML')
    #         next_df = pd.read_html(html_content)[0]
    #         df = pd.concat([df, next_df], ignore_index=True)
    #     except Exception as e:
    #         print(e)
    #         break

    # # 输出表格数据
    # print(df)        

# 添加前缀的函数
def add_prefix(column):
    if column.startswith('6'):
        return 'sh' + column
    elif column.startswith(('0', '3')):
        return 'sz' + column
    else:
        return column

def get_daily(working_path):
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
    csv_file = f"{working_path}/capital/{today_time}.csv"
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
    captial_df.to_csv(csv_file, encoencodingding="utf-8")


    


if __name__ == "__main__":

    chunks_num =5
    working_path = os.getcwd()

    get_daily(os.getcwd())
    # get_daily3()
