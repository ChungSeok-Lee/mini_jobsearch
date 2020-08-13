# DB 연결
import pymysql
from pymongo import MongoClient

import pandas as pd
# 자연어 전처리 라이브러리 _ pip install konlpy
from konlpy.tag import Okt # 오류가 난다면 jdk(java 확인해볼 것)
import nltk
from nltk.tokenize import word_tokenize
from nltk import Text
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')
from collections import Counter # 리스트의 글자 수 카운트
from word_prepro import word_preprocessing # 단어의 나열 리스트로 반환


df = pd.read_csv('../File/code_table.csv')
df = df[['Name', 'Code']]

db = pymysql.connect(host='localhost', port=3306, user= 'lee', password='1234', db='job', charset='utf8', autocommit= True)
cursor = db.cursor(pymysql.cursors.DictCursor)

query = "INSERT INTO Job_KeyWord VALUES (%s, %s)"

for idx in range(len(df)):   #len(df)
    if '/' in str(df[idx]):
        s_name = df['Name'][idx]
        temp = df['Code'][idx]
        s_code = str(temp).split('/')[1]
        temp_r = word_preprocessing(str(s_name))
        for content in temp_r:
            cursor.execute(query,(str(s_code), str(content)))
    else:
        s_name = df['Name'][idx]
        s_code = df['Code'][idx]
        temp_r = word_preprocessing(str(s_name))
        for content in temp_r:
            cursor.execute(query,(str(s_code), str(content)))

db.close()