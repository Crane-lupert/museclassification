# -*- coding:utf-8 -*-
'''
다른 환경에서 시행 시 주의사항
1.본 코드는 OSX eclipse 기반 3.7 pydev에서 설계됨
2.디렉토리 수정 필수(폴더는 일일히 생성 후 실행할 것.)
3.csv기반 파일처리로 진행되기 때문에 소요시간 3분 내외.
4.kaggle에 있는 데이터를 기반으로 하지만, NLP 파이썬 코드를 돌리기 전에
    sql(oracle)로 usvideo상에서 category_id가 10번인 것만 남겼고,
    uscomments에도 동일한 처리가 이루어짐(63만개의 comment->9만개 가량의 comment)
'''
import csv

from textblob import TextBlob
from collections import Counter


f = open('USCOMMENTS_DATA_TABLE.csv','r')
rdr = csv.reader(f)

dirbefore =''
dirafter = 'javajavajava'
dummy=[]

for line in rdr:
    print(line[0])
    dirbefore='csvhell2/'+line[0]+'.csv'
    if(line[0]=='VIDEO_ID'):
        continue
    elif(dirafter=='javajavajava'):#처음임
        print('fir : '+line[1])
        f = open(dirbefore,'w', newline='\n')
        dummy.append([line[1]])
        dirafter ='csvhell2/'+line[0]+'.csv'
    elif(dirbefore==dirafter): #ID가 이전과 동일
        print('con : '+line[1])
        dummy.append([line[1]])
    elif(dirbefore!=dirafter):#ID가 이전과 다름
        print('새 개통')
        wr = csv.writer(f)#이전까지 했던 걸 넣어준다.
        wr.writerows(dummy)#삽입 얍!
        #print('dummy : '+dummy)
        f = open('csvhell2/'+line[0]+'.csv','w', newline='\n')#주소를 재지정해주고
        dummy.clear()
        dummy.append([line[1]])#더미도 재지정해준다.
        dirafter ='csvhell2/'+line[0]+'.csv'#애프터도 재지정해준다.
        
#여기까지 댓글들을 Video_ID에 기반해서 쪼개넣는 것.

#댓글에서 형용사만 살린다.
def get_adjectives(text):
    blob = TextBlob(text)
    return [ word for (word,tag) in blob.tags 
            if tag == 'JJ' or tag =='JJR' or tag =='JJS']


f2 = open('USVIDEO_DATA_TABLE.csv','r')
rdr2 = csv.reader(f2)
check = []
dummy = []

for line2 in rdr2:
    if((line2[0]!='VIDEO_ID' and line2[0] not in check) and line2[0]!="Zy6vBxqlapw"):
        '''
        왜인진 모르겠으나 SQL csv 입출력과정에서 해당 video_id 댓글데이터가 사라짐. 
        해당 데이터가 사라져도 전체 분석에 지장은 없으므로 속행.
        ''' 
        check.append([line2[0]])
        ff2 = open('csvhell2/'+line2[0]+'.csv','r', newline='\n')
        rd2 = csv.reader(ff2)
    #csvhell에 저장한 비디오 키로된 제목 파일들을 연다.
        for lin2 in rd2:
            obj = ' '.join(get_adjectives(lin2[0]))
            if(obj!=''):
                dummy.append([obj])    
    fff2 = open('csvres/'+line2[0]+'_pss'+'.csv','w', newline='\n')
    wr = csv.writer(fff2)
    wr.writerows(dummy)
    dummy=[]
#csvres에는 형용사만 필터링된 댓글내용이 VideoID별 csv파일마다 쪼개넣어졌다.

#USVIDEO에 있는 ID대로 데이터를 분해한 걸 각각 분석돌려준다.
f3 = open('USVIDEO_DATA_TABLE.csv','r')
rdr3 = csv.reader(f3)
cnt=0
# dummy = []
fff3 = open('wordtotallist.csv' , 'w', newline='\n')
wr3 = csv.writer(fff3)
for line3 in rdr3:
    if(line3[0]!='VIDEO_ID' and line3[0]!="Zy6vBxqlapw"):
        print(line3[0])
        ff3 = open('csvres/'+line3[0]+'_pss'+'.csv','r', newline='\n')
        rd3 = csv.reader(ff3)
        obj = ''
        print(cnt)
        cnt+=1
        for lin3 in rd3:#CSV 파일을 열어서 리스트를 한덩어리로
            if(len(lin3[0])<=30):#처리에 실패한 것으로 간주
                obj +=' '+lin3[0].lower()#합체!
    
    adj = obj.split(' ')#합체된걸 다시 list로 나눈다.
    count=Counter(adj)
    tag_count = []
    tags = []
    for n in count.keys():
        if(count.get(n)<3 or n==''):
            adj.remove(n)
            
#     ffw = open('csvres/'+line[0]+'_pss'+'.csv','w', newline='\n')
#     wrw = csv.writer(ffw)
#     for lin in rd:
    
    for v in adj:
        if v not in dummy:
            dummy.append(v)
            wr3.writerow([v])
'''
여기까지 해서 나온 단어의 수가 약 900~1200개 사이(버전마다 차이 있음)
이걸 수작업으로 다시 400~500개대로 줄인다.
wordtotallist.csv를 이렇게 줄인 것을 wordcountmanual.csv로 이름짓는다.
'''
