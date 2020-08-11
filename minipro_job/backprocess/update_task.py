from background_task import background
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

from pymongo import MongoClient
import pymysql
from pymongo import MongoClient

# --예시--#
# @background()
# def task_hello(schedule= 10, repeat=60):
#     time_tuple = time.localtime()
#     time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
#     print("task ...Hello World!", time_str)

# django.setting.py 중 INSTALLED_APPS에 'background_task' 추가

#-- 크롬드라이버 설정 
chrome_options = Options() #초기화
chrome_options.add_argument("--headless")
chrome_options.add_argument("disable~~")
path = '/home/sundoosdedu/다운로드/chromedriver' # 경로설정
driver  = webdriver.Chrome(path) # driver 선언
driver.implicitly_wait(3) # 딜레이 설정

#-- URL 참조 위한 section code DB연결
mariadb = pymysql.connect(host='localhost', port=3306, user= 'lee', password='1234', db='job', charset='utf8', autocommit= True)
cursor = mariadb.cursor(pymysql.cursors.DictCursor)
cursor.execute("select * from Job_SectionCode")
rows = cursor.fetchall() #데이터 Fetch
mariadb.close()
codedf = pd.DataFrame(rows) # 직군별 코드 df

#-- 채용공고를 모아두는 MongoDB 연결
mongodb = MongoClient('mongodb://172.17.0.2:27017/')
mydb = mongodb['job_opening']
mycol = mydb["opening_data"]


@background()
# MongoDB에 저장할 요소들 담아둘 lst 변수 선언

def task_crawling(schedule= timedelta(minutes=20), repeat=60):
    #-- 크롤링 대상 사이트 선언
    baseURL = 'https://www.wanted.co.kr/wdlist/'
    datalst = list()
    for idx in range(1): #len(codedf)
        if codedf.iloc[idx][0] == codedf.iloc[idx][2]:
            URL = baseURL+str(codedf.iloc[idx][0])
        else:
            URL = baseURL+str(codedf.iloc[idx][0])+'/'+str(codedf.iloc[idx][2])
        Detail_NM = codedf.iloc[idx][1] # 카테고리 명
        #크롬드라이버로 URL 접근 
        driver.get(URL)
        # Selenium을 통해 Scroll 조작 
        SCROLL_PAUSE_TIME = 2
        #마지막 시점의 창 높이 저장
        last_height =driver.execute_script("return document.body.scrollHeight")
        while True:
            #scroll down to bottom 
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            #마지막 창 로딩을 위해 살짝 스크롤 올리기
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            #새로운 높이가 이전 높이와 변하지 않았으면 스크롤 종료
            if new_height == last_height:
                break

            last_height = new_height
            
        # 크롤링 대상 elements
        page_len = len(driver.find_elements_by_class_name('_3D4OeuZHyGXN7wwibRM5BJ')) #채용공고 한 개 영역

        #새로운 크롬드라이버 선언
        driver2 = webdriver.Chrome(path)
        driver2.implicitly_wait(3)
        #MongoDB 연결하여 같은 직군의 채용공고 호출
        tlst = mycol.find({"Detail_Category": codedf.iloc[idx][1]})

        templst = []
        for x in tlst:
            templst.append(x)
        opendf = pd.DataFrame(templst) 

        for i in range(page_len):    #page_len = 공고 갯수
            # elements path loop를 통해 각 기본 요소 추출
            opening_path = '/html/body/div[1]/div/div[3]/div[2]/div/ul/li['+str(i+1)+']/div/a'                     
            opening = driver.find_element_by_xpath(opening_path)
            opening_url = opening.get_attribute('href')
            opening_company_nm = opening.get_attribute('data-company-name')
            opening_position_nm = opening.get_attribute('data-position-name')
            
            #몽고DB에 존재하는 채용공고와 일치하면 Pass
            tester = mycol.find({"Company_NM": opening_company_nm, 'Position_NM': opening_position_nm})
            testerlst = [x for x in tester]
            if len(testerlst) >= 1:
                pass
            else:
                #채용 공고 상세 진입
                driver2.get(opening_url)
                maintask  = driver2.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[2]/span').text
                qual = driver2.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[3]/span').text
                qual2 = driver2.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[4]/span').text
                
                time_tuple = time.localtime()
                time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
                data =  {"Company_NM": opening_company_nm, 'Detail_Category': Detail_NM,'Position_NM':opening_position_nm, 'URL':opening_url, 'MainTask': maintask, 'Qual': qual, 'Qual2': qual2, 'Time': time_str}
                print('Updated!', data)
                datalst.append(data)
    
    mydb.opening_data.insert_many(datalst)
