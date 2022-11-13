import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
import os

########################
# FUNCTION DEFINITIONS #
########################

# Regex-based parsing
# Fetches page content and parses for:
#  - Emails
#  - Phone numbers
# Returns a jagged array of data in the order listed above
def parsePage(url):
    page_fetch = requests.get(url)
    page_source = str(BeautifulSoup(page_fetch.content, 'html.parser'))
    email_matches = re.findall(re_emailLink, page_source)
    phone_matches = re.findall(re_phoneNumber, page_source)

    return (email_matches, phone_matches)

# Appends a jagged array data matrix to an XML parent node
# Each row index in the matrix must correlate to each index of elementList
# Elements of each matrix row are appended to their respective elementList
# Returns nothing
def appendToXML(parent, dataMatrix, elementList):
    for i, dataRow in enumerate(dataMatrix):
        tag = elementList[i].tag.split('_')[0]
        for dataCol in dataRow:
            ET.SubElement(elementList[i], tag).text = dataCol


################
#     MAIN     #
################

# compile regex pattern into regex objects
re_emailLink = re.compile(r"(?<=mailto:)[0-9a-zA-Z.+-_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}")  # matches the email format defined in RFC
re_phoneNumber = re.compile(r"\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}")  # matches the standard email formats
re_aspx = re.compile(r"\.aspx$")  # matches .aspx websites

# accessing root URl
url_root = "https://www.usf.edu/engineering/about/deans-office.aspx"
print("Requesting access to: '%s'" % url_root)
page_fetch = requests.get(url_root)
if not page_fetch.ok:
    print("An error has occurred with the entered link: %d" % page_fetch.status_code)
    exit(1)
print("Request granted")

# initialize XML output
data = ET.Element('URLGraphXML')
tree = ET.ElementTree(data)

# extract page content into BeautifulSoup object
page_source = BeautifulSoup(page_fetch.content, 'html.parser')

# parse root page for subpage links
# filter non '/engineering' webpages (ASPX)
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


# Collect data for root page
page_source = str(page_source)
root_page = ET.SubElement(data, 'root', url=url_root)
email_matches = re.findall(re_emailLink, page_source)
phone_matches = re.findall(re_phoneNumber, page_source)
data_matrix = (email_matches, phone_matches)
email_list = ET.SubElement(root_page, 'email_list')
phone_list = ET.SubElement(root_page, 'phone_list')
element_list = (email_list, phone_list)

appendToXML(root_page, data_matrix, element_list)
print("\nRoot URL: %s" % url_root)
print("    Emails: ", end='')
print(data_matrix[0])
print("    Phone#: ", end='')
print(data_matrix[1])

# parse page source for regex matches using regex object
for url in subpages[1:]:
    # create url node
    subpage = ET.SubElement(root_page, 'subpage', url=url)

    # parse url for data
    data_matrix = parsePage(url)

    # skip url if parsing returned no data
    if not data_matrix:
        continue

    # create sub elements to categorize data
    email_list = ET.SubElement(subpage, 'email_list')
    phone_list = ET.SubElement(subpage, 'phone_list')
    element_list = (email_list, phone_list)

    # append data matrix to xml tree
    appendToXML(subpage, data_matrix, element_list)

    # print data to console
    print("Link: %s" % url)
    print("    Emails: ", end='')
    print(data_matrix[0])
    print("    Phone#: ", end='')
    print(data_matrix[1])

# generate xml tree
print("\nGenerating URL Graph...")


# write tree to file
filename = "output.xml"
tree.write(filename)

# print file link to console
dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
print("Graph successfully generated: file:///"+dir_path+"/%s" % filename)