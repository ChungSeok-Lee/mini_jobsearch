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

  # _영어: General 불용어 삭제 & 뒤에 붙은 한글조사 삭제
  result= list()
  for txt in o_wordlst:
    if txt not in stop_words:
      result.append(txt)
  stop_words_k = ['은', '는', '이', '가', '에', '의', '을','를', '등', '으로', '로', '과', '와'] #영단어 뒤에 붙을 한글 조사 불용어 리스트
  result_e = list()
  for word in result:
    for letter in word:
      if letter in stop_words_k:
        word = word.replace(letter,'')
    result_e.append(word)

  ## SECTION __ 영어 + 한글 | 단어장 합치기 ##
  t_result = result_k+ result_e

  fin_result = list()
  for txt in t_result:
    if len(txt) > 1:
      fin_result.append(txt)
  result_ = Counter(fin_result) #글자 빈도수 카운트
  for key, value in dict(result_).items(): #빈도수 10 미만 단어 삭제
    if value < 10 :
      del result_[key]

  return result_
