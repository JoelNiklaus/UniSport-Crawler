from bs4 import BeautifulSoup
import requests
import json
from collections import OrderedDict
import re
import date_helper_neuch as dh_n

#page with all courses
startpage = 'http://www10.unine.ch/sun/types/disciplines/'

datesregex = r'du\s(\d{1,2})\s(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\sau\s(\d{1,2})\s(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s)?(\d{4})?'
timeregex = r'((Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)((\s|\xa0)?:(\s|\xa0)?)?\d{2}h(\d{2})?((\s|\xa0)?–(\s|\xa0)?|(\s|\xa0)?-(\s|\xa0)?)\d{2}h(\d{2})?)' # used to include ?P<sport_regex>(?=.*) right after very first bracket

neuch = {"name": "Neuchâtel", "code": "NE"}

# key translation mappings
mapping_keys = open("mapping_keys.json", 'r')
mapping = json.load(mapping_keys)

# mapping for categories
mapping_sports_categories = open("mapping_sports_categories.json", 'r')
mapping_s_c = json.load(mapping_sports_categories)

# sport mappings
mapping_sport = open("mapping_sports_original.json", 'r')
mapping_s = json.load(mapping_sport)

#go through all pages
def goThroughPages(startpage, file):
    r = requests.get(startpage)
    soup = BeautifulSoup(r.content, 'lxml')
    next = soup.find(class_='navigation-next')
    if next != None:
        handle_page(next['href'], file)
        goThroughPages(next['href'], file)
    else:
        print('Import finished.')

#one page of sports
def handle_page(page, file):
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'lxml')
    sports = soup.find_all(class_='work-details')
    for sport in sports:
        handle_sport(sport.a['href'], sport.a['title'], file)

# one sport
def handle_sport(sport_url, title, file):
    r = requests.get(sport_url)
    soup = BeautifulSoup(r.content, 'lxml')
    attrs = soup.find(class_='entry-content clearfix')
    attributes = []
    for attr in attrs.find_all('a'):
        if(attr['href'] == '#'):
            attributes.append(attr.contents[0])
    for i in range(0, len(attributes)):
        if mapping[attributes[i]]:
            attributes[i] = mapping[attributes[i]]

    panes = soup.find_all(class_='pane')
    course = {}
    d = None
    t = []
    for i in range(0,min(len(attributes), len(panes))):
        if(len(panes[i].contents) > 0): # some panes are empty, e.g. "Prix" for "Zumba"
            course[str(attributes[i])] = panes[i].contents[0].get_text().replace('\xa0', ' ')
            dates = re.match(datesregex, panes[i].contents[0].get_text())
            if dates != None:
                d = dates.groups()
            times = re.findall(timeregex, panes[i].contents[0].get_text())
            if(times != None):
                for time in times:
                    t.append(re.sub(r'\s+', '', time[0].replace('\xa0', '').replace('-', ':').replace('–', ':')))
    if(d != None and len(t) > 0):
        print (title)

        # add ever-present attributes
        course['sport'] = mapping_s[title]
        course['sportOriginal'] = title
        course['link'] = sport_url
        dates = dh_n.nice_dates(d, t)
        course['dates'] = dates
        course['university'] = neuch
        course['continuous'] = False
        course['category'] = mapping_s_c[title]
        course_json = json.dumps(OrderedDict(course), sort_keys=False, indent=4)
        file.write(course_json + ",\n")

with open('output/output-neuch.json', 'w') as file:
    file.write('[')
    goThroughPages(startpage, file)
    file.write(']') #you have to manually delete the last comma
    file.close()