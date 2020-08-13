import pymysql
import pandas as pd 
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import time 

def make_wordcloud(code):
    #-- 워드클라우드를 위한 글꼴 설정 
    fontpath = '../File/S-Core_Dream_OTF/SCDream4.otf'
    font= fm.FontProperties(fname = fontpath, size=9)
    mpl.font_manager._rebuild()


    #-- 워드클라우드 만든 기본 단어 호출 위한 DB 연결
    mariadb = pymysql.connect(host='localhost', port=3306, user= 'lee', password='1234', db='job', charset='utf8', autocommit= True)
    cursor = mariadb.cursor(pymysql.cursors.DictCursor)
    query = "SELECT Word, count(Word) FROM Job_KeyWord WHERE Code_s=%s GROUP BY Word ORDER BY count(Word) DESC LIMIT %s"
    code = code #함수 parameter 처리
    limits = 100 #함수 parameter 처리
    cursor.execute(query,(code, limits)) # 상위 50개 단어 추출
    rows = cursor.fetchall()
    mariadb.close()
    #-- 워드클라우드 만들 단어 목록
    worddict ={}
    for idx in range(len(rows)):
        worddict[rows[idx]['Word']] = rows[idx]['count(Word)'] 

    #-- 워드클라우드 설정
    wordcloud = WordCloud(
        font_path = fontpath,
        width = 1200,
        height = 800,
        background_color='white'
    )


    #-- 워드클라우드 출력
    pic_array = wordcloud.generate_from_frequencies(worddict).to_array()
    fig = plt.figure(figsize=(12,12))
    plt.imshow(pic_array, interpolation='bilinear')
    plt.axis('off')


    #-- 워드클라우드 저장
    time_tuple = time.localtime()
    time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    # fig.savefig('./static/wordcloud_img/wci_%s_%s.png' % (str(time_str.split(', ')[0]), str(code)))
    fig.savefig('./static/wordcloud_img/img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
    fig.savefig('./static/show/showimage.png')
