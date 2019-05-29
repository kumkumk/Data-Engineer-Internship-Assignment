# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:58:14 2019

@author: Kumkum
"""

import requests
import json
import csv
from collections import Counter

def fetch_url(q,begin_date,end_date,key,**kwargs):
    c=0
    if kwargs:
        k=kwargs.keys()
        if 'fq' in k:
            fq=kwargs['fq']
            c=c+1
        if 'facet_fields' in k:
            c=c+2
            facet_fields=kwargs['facet_fields']
            facet=kwargs['facet']
            facet_filter=kwargs['facet_filter']
    if c==0:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&begin_date={}&end_date={}&api-key={}".format(q,begin_date,end_date,key)
    elif c==1:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq={}&begin_date={}&end_date={}&api-key={}".format(q,fq,begin_date,end_date,key)
    elif c==2:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&facet_fields={}&facet={}&facet_filter={}&begin_date={}&end_date={}&api-key={}".format(q,facet_fields,facet,facet_filter,begin_date,end_date,key)
    elif c==3:
        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&fq={}&facet_fields={}&facet={}&facet_filter={}&begin_date={}&end_date={}&api-key={}".format(q,fq,facet_fields,facet,facet_filter,begin_date,end_date,key)
    
    
    return url     

#myurl=fetch_url('government','20190101','20190501','KZkw3mzFKLQ7TwPGfG7kmIbdkqi0uAyd',fq='news_desk:("U.S.")')

#myurl=fetch_url('government','20190101','20190501','KZkw3mzFKLQ7TwPGfG7kmIbdkqi0uAyd')

def info_city(city_name):

    myurl=fetch_url(city_name,'20190101','20190501','KZkw3mzFKLQ7TwPGfG7kmIbdkqi0uAyd',fq='glocations:("{}")'.format(city_name),facet_fields='news_desk',facet='true',facet_filter='true')
    print(myurl)
    mycontent=requests.get(myurl)
    resp=json.loads(mycontent.text)
    listofd=resp['response']['facets']['news_desk']['terms']
    topics = {}
    for ele in listofd:
        topic=ele['term']
        topics[topic]=ele['count']
    return topics

states = ['TEXAS','CALIFORNIA','NEW YORK CITY','FLORIDA','ARIZONA','OHIO','MICHIGAN']
res=[]
for state in states:
    top_topics={}
    temp=info_city(state)
    temp=list(temp.keys())
    #print(temp)
    res.append(temp)
print(res)
statedic={}
for ix,state in enumerate(states):
    statedic[state]=res[ix]

print(statedic)
with open("top issues for given city.csv",mode='w+') as f1:
    writer=csv.writer(f1,delimiter=",")
    for key,value in statedic.items():
        writer.writerow([key,value])
    
    





myurl=fetch_url('shooting','20190101','20190501','KZkw3mzFKLQ7TwPGfG7kmIbdkqi0uAyd')
print(myurl)
mycontent=requests.get(myurl)

resp=json.loads(mycontent.text)

hits=resp['response']['meta']['hits']

if hits>1000:
    pages=10
else:
    pages=hits//10

l=[]
   
for page_num in range(pages):
    nextpageurl=myurl+'&page={}'.format(page_num)
    print("url is ")
    print(nextpageurl)
    mycontent=requests.get(nextpageurl)
    resp=json.loads(mycontent.text)
    listofsmth=resp['response']['docs']
    for article in listofsmth:
    #print('keywords***********')
        temp_list=article['keywords']
        for ele in temp_list:
            if ele['name']=="glocations":
                l.append(ele["value"])
print("list is "+str(l))
mydic=Counter(l)
print("dictionary is")
newd=dict(mydic)
#print(newd)
newd2={}
for ele in newd.keys():
    newele=ele.split('(')[0]
    newd2[newele]=newd[ele]
print(newd2)

with open("shooting.csv",mode='w+') as csv_file:
    writer=csv.writer(csv_file)
    writer.writerow(["City","Count"])
    for key,value in newd2.items():
        writer.writerow([key,value])
    


    


