# -*- coding:utf-8 -*-
'''
다른 환경에서 시행 시 주의사항
1.본 코드는 OSX eclipse 기반 3.7 pydev에서 설계됨
2.디렉토리 수정 필수(폴더는 일일히 생성 후 실행할 것.)
3.csv기반 파일처리로 진행되기 때문에 소요시간 3분 내외.
'''
import csv
import pandas as pd
f7 = open('USVIDEO_DATA_TABLE.csv','r')
rdr7 = csv.reader(f7)
f71 = open('worddfterm.csv', 'r')
rdr71 = csv.reader(f71)
inde7 = []
al = '0'
data = []
for rd71 in rdr71:
    inde7.append(rd71[0])
    data.append(al)
dummy7 = []
pure7 =[] 
check7 = []
my_df7 = pd.DataFrame(data=data, index=inde7, columns=["numbers"])
for line7 in rdr7:
    if((line7[0] in check7) or (line7[0]=='VIDEO_ID') or (line7[0]=="Zy6vBxqlapw")):
        continue
    ff7 = open('csvres/'+line7[0]+'_pss'+'.csv','r', newline='\n')
    rd7 = csv.reader(ff7)
    obj7 = ''
    for lin7 in rd7:#CSV 파일을 열어서 리스트를 한덩어리로
        if(len(lin7[0])<31):#처리에 실패한 것으로 간주
            obj7 +=' '+lin7[0].lower()
    adj7 = obj7.split(' ')#합체된걸 다시 list로 나눈다.
    for ad7 in adj7:
        if ad7 in inde7:
            my_df7['numbers'][ad7]=str(int(my_df7['numbers'][ad7])+1)
    ff7.close()        
    my_df7.to_csv('/Users/Haka4700/pywork/maranly/week3/csvres2/'+line7[0]+'.csv', sep=',', na_rep=0)
f8 = open('USVIDEO_DATA_TABLE.csv','r')
rdr8 = csv.reader(f8)
for line8 in rdr8:
    if((line8[0] in check7) or (line8[0]=='VIDEO_ID') or (line8[0]=="Zy6vBxqlapw")):
        continue
    ff8 = open('csvres2/'+line8[0]+'.csv','r', newline='\n')
    rd8 = csv.reader(ff8)
    fw8 = open('csvres3/'+line8[0]+'.csv','w', newline='\n')
    rdw8 = csv.writer(fw8)
    total = 0
    dummy=[]
    for k in rd8:
        if k[1]!="numbers":
            total+=int(k[1])
    ff9 = open('csvres2/'+line8[0]+'.csv','r', newline='\n')
    rd9 = csv.reader(ff9)
    for j in rd9:
        if j[1]!="numbers":
            print(j[0]+","+str(float(j[1])/total))
            dummy.append([j[0],str(float(j[1])/total)])
    rdw8.writerows(dummy)