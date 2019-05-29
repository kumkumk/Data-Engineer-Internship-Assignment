# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:15:00 2019

@author: Kumkum
"""

from bs4 import BeautifulSoup
import requests
import csv
import unicodedata

# fetch url to be scraped
html=requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population")

#parse the content returned and create a BeautifulSoup object
parsed=BeautifulSoup(html.content,'html5lib')

tables=parsed.findAll('table')

#get the table with list of top cities
table=tables[4]


rows=table.findAll('tr')

header = rows[0]

cols=[]

#get the column names from table first row
for head in header.findAll('th'):
    colname = head.text
    colname =colname.strip('\n')
    cols.append(colname)

cols.append('City Link')

dic={}
for col in cols:
    dic[col]=[]
#print('Dictionary'+str(dic))

str1='https://en.wikipedia.org'

i=0
for row in rows[1:101]:
    
    cells=row.findAll('td')
    temp=cells[0].text.strip('\n')
    dic[cols[0]].append(temp)
    dic[cols[-1]].append(str1+cells[1].a['href'])
    dic[cols[1]].append(cells[1].a.text)
    #dic[cols[-1]].append(str1+cells[2].a['href'])
    temp=unicodedata.normalize("NFKD",cells[2].text)
    temp=temp.strip('\n')
    dic[cols[2]].append(temp)
    temp=cells[3].text.strip('\n')
    dic[cols[3]].append(temp)
    temp=cells[4].text.strip('\n')
    dic[cols[4]].append(temp)
    temp=cells[5].text.strip('\n')
    dic[cols[5]].append(temp)
    temp=unicodedata.normalize("NFKD",cells[6].text)
    temp=temp.strip('\n')
    dic[cols[6]].append(temp)
    temp=unicodedata.normalize("NFKD",cells[8].text)
    temp=temp.strip('\n')
    dic[cols[7]].append(temp)
    
    lat_tag=cells[10].find('span',attrs={'class':'latitude'})
    
    lat_tag=unicodedata.normalize("NFKD",lat_tag.text)
    long_tag=cells[10].find('span',attrs={'class':'longitude'})
    long_tag=unicodedata.normalize("NFKD",long_tag.text)
    
    dic[cols[8]].append(lat_tag+" "+long_tag)
    i=i+1
    #temp=unicodedata.normalize("NFKD",cells[10].text)
    #dic[cols[8]].append(cells[10].span.text)

#print('dictionary updated'+str(dic))

typ="population"

# write the table to csv file
with open("top 100 cities by {}.csv".format(typ),mode='w+',encoding='utf-8') as f1:
    writer=csv.writer(f1,delimiter = ",")
    writer.writerow(dic.keys())
    writer.writerows(zip(*dic.values()))

#prepare url links from the table scraped above
city_links=dic['City Link']
parsed_cities=[]

# to fetch text from the city link passsed as argument
def gather_city(parsed_city,city):
    with open('{}.csv'.format(city),mode='w+',encoding='utf-8') as f:
        writer=csv.writer(f,delimiter=',',quoting=csv.QUOTE_MINIMAL)
        para=parsed_city.findAll('p')
        for p in para[:6]:
            writer.writerow([p.text])
        
# 10 sample cities taken from table above 
for link in city_links[:10]:
    city=requests.get(link)
    parsed_cities.append(BeautifulSoup(city.content,'html5lib'))
    

for ix,parsed_city in enumerate(parsed_cities):
    gather_city(parsed_city,dic['City'][ix])
 
  






