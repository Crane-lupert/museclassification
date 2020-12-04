# -*- coding:utf-8 -*-
'''
다른 환경에서 시행 시 주의사항
1.본 코드는 OSX eclipse 기반 3.7 pydev에서 설계됨
2.디렉토리 수정 필수(폴더는 일일히 생성 후 실행하는 것을 권장.)
3.csv기반 파일처리로 진행되기 때문에 소요시간 3분 내외.
'''
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import csv
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from pandas.io.parsers import read_csv

f7 = open('USVIDEO_DATA_TABLE.csv','r')
rdr7 = csv.reader(f7)
f71 = open('worddfterm.csv', 'r')
rdr71 = csv.reader(f71)
inde7 = []
al = '0'
databs = []
for rd71 in rdr71:
    inde7.append(rd71[0])
    databs.append(al)
total = []
for line7 in rdr7:
    if((line7[0]=='VIDEO_ID') or (line7[0]=="Zy6vBxqlapw")):
        continue
    column=[]
    data = []
    ff7 = open('csvres3/'+line7[0]+'.csv','r', newline='\n')
    rd7 = csv.reader(ff7)
    for r7 in rd7:
        column.append(r7[0])
        data.append(r7[1])
    k=pd.DataFrame(data=data, index=inde7, columns=[line7[0]]).transpose()
    total.append(k)
finto = total[0]
for tot in range(len(total)-1):
    finto.loc[total[tot+1].loc[total[tot+1].index[0]].name] = total[tot+1].loc[total[tot+1].index[0]]

d=finto

pca = PCA(n_components = 2)
X2D = pca.fit_transform(d)

pca = PCA() #주성분 개수 지정하지 않고 클래스생성
pca.fit(d.values)  #주성분 분석
cumsum = np.cumsum(pca.explained_variance_ratio_) #분산의 설명량을 누적합
num_d = np.argmax(cumsum >= 0.95) + 1 # 분산의 설명량이 95%이상 되는 차원의 수

pca = PCA(n_components=0.95) #95%이상의 분산을 설명력을 갖는 차원축소
new_d = pca.fit_transform(d)
ontherun=pd.DataFrame(new_d, index=d.index)

plt.figure(figsize = (10, 7))
plt.title("Sentimental Dendograms")
dend = shc.dendrogram(shc.linkage(ontherun, method = 'ward'))
plt.show()

amc = ontherun.iloc[:, 0:4].values

cluster = AgglomerativeClustering(n_clusters = 6, affinity = 'euclidean', linkage = 'ward')
agmc = cluster.fit_predict(amc)
plt.figure(figsize = (10, 7))
plt.scatter(amc[:,0], amc[:,1], c = cluster.labels_, cmap = 'rainbow')
for label, x, y in zip(d.index, amc[:, 0], amc[:, 1]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-1, 1),
        textcoords='offset points', ha='right', va='bottom')
plt.show()

plt.figure(figsize = (10, 7))
plt.scatter(amc[:,0], amc[:,2], c = cluster.labels_, cmap = 'rainbow')
for label, x, y in zip(d.index, amc[:, 0], amc[:, 2]):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-1, 1),
        textcoords='offset points', ha='right', va='bottom')
plt.show()
finresult = []
ld= list(d.index)
lag = list(agmc)
f9 = open('USVIDEO_DATA_TABLE.csv','r')
rdr9 = csv.reader(f9)
result = pd.DataFrame(data=None, columns=['video_ID','section_key'])
for rd9 in rdr9:
    for i in range(len(ld)):
        if ld[i]==rd9[0]:
            result.loc[rd9[1]] = [rd9[1], lag[i]]
print(result.head())
result.to_csv('final_classification_result.csv')


