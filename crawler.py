from bs4 import BeautifulSoup
import requests
#import lxml
#import html5lib
import json
from collections import OrderedDict

#all courses
#from here, visit each sport and from there, each course in tabs "Geleitetes Angebot" and "Geleitetes Training"
all_courses = 'http://www.unibe.ch/universitaet/campus__und__infrastruktur/universitaetssport/sportangebot/sport_a_z/index_ger.html'

#courses found above look like this:
starting_url = 'http://www.zssw.unibe.ch/usp/zms/angebot/7428/index_ger.html'

def scrape(data):
    soup = BeautifulSoup(data, 'lxml') # alternatives are 'html5lib' or html.parser
    soup.unicode
    course = soup.table
    return toJSON(course)

def toJSON(data):
    table_data = [[cell.get_text() for cell in row("td")] for row in data("tr")]
    #json_data = json.dumps(OrderedDict(table_data))
    thiscourse = json.dumps(OrderedDict(table_data), sort_keys=False, indent=4).decode('unicode-escape') #now prints nicely
    return thiscourse

try:
    r = requests.get(starting_url)
    if r.status_code == 200:
        coursedata = scrape(r.content)
        print coursedata
    else:
        print('Could not load content of ' + starting_url)
except requests.exceptions.ConnectionError as connErr:
    print('Error! Probably the url does not exist.')
    print(connErr)
except Exception as e:
    print(e)
