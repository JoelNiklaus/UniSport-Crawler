from bs4 import BeautifulSoup
import requests
import lxml
import html5lib
import json
from collections import OrderedDict


starting_url = 'http://www.zssw.unibe.ch/usp/zms/angebot/7428/index_ger.html'


def scrape(data):
    soup = BeautifulSoup(data, 'lxml') # alternatives are 'html5lib' or html.parser

    course = soup.table

    print(course.prettify())
    print(course.get_text())

    return toJSON(course)



def toJSON(data):
    table_data = [[cell.text for cell in row("td")] for row in data("tr")]
    print(table_data)
    json_data = json.dumps(OrderedDict(table_data))
    print(json_data)
    return json_data

try:
    r = requests.get(starting_url)
    if r.status_code == 200:
        scrape(r.content)

    else:
        print('Could not load content of ' + starting_url)
except requests.exceptions.ConnectionError as connErr:
    print('Error! Probably the url does not exist.')
    print(connErr)
except Exception as e:
    print(e)


