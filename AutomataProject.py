import requests
import lxml
from bs4 import BeautifulSoup
import re

# Accessing URl
url = "https://www.usf.edu/engineering/undergraduate/e-council.aspx"  ##Enter URL here
page = requests.get(url)  ##There is alternative way of requesting access just in case of errors

# Parse Webpage with Beautiful soup object
page_source = str(BeautifulSoup(page.content, 'lxml'))

#subpages = []
#for anchor in soup.find_all('a', href=True):
#    string = 'https://www.usf.edu'+str(anchor['href'])
#    subpages.append(string)

# compile regex pattern into a regex object
re_emailLink = re.compile(r"(?<=mailto:)[0-9a-zA-Z.+-_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}")

# parse page source for regex matches using regex object
email_matches = re.findall(re_emailLink, page_source)

# print regex matches
print(email_matches)

#print(soup)

#print(soup)



##Extract Information
##3 ways to elements:
##1.) 'findall()': Find all nodes
##2.) 'find()': Find a single node
##3.) 'select()': Finds nodes according to the selector CSS Selector

