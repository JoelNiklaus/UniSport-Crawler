import os
from bs4 import BeautifulSoup
import requests
#import lxml
#import html5lib
import json
from collections import OrderedDict
import re

#search result containing links to all courses
all_courses = 'http://www.zssw.unibe.ch/usp/zms/sportangebot/suche/index_ger.html'

#courses found above look like this:
example_url = 'http://www.zssw.unibe.ch/usp/zms/angebot/7428/index_ger.html'


def getLinks(data):
    soup = BeautifulSoup(data, 'lxml')
    links = []
    for link in soup.find_all('a'):
        linkText = link.get('href')
        pattern = re.compile("/angebot/\d{4}") # angebot and containing 4 digit number
        if isinstance(linkText, str) and pattern.search(linkText):
            links.append("http:"+linkText) #append link to list
    return links

def scrape(data, originalLink = ''):
    soup = BeautifulSoup(data, 'lxml') # alternatives are 'html5lib' or html.parser
    course = soup.table
    return toJSON(course, originalLink)

def toJSON(data, originalLink):
    table_data = [[cell.get_text() for cell in row("td")] for row in data("tr")]
    table_data.append(['Originaler Link', originalLink])
    thiscourse = json.dumps(OrderedDict(table_data), sort_keys=False, indent=4)
    return thiscourse

def makeRequest(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.content.decode('utf-8')
        else:
            print('Could not load content of ' + url)
    except requests.exceptions.ConnectionError as connErr:
        print('Error! Probably the url does not exist.')
        print(connErr)
    except Exception as e:
        print(e)


#data = makeRequest(example_url)
#coursedata = scrape(data)
#print(coursedata)

with open('output-bern.json', 'w') as file:
    print('Making Request to ' + all_courses + ' ...')
    data = makeRequest(all_courses)
    print('Extracting links ...')
    links = getLinks(data)
    print('Downloading Course Data ...')
    for link in links:
        data = makeRequest(link)
        coursedata = scrape(data, link)
        file.write(coursedata + ",\n")
    # delete last comma
    file.seek(-1, os.SEEK_END)
    file.truncate()

print('Done loading data.')