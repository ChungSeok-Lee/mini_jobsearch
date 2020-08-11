import re

def del_k(text):
    txt = text
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기를 제외한 모든 글자 
    result  = hangul.findall(txt)
    return result


