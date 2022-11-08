import requests
import lxml
from bs4 import BeautifulSoup
import re

# Accessing URl
url = "https://www.usf.edu/engineering/about/deans-office.aspx"
page = requests.get(url)

# Parse Webpage with Beautiful soup object
page_source = BeautifulSoup(page.content, 'html.parser')

# Parse root page for '/engineering' subpages
subpages = [url]
for tag in page_source.find_all(href=re.compile("^/engineering")):
    if '/engineering' in tag['href']:
        url = 'https://www.usf.edu'+str(tag['href'])
        subpages.append(url)

print(subpages)

# compile regex pattern into a regex object
re_emailLink = re.compile(r"(?<=mailto:)[0-9a-zA-Z.+-_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}")
re_phoneNumber = re.compile(r"\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}")

# parse page source for regex matches using regex object
for url in subpages:
    page = requests.get(url)
    page_source = str(BeautifulSoup(page.content, 'html.parser'))
    email_matches = re.findall(re_emailLink, page_source)
    phone_matches = re.findall(re_phoneNumber, page_source)
    print("URL: "+url)
    print("    Emails: ", end='')
    print(email_matches)
    print("    Phone#: ", end='')
    print(phone_matches)


