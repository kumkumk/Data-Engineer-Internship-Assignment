# Data-Engineer-Internship-Assignment
This project is about collecting data about top cities of United States from Wikipedia and New York Times Search API using Python and its library BeautifulSoup

## Getting Started
There are 2 py scripts : wiki-scrape.py and nyt.py:

1.wiki-scrape.py contains the code for scraping data about top cities from Wikipedia

2.nyt.py contains code to collect data about US cities from NYT search API responses in JSON

3.Output : collected data is written to  csv files ready to be uploaded to BigQuery table

### Wikipedia Web Scraping
the wiki-scrape.py returns multiple csv files:
1. Top 100 cities by "Population".csv -  a table scraped from the Wikipedia page about the top cities in USA written to csv file with the header row giving the column names and comma separated. we can generate multiple csv files by different filters eg.Population,Density etc
2. city.csv eg: Chicago.csv : contains the text extracted from Wikipedia city pages whose links were given in the table from Top 100 cities file described above

### NYT Data Collection:
Used NYT search API to fetch furthur information about Cities in USA
There were 2 kinds of searches done :
1. search for a keyword eg."crime" and look for glocations i.e geolocations of returned articles and then find the top cities/locations in terms of the articles count relating to Crime
2. search for a given city and find the top category of news articles published about that City. For now I have given state names as a list of geolocations ['ARIZONA','CALIFORNIA']. the results in the form of a dictionary with key as the news type and value as article count eg.{"Sports":490 }  


