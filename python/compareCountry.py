# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:41:59 2020

@author: SHAOQM
"""
import time
import requests
import json
#import matplotlib.pyplot as plt
import numpy as np

#plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签SimHei
#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号#有中文出现的情况，需要u'内容'
import os
currPath = os.path.dirname(os.path.abspath(__file__))

url = r'https://covid19.tk/by_world.json?t='

#response = json.loads(requests.get(url + str(int(time.time()*1000)), verify=False ).text)
#with open('globaldata.json', 'w') as f:
#    json.dump(response, f)

# Get Data
try: response
except NameError: response = None

if response is None:
    try:
        with open(currPath + '/globaldata.json', 'r') as f:
            response = json.load(f)    
    except FileNotFoundError:
        response = json.loads(requests.get(url + str(int(time.time()*1000)), verify=False ).text)
        with open(currPath + '/globaldata.json', 'w') as f:
            json.dump(response, f)
           


#import pandas as pd
#import json
#
#url = 'http://datanews.caixin.com/interactive/2020/pneumonia-h5/data/data2.csv'
#raw = pd.read_csv(url)
#
#data = {'hist':{}, 'time':raw['time'][2:-1].tolist()}
#for col in raw.columns[1:]:
#    data['hist'][col] = pd.to_numeric(raw[col][2:-1]).tolist()
#hist = data['hist']
#with open(currPath + '/chinadata.json', 'w') as f:
#    json.dump(hist, f)


# Add realtime update in production
#response = json.loads(requests.get(url + str(int(time.time()*1000)), verify=False ).text)

with open(currPath + '/chinadata.json', 'r') as f:
    chinahist = json.load(f)
hist = {'China': {'y': chinahist['全国']}}
for res in response:
    if res['confirmedCount']>200 and len(res['countryName'])<7:
#        print(res[-1])
        records = []
        for rec in res['records']:
#            if rec['confirmedCount'] < 200:
#                continue
            month, day  = (int(_) for _ in rec['updateTime'].split('/'))
           
            if month*100+day < 216:
                continue
            records.append(rec['confirmedCount'])
        if len(records)>=4:
            hist[res['countryEnglishName']] = {'y': records}


thres = 100
#marker = 'osD^x'
#plt.clf()
cnt = 0
compareData = {}
for rec in hist:
    arr = np.array(hist[rec]['y'] )
    idx0 = np.argmax(arr > thres)-1
    offset = np.log(thres/arr[idx0]) / np.log(arr[idx0+1]/arr[idx0]) + idx0
#    offset = (thres-hist[rec][idx0]) / (hist[rec][idx0+1]-hist[rec][idx0]) + idx0
    x = np.arange(float(len(arr)))
    x -= offset
    compareData[rec] = [list(_) for _ in zip(x.tolist(),hist[rec]['y'])]


print(json.dumps(compareData))
#    plt.plot(x, np.abs(arr), '-'+marker[cnt//10])
    # cnt += 1
#plt.yscale('log')
#plt.xlim(left = -5, right = 30)
#plt.legend(hist.keys())
#plt.xlabel(f'Days After {thres} Cases')
#plt.ylabel('Accumulated Cofirmed Cases')


