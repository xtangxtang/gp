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

    # url = "http://data.eastmoney.com/zjlx/detail.html"
    url = 'https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0'
    # url = "http://q.10jqka.com.cn/"   

    # 打开网页
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.XPATH, '//table')))
    print(table)

    # 获取表格数据
    html_content = table.get_attribute('outerHTML')
    df = pd.read_html(html_content)[0]  # 假设表格是页面上的第一个表格
    print(df)    

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
    alink = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pageList"]/div/ul/li[9]/a')))
    print("alink " + str(alink.text))
    WebDriverWait(driver, 10).until(EC.elemenet_to_be_clickable((By.XPATH, '//*[@id="pageList"]/div/ul/li[9]/a'))).click()
    # next_page_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"下一页")]')))
    # next_page_link.click()
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

def get_daily():
    # url = "http://data.eastmoney.com/zjlx/detail.html"
    url = "https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0"
    # url = "http://q.10jqka.com.cn/"


    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/mnt/nvme0n1/chromedriver',chrome_options=chrome_options)
    driver.get(url)  

    # Find all of the rows in the table
    rows = driver.find_elements(By.CSS_SELECTOR, 'table tr')
    # For each row, find the cells and extract the text
    for row in rows:
        try:
            cells = row.find_elements(By.CSS_SELECTOR, 'td') or row.find_elements(By.CSS_SELECTOR, 'th')
        except:
            continue
        for cel in cells:
            print(cel.text, end= ",")
        print()

    driver.find_element_by_xpath("//li[@class='next']").click()
    # driver.execute_script("arguments[0].click();", nxt)

    driver.implicitly_wait(30)

    # Find all of the rows in the table
    rows = driver.find_elements(By.CSS_SELECTOR, 'table tr')
    # For each row, find the cells and extract the text
    for row in rows:
        try:
            cells = row.find_elements(By.CSS_SELECTOR, 'td') or row.find_elements(By.CSS_SELECTOR, 'th')
        except:
            continue
        for cel in cells:
            print(cel.text, end= ",")
        print()    

    driver.quit()
    


if __name__ == "__main__":

    chunks_num =5
    working_path = os.getcwd()

    get_daily2()
