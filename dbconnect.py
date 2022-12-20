# MariaDB 연결 정보를 객체로 저장한 파일
# 보안 유지를 위해서 별도의 파일에 보관해줘야 함.


config = {
    'host':'61.74.225.3',
    'user':'root',
    'password':'kor123',
    'database':'2team',
    'port':3306,
    'charset':'utf8',
    'use_unicode':True
}

import pickle

with open('mydb.dat', mode='wb') as obj:
    pickle.dump(config, obj)