from bs4 import BeautifulSoup
import requests
import json
from collections import OrderedDict
import re
import date_helper_bern as dh_b #custom helper function for the rather nasty dates
import random

#search result containing links to all courses
all_courses = 'http://www.zssw.unibe.ch/usp/zms/sportangebot/suche/index_ger.html'
#all_courses = 'http://www.unibe.ch/universitaet/campus__und__infrastruktur/universitaetssport/sportangebot/sport_a_z/index_ger.html'

#courses found above look like this:
example_url = 'http://www.zssw.unibe.ch/usp/zms/angebot/7428/index_ger.html'

# translation key mappings
mapping_keys = open("mapping_keys.json", 'r')
mapping = json.load(mapping_keys)

# mapping for categories
mapping_sports_categories = open("mapping_sports_categories.json", 'r')
mapping_s_c = json.load(mapping_sports_categories)

# sport mappings
mapping_sport = open("mapping_sports_original.json", 'r')
mapping_s = json.load(mapping_sport)

bern = {"name": "Bern", "code": "BE"}

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

    # translate attributes according to mapping
    for attribute in table_data:
        if mapping[attribute[0]]:
            attribute[0] = mapping[attribute[0]]

    # add ever-present attributes
    table_data.append(['link', originalLink])
    table_data.append(['sport', mapping_s[title]])
    table_data.append(['sportOriginal', title])
    table_data.append(['university', bern])
    table_data.append(['category', mapping_s_c[title]])
    dates = dh_b.extractDates(table_data)
    if dates == 'CONT':
        table_data.append(["continuous", True])
    else:
        table_data.append(["continuous", False])
    if dates != 'NEVER' and dates != 'CONT':
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