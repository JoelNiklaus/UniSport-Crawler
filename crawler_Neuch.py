from bs4 import BeautifulSoup
import requests
import json
from collections import OrderedDict
import re
import date_helper_bern as dh_b #custom helper function for the rather nasty dates
import random

#page with all courses
startpage = 'http://www10.unine.ch/sun/types/disciplines/'

datesregex = r'du\s(\d{1,2})\s(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\sau\s(\d{1,2})\s(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(\s\d{4})?'
timeregex = r'((Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)((\s|\xa0)?:(\s|\xa0)?)?\d{2}h(\d{2})?((\s|\xa0)?–(\s|\xa0)?|(\s|\xa0)?-(\s|\xa0)?)\d{2}h(\d{2})?)' # used to include ?P<sport_regex>(?=.*) right after very first bracket

#go through all pages
def goThroughPages(startpage):
    r = requests.get(startpage)
    soup = BeautifulSoup(r.content, 'lxml')
    next = soup.find(class_='navigation-next')
    if next != None:
        handle_page(next['href'])
        goThroughPages(next['href'])
    else:
        print('Import finished.')

#one page of sports
def handle_page(page):
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'lxml')
    sports = soup.find_all(class_='work-details')
    for sport in sports:
        print(sport.a['title'] + ": " + sport.a['href'] + "")
        handle_sport(sport.a['href'])

# one sport
def handle_sport(sport_url):
    r = requests.get(sport_url)
    soup = BeautifulSoup(r.content, 'lxml')
    attrs = soup.find(class_='entry-content clearfix')
    attributes = []
    for attr in attrs.find_all('a'):
        attributes.append(attr.contents[0])
    panes = soup.find_all(class_='pane')
#    for pane in panes:
#        print (pane.contents[0])

    for i in range(0,min(len(attributes), len(panes))):
        if(len(panes[i].contents) > 0): # some panes are empty, e.g. "Prix" for "Zumba"
            print (str(attributes[i]) + ": " + panes[i].contents[0].get_text())
            dates = re.match(datesregex, panes[i].contents[0].get_text())
            if dates != None:
                print ("--- " + str(dates.groups()))
            times = re.findall(timeregex, panes[i].contents[0].get_text())
            if(times != None):
                for time in times:
                    print ("--- " + time[0])
    print("\n")
goThroughPages(startpage)
