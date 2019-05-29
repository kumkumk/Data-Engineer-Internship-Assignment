# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:58:14 2019

@author: Kumkum
"""

import requests
import json
import csv
from collections import Counter

# fetch_url()- for dyanamic url  creation based on paramaters
# the returned url is then used to fetch Json responses from NYT server
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

# info_city for fetching topmost news desk for given city

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
# calling info_city for all states and save the topmost topics to a list
for state in states:
    top_topics={}
    temp=info_city(state)
    temp=list(temp.keys())
    
    res.append(temp)


# creating a dictionary of {state:list of topmost topics}
statedic={}
for ix,state in enumerate(states):
    statedic[state]=res[ix]

# write the results in dictionary from above to csv file
with open("top issues for given city.csv",mode='w+') as f1:
    writer=csv.writer(f1,delimiter=",")
    for key,value in statedic.items():
        writer.writerow([key,value])
    
    



#second part to fetch top cities for a given topic
        
# fetch url for topic-shooting

myurl=fetch_url('shooting','20190101','20190501','KZkw3mzFKLQ7TwPGfG7kmIbdkqi0uAyd')
print(myurl)
mycontent=requests.get(myurl)

resp=json.loads(mycontent.text)

hits=resp['response']['meta']['hits']

# NYT allows only 1000 results to be queried (10 per page) 
if hits>1000:
    pages=10
else:
    pages=hits//10

l=[]

# page_num passed in url to paginate through the returned results
   
for page_num in range(pages):
    nextpageurl=myurl+'&page={}'.format(page_num)
    #print("url is ")
    #print(nextpageurl)
    mycontent=requests.get(nextpageurl)
    resp=json.loads(mycontent.text)
    listofsmth=resp['response']['docs']
    for article in listofsmth:
    #print('keywords***********')
        temp_list=article['keywords']
        for ele in temp_list:
            if ele['name']=="glocations":
                l.append(ele["value"])

mydic=Counter(l)

newd=dict(mydic)

# create a dictionary to store CityName , Count of articles as key value pairs
newd2={}
for ele in newd.keys():
    newele=ele.split('(')[0]
    newd2[newele]=newd[ele]
print(newd2)

# write to dictionary above to csv file
with open("shooting.csv",mode='w+') as csv_file:
    writer=csv.writer(csv_file)
    writer.writerow(["City","Count"])
    for key,value in newd2.items():
        writer.writerow([key,value])
    


    


