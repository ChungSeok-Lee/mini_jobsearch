from background_task import background
import time
import requests
from bs4 import BeautifulSoup as bs
import sqlite3

# --예시--#
# @background()
# def task_hello(schedule= 10, repeat=60):
#     time_tuple = time.localtime()
#     time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
#     print("task ...Hello World!", time_str)

# django.setting.py 중 INSTALLED_APPS에 'background_task' 추가


# 초기화 --------------------------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("disable~~")

# 크롬드라이버 경로
path = '/home/sundoosdedu/다운로드/chromedriver'
# 선언
driver  = webdriver.Chrome(path)

# 딜레이
driver.implicitly_wait(3)


@background()
def task_crawling(schedule= 10, repeat=60):
    conn = sqlite3.connect('db.sqlite3')
    query = 'CREATE TABLE economic (title TEXT, link TEXT)'
    conn.execute(query)
    conn.commit
    conn.close()

    

    