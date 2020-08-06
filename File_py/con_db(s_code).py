import pymysql
import pandas as pd 

## 직군 별 code 정보 mariadb에 저장하는 code ##

df = pd.read_csv('../File/code_table.csv')
#연결할 DB 정보
db = pymysql.connect(host='localhost', port=3306, user= 'lee', password='lcs', db='job', charset='utf8', autocommit= True)
cursor = db.cursor(pymysql.cursors.DictCursor)
# cursor.execute("INSERT INTO test VALUES ('한글', '00001872')")

for idx in range(len(df)):
    if len(str(df['Code'][idx])) > 5:
        s_name = df['Name'][idx]
        temp = df['Code'][idx]
        code = str(temp).split('/')[1]
        #커서 설정 
        cursor.execute("insert into Job_section_Code values ('"+str(code)+"', '"+str(s_name)+"');")
    else:
        s_name = df['Name'][idx]
        cate_code = df['Category_Code'][idx]
        cursor.execute("insert into Job_section_Code values ('"+str(cate_code)+"', '"+str(s_name)+"');")


db.close()

