# -*- coding:utf-8 -*-
'''
다른 환경에서 시행 시 주의사항
1.본 코드는 OSX eclipse 기반 3.7 pydev에서 설계됨
2.디렉토리 수정 필수(폴더는 일일히 생성 후 실행할 것.)
3.csv기반 파일처리로 진행되기 때문에 소요시간 3분 내외.
'''
import pandas as pd
import csv

from textblob import TextBlob
from collections import Counter

import networkx as nx
from IPython.display import display


def return_centralities_as_str(input_g):
    # weighted degree centrality를 딕셔너리로 리턴
    
    def return_pagerank(input_g):
        return nx.pagerank(input_g, weight='weight')
    return {
        'pagerank':return_pagerank(input_g)
    }

#DF 기본 뼈대 완성 핫-하
g5 = open('wordcountmanual.csv','r')
rgr5 = csv.reader(g5)
inde5 = []
for rg5 in rgr5:
    inde5.append(''.join(rg5))
my_df5 = pd.DataFrame(index=inde5, columns=inde5, data=0)
display(pd.DataFrame(my_df5))

#USVIDEO에 있는 ID대로 데이터를 분해한 걸 각각 분석돌려준다.
f6 = open('USVIDEO_DATA_TABLE.csv','r')
rdr6 = csv.reader(f6)
dummy6 = []
pure6 =[] 
check6 = []
for line6 in rdr6:
    if((line6[0] in check6) or (line6[0]=='VIDEO_ID') or (line6[0]=="Zy6vBxqlapw")):
        #print("넌 돌아가")
        continue
    if((len(check6)+1)<0 or (len(check6)+1)>100 or (len(check6)+1)==49):
        #print(str(len(check)+1)+'/49번째는 건너뛸꺼야')
        check6.append(line6[0])
        continue
    #print(str(len(check)+1)+'/49번째 진행중')
    check6.append(line6[0])
    ff6 = open('csvres/'+line6[0]+'_pss'+'.csv','r', newline='\n')
    rd6 = csv.reader(ff6)
    obj6 = ''
    for lin6 in rd6:#CSV 파일을 열어서 리스트를 한덩어리로
        if(len(lin6[0])<31):#처리에 실패한 것으로 간주
            obj6 +=' '+lin6[0].lower()
              
    adj6 = obj6.split(' ')#합체된걸 다시 list로 나눈다.
    #print(type(adj))
    #break/goto/continue는 느리게 만드는 주범이다.
    count6=Counter(adj6)
    tag_count6 = []
    tags6 = []
      
      
    for ad6 in adj6:
        for a6 in adj6:
            if (ad6 in inde5) and (a6 in inde5):
                my_df5[ad6][a6]+=1
    ff6.close()         
my_df5.to_csv('/Users/Haka4700/pywork/maranly/week3/wordrelfin.csv', sep=',', na_rep=0)
'''
display(pd.DataFrame(my_df5))
G6 = nx.Graph()
GG6=[]
for ind6 in inde5:
    for ind7 in inde5:
        GG6.append([ind6, ind7, my_df5[ind6][ind7]])

G6.add_weighted_edges_from(GG6)
nx.draw_networkx(G6)

ddic = return_centralities_as_str(G6)
ddi = []
my_df7 = pd.DataFrame(index=inde5, columns=inde5, data=0)
for k,v in ddic.items():
    for kk,vv in v.items():
        ddi.append([kk, str(vv)])
        print(kk)
        print(vv)
        my_df7[kk][kk]=str(vv)
my_df7.to_csv('/Users/Haka4700/pywork/maranly/week3/wordreleigen.csv', sep=',', na_rep=0)
'''
'''
eigenvector는 코드에 문제가 있어서 보류.
pagerank(단순 빈도)기반으로 이용할 단어 선정
'''