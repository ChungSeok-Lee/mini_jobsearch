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
import re
from word_prepro_dele_kor import del_k


def word_preprocessing(D_cate):
  ## SECTION __ DB 연결  ##
  client = MongoClient('mongodb://172.17.0.2:27017/')
  mydb = client['job_opening']
  mycol = mydb["opening_data"]
  tlst = mycol.find({"Detail_Category": D_cate})
  
  ## SECTION __ 기초 데이터셋  ##
  templst = []
  for x in tlst:
      templst.append(x)

  tempdf = pd.DataFrame(templst) 

  ## SECTION __ 한글 글자 추출 과정 ##
  okt = Okt()
  wordlst =[]
  k_word = []
  kkwordlst = []
  for select_col in ['MainTask', 'Qual', 'Qual2']:
    for feature in tempdf[select_col]:
        word = okt.nouns(feature)
        kkwordlst += word
  for element in kkwordlst:
    if len(element) > 1: # 한 글자 수 이하 단어 삭제
        k_word.append(element)

  result_k =[]
  stop_words_korean_words = ['관련', '보유', '우대', '대한', '대해', '이상', '이상인', '기반'] # 한글 단어 중 의미 없는 불용어 리스트   
  for txt in k_word:
    if txt not in stop_words_korean_words:
      result_k.append(txt)  

  ## SECTION __ 영어 글자 추출 과정 ##
  stop_words = set(stopwords.words('english')) #보편적인 불용어
  for select_col in ['MainTask', 'Qual', 'Qual2']: #영어 추출
    feature = tempdf[select_col] 
    for content in feature:
      tplst = word_tokenize(content)
      for element in tplst:
        if len(element) > 1: # 한 글자 수 이하 단어 삭제
          wordlst.append(element)
  
  # 영어 & 한글 분리
  k_wordlst = []
  o_wordlst = []
  t_wordlst = []
  for testword in wordlst:
    if ord('가') <= ord(testword[0]) <= ord('힣'):
      # k_wordlst.append(testword)
      pass
    else:
      o_wordlst.append(testword)

  # _영어: General 불용어 삭제 & 뒤에 붙은 한글 삭제 _ ['시스템', '경력', '개발', '기반'] 등 앞에 특정 단어만 가지고 충분히 필요역량이 무엇인지 유추가능하여 삭제
  result= list()
  for txt in o_wordlst:
    if txt not in stop_words:
      result.append(txt)
  result_e = list()
  for word in result:
    trslt = del_k(word)
    if type(trslt) is list:
      for t_word in trslt:
        if ord('a') <= ord(t_word.lower()[0]) <= ord('z'):
          result_e.append(t_word.upper()) #string.upper 영어 모두 대문자로 통일
    else:
      result_e.append(trslt.upper())

  ## SECTION __ 영어 + 한글 | 단어장 합치기 ##
  t_result = result_k+ result_e

  fin_result = list()
  for txt in t_result:
    if '/' in txt:  # 최종 단어 중에 /로 구분되어 있는 단어들 검색
      for tttxt in txt.split('/'):  # /로 구분되어 있는 단어 split하여 각각 fin_result에 추가
        if len(tttxt) >1:
          fin_result.append(tttxt)
    elif len(txt) > 1:
      fin_result.append(txt)

  return fin_result
