from pymongo import MongoClient
import kss
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
from word_prepro import word_preprocessing

temp_r = word_preprocessing('서버 개발자')
print(type(temp_r))


# #임시


# client = MongoClient('mongodb://172.17.0.2:27017/')
# mydb = client['job_opening']
# mycol = mydb["opening_data"]

# tlst = mycol.find({"Detail_Category": "서버 개발자"})
# # select_col = s_col  # 1.MainTask 2.Qual, 3.Qual2

# templst = []
# for x in tlst:
#     templst.append(x)

# tempdf = pd.DataFrame(templst)
# print(tempdf)