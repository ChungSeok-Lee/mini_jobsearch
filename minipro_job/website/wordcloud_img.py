import pymysql
import pandas as pd 
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import time 


def make_wordcloud(code):
    #-- 워드클라우드를 위한 글꼴 설정 
    # fontpath = './static/Font/SCDream4.otf'
    # font= fm.FontProperties(fname = fontpath).get_name()
    # mpl.font_manager._rebuild()
    # plt.rcParams["font.family"]=font
    font_fname = 'website/static/Font/SCDream4.otf'
    font_family = fm.FontProperties(fname= font_fname).get_name()
    plt.rcParams["font.family"] = font_family


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
    wordcloud_ = WordCloud(
        font_path = font_fname,
        width = 1200,
        height = 800,
        background_color='white'
    )


    #-- 워드클라우드 출력
    words = wordcloud_.generate_from_frequencies(worddict)
    pic_array = words.to_array()
    fig = plt.figure(figsize=(12,8))
    plt.imshow(pic_array, interpolation='bilinear')
    plt.axis('off')


    #-- 워드클라우드 저장
    time_tuple = time.localtime()
    time_str = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    fig.savefig('website/static/wordcloud_img/img_%s_%s.png' % (str(code), str(time_str.split(', ')[0].replace('/', ''))))
    fig.savefig('website/static/show/showimage.png')
    
    return pic_array
