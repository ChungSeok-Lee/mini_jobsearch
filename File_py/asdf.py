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

twlst = word_preprocessing('서버 개발자')
df = pd.DataFrame(twlst)
df.to_csv('tdf1.csv', index=False)