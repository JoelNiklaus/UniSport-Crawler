from bs4 import BeautifulSoup
import re
import requests
#import lxml
#import html5lib
import json
from collections import OrderedDict

#all courses
#from here, visit each sport and from there, each course
all_courses = 'http://www3.unifr.ch/sportuni/de/sportangebot/angebot-nach-aktivitaet.html'
courseprefix = 'http://www3.unifr.ch/sportuni/de/'

#courses found above look like this:
#starting_url = 'http://www.zssw.unibe.ch/usp/zms/angebot/7428/index_ger.html'

#visit each sport page individually.
#compile list of all sports in distinctsports.
def scrapeMainPage(data):
    soup = BeautifulSoup(data, 'lxml') # alternatives are 'html5lib' or html.parser
    sports = soup.find_all(class_='link-list')
    sportsaslist = []
    for lst in sports:
        thislist = lst.find_all('a')
        for item in thislist:
            sportsaslist.append(item)
    for item in sportsaslist:
        link = courseprefix + item.get('href')
        req = requests.get(link)
        if req.status_code == 200:
            scrapeOneCourse(req.content.decode('utf-8'))
        else:
            print('Could not load content of ' + link)

def scrapeOneCourse (data):
    soup = BeautifulSoup(data, 'html5lib')
    print(soup.h2.get_text().strip()) #title of the sport
    print()
    print(soup.find_all(class_='tabcordion')) #most of the info is here; we also have to follow the link in the javascript.onclick event





#def toJSON(data):
#    table_data = [[cell.get_text() for cell in row("td")] for row in data("tr")]
#    #json_data = json.dumps(OrderedDict(table_data))
#    thiscourse = json.dumps(OrderedDict(table_data), sort_keys=False, indent=4)
#    return thiscourse

try:
    r = requests.get(all_courses)
    if r.status_code == 200:
        scrapeMainPage(r.content.decode('utf-8'))
    else:
        print('Could not load content of ' + all_courses)
except requests.exceptions.ConnectionError as connErr:
    print('Error! Probably the url does not exist.')
    print(connErr)
except Exception as e:
    print(e)
