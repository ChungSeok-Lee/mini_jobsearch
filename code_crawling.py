import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# 본래 사이트에서 html 코트만 복사해온 뒤 추출하기 편하게 편집하여 임시 서버에 띄우기
res = requests.get('http://minipro-health-ysvmp.run.goorm.io/minipro_health/temp.html')
soup = bs(res.content, 'html.parser')
links = soup.find_all('a', class_ = '')

tempdict = dict()
lst_NM = list()
lst_code = list()
for content in links:
    name = content.text
    lst_NM.append(name.strip())
    lst_code.append(content.get('href'))

tempdict['Name'] = lst_NM
tempdict["Code"] = lst_code

pd.DataFrame(tempdict).to_csv('code_table.csv')
# 이후 주피터 노트북에서 마무리 작업