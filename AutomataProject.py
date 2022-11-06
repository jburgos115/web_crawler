##Here is website for reference: https://www.topcoder.com/thrive/articles/web-crawler-in-python

import requests
import lxml
from bs4 import BeautifulSoup

##Accessing URl
url = "https://www.usf.edu/engineering/"  ##Enter URL here
f = requests.get(url)  ##There is alternative way of requesting access just in case of errors

##Parse Webpage with Beautiful soup object
soup = BeautifulSoup(f.content, 'lxml')

subpages = []
for anchor in soup.find_all('a', href=True):
    string = 'https://www.usf.edu'+str(anchor['href'])
    subpages.append(string)

print(subpages)

#print(soup)



##Extract Information
##3 ways to elements:
##1.) 'findall()': Find all nodes
##2.) 'find()': Find a single node
##3.) 'select()': Finds nodes according to the selector CSS Selector

