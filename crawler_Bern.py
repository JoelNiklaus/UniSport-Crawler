from bs4 import BeautifulSoup
import requests
import json
from collections import OrderedDict
import re
import date_helper_bern as dh_b #custom helper function for the rather nasty dates
import random

#search result containing links to all courses
all_courses = 'http://www.zssw.unibe.ch/usp/zms/sportangebot/suche/index_ger.html'

#courses found above look like this:
example_url = 'http://www.zssw.unibe.ch/usp/zms/angebot/7428/index_ger.html'

bern = {"Name": "Bern", "Code": "BE"}
mock1 = {"Name": "Mock Category 1", "Code": "MOCK1"}
mock2 = {"Name": "Mock Category 2", "Code": "MOCK2"}
mock3 = {"Name": "Mock Category 3", "Code": "MOCK3"}

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
    title = re.search(r'Portal: (.*) - Universität Bern', soup.title.string).group(1)
    print(title) #track progress while parsing
    course = soup.table
    return toJSON(course, originalLink, title)

def toJSON(data, originalLink, title):
    table_data = [[cell.get_text() for cell in row("td")] for row in data("tr")]
    table_data.append(['link', originalLink])
    table_data.append(['sport', title])
    table_data.append(['university', bern])
    r = random.random()
    if (r < 0.3):
        table_data.append(["category", mock1])
    elif (r < 0.7):
        table_data.append(["category", mock2])
    else:
        table_data.append(["category", mock3])
    dates = dh_b.extractDates(table_data)
    table_data.append(['dates', dates])

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

with open('output/output-bern.json', 'w') as file:
    data = makeRequest(all_courses)
    links = getLinks(data)
    file.write('[')
    for link in links:
        data = makeRequest(link)
        coursedata = scrape(data, link)
        file.write(coursedata + ",\n")
    file.write(']') #you have to manually delete the last comma
    file.close()

print('Done loading data.')