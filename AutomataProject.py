import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET

# compile regex pattern into regex objects
re_emailLink = re.compile(r"(?<=mailto:)[0-9a-zA-Z.+-_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}")  # matches the email format defined in RFC
re_phoneNumber = re.compile(r"\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}")  # matches the standard email formats
re_aspx = re.compile(r"\.aspx$")  # matches .aspx websites

# accessing URl
url_root = "https://www.usf.edu/engineering/about/deans-office.aspx"
print("Requesting access to: '%s'" % url_root)
page = requests.get(url_root)
if not page.ok:
    print("An error has occurred with the entered link: %d" % page.status_code)
    exit(1)
print("Request granted")

# initialize XML output
data = ET.Element('URLGraphXML')
# tree = ET.ElementTree(xml_root)




# Parse Webpage with Beautiful soup object
page_source = BeautifulSoup(page.content, 'html.parser')

# Parse root page for subpage links
# Filter non '/engineering' subpages
subpages = [url_root]  # root is first element
for tag in page_source.find_all(href=re.compile("^/engineering")):  # locate all engineering pages
    if '/engineering' in tag['href']:
        url = 'https://www.usf.edu'+str(tag['href'])
        if re.search(re_aspx, url) and url not in subpages:  # check if a webpage and reject redundancies
            subpages.append(url)

print("Scanning for links...")
print("    (root)%s\n    " % subpages[0], end='')
print(*subpages[1:], sep="\n    ")
print("Pages found (%d)" % len(subpages))

def parsePage(element, url):
    email_matches = re.findall(re_emailLink, page_source)
    phone_matches = re.findall(re_phoneNumber, page_source)
    return

root_page = ET.SubElement(data, 'root', url=url_root)
data.append(root_page)


# parse page source for regex matches using regex object
print("\nRoot URL: " + url_root)
i = 1
for url in subpages:
    page = requests.get(url)
    page_source = str(BeautifulSoup(page.content, 'html.parser'))
    email_matches = re.findall(re_emailLink, page_source)
    phone_matches = re.findall(re_phoneNumber, page_source)
    if i == 1:
        print("    Emails: ", end='')
        print(email_matches)
        print("    Phone#: ", end='')
        print(phone_matches)
        i = 0
    if not email_matches and not phone_matches:
        continue
    print("Link: "+url)
    Child_URL = ET.fromstring("<URL = >"+str(url)+"</URL>")
    root_URL.append(Child_URL)
    print("    Emails: ", end='')
    print(email_matches)
    Email = ET.fromstring("<email>"+str(email_matches)+"</email>")
    Child_URL.append(Email)
    print("    Phone#: ", end='')
    print(phone_matches)
    Phone = ET.fromstring("<phone>"+str(phone_matches)+"</phone>")
    Child_URL.append(Phone)

exit(0)
print("Generating URL Graph...")
tree = ET.ElementTree(xml_root)
tree.write("output.xml")
print("Graph successfully generated.")
