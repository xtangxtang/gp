from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import time
from datetime import datetime
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options)


driver.get("http://www.sse.com.cn/assortment/stock/list/share/")
time.sleep(3)

select = Select(driver.find_element_by_class_name("selectpicker"))
select.select_by_visible_text('主板A股')
time.sleep(3)
excel_button = driver.find_element(By.CLASS_NAME, 'tableDownload')
excel_button.click()
time.sleep(10)
os.rename('GPLIST.xls', 'sh_zhuban.xls')

select = Select(driver.find_element_by_class_name("selectpicker"))
select.select_by_visible_text('科创板')
time.sleep(3)
excel_button = driver.find_element(By.CLASS_NAME, 'tableDownload')
excel_button.click()
time.sleep(10)
os.rename('GPLIST.xls', 'sh_kcb.xls')


driver.get("http://www.szse.cn/market/product/stock/list/index.html")
time.sleep(3)
excel_button = driver.find_element(By.CLASS_NAME, 'btn-default-excel')
excel_button.click()