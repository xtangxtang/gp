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

def get_daily():
    url = "http://data.eastmoney.com/zjlx/detail.html"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/mnt/nvme0n1/chromedriver',chrome_options=chrome_options)
    driver.get(url)    

    # //*[@id="dataview"]/div[2]/div[2]/table/tbody/tr[1]
    # //*[@id="dataview"]/div[2]/div[2]/table
    # /html/body/div[2]/div[8]/div[2]/div[6]/div[1]/div[2]/div[2]/table/tbody

    # num_rows = len(driver.find_element_by_xpath("//*[@id='dataview']/table"))
    # print(driver.find_element_by_xpath("//*[@id='dataview']/table/tbody"))
    # print(driver.find_element_by_xpath("//*[@id='dataview']"))


    # html=driver.page_source
    # soup=BeautifulSoup(html,'html.parser')
    # div=soup.select_one("div#pagerbox")    
    # print(str(div))

    # exit(0)
    # while True:
    #     try:
    #         # //*[@id="dataview"]/div[3]/div[1]/a[9]
    #         driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dataview']/div[3]/div[1]/a[8]"))))
    #         driver.find_element_by_xpath("//*[@id='dataview']/div[3]/div[1]/a[8]").click()
    #         print("Navigating to Next Page")
    #     except Exception as e :
    #         print(e)
    #         driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='dataview']/div[3]/div[1]/a[9]")))) 
    #         driver.find_element_by_xpath("//*[@id='dataview']/div[3]/div[1]/a[8]").click()
    #         print("Navigating to Next Page")
            
    #         # print("Last page reached")
    #         # break    

    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    div=soup.find("table")
    table=pd.read_html(str(div))
    print(table)


if __name__ == "__main__":

    chunks_num =5
    working_path = os.getcwd()

    get_daily()
