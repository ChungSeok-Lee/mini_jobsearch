from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

from pymongo import MongoClient

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

# 크롤링 대상 사이트
df = pd.read_csv('./File/code_table.csv')
for cate_num in range(len(df)):  #len(df)
    Detail_NM = df['Name'][cate_num]
    jobsection_url = 'https://www.wanted.co.kr/wdlist/'+str(df['Code'][cate_num])+'?country=kr&job_sort=job.latest_order&years=-1&locations=all' #code_table을 참고하여 url
    driver.get(jobsection_url)

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
    page_len = len(driver.find_elements_by_class_name('_3D4OeuZHyGXN7wwibRM5BJ'))
    # 저장 요소들 lst 변수 선언
    datalst = list()

    driver2 = webdriver.Chrome(path)
    driver2.implicitly_wait(3)

    for i in range(page_len):    #page_len = 공고 갯수
        # elements path loop를 통해 각 기본 요소 추출
        opening_path = '/html/body/div[1]/div/div[3]/div[2]/div/ul/li['+str(i+1)+']/div/a'                     
        opening = driver.find_element_by_xpath(opening_path)
        opening_url = opening.get_attribute('href')
        opening_company_nm = opening.get_attribute('data-company-name')
        opening_position_nm = opening.get_attribute('data-position-name')
        #채용 공고 상세 진입
        driver2.get(opening_url)
        maintask  = driver2.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[2]/span').text
        qual = driver2.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[3]/span').text
        qual2 = driver2.find_element_by_xpath('//*[@id="__next"]/div/div[3]/div[1]/div[1]/div[1]/div[2]/section[1]/p[4]/span').text
        
        data =  {"Company_NM": opening_company_nm, 'Detail_Category': Detail_NM,'Position_NM':opening_position_nm, 'URL':opening_url, 'MainTask': maintask, 'Qual': qual, 'Qual2': qual2}
        datalst.append(data)



    # 저장한 datalst를 MongoDB에 저장
    #Docker로 띄운 원격 Mongodb server로 접속
    client = MongoClient('mongodb://172.17.0.2:27017/')
    jobdb = client.job_opening
    res = jobdb.opening_data.insert_many(datalst)


