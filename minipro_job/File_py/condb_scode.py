import pymysql
import pandas as pd 

## 직군 별 code 정보 mariadb에 저장하는 code ##

df = pd.read_csv('../File/code_table.csv')
#연결할 DB 정보
db = pymysql.connect(host='localhost', port=3306, user= 'lee', password='1234', db='job', charset='utf8', autocommit= True)
cursor = db.cursor(pymysql.cursors.DictCursor)
# cursor.execute("INSERT INTO test VALUES ('한글', '00001872')")

for idx in range(len(df)):
    if len(str(df['Code'][idx])) > 5:
        s_name = df['Name'][idx]
        temp = df['Code'][idx]
        code = str(temp).split('/')[1]
        codecate = df['Category_Code'][idx]
        cate = df['Category'][idx]
        #커서 설정 
        query = "INSERT INTO Job_SectionCode VALUES (%s, %s, %s, %s)"
        cursor.execute(query,(str(code), str(s_name), str(codecate), str(cate))
    else:
        s_name = df['Name'][idx]
        cate_code = df['Category_Code'][idx]
        cursor.execute(query,(str(codecate), str(cate), str(codecate), str(cate))


db.close()

