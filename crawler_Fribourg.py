from bs4 import BeautifulSoup, Comment
import re
import requests
import json
from collections import OrderedDict
import random #for assigning mock categories
import date_helper_fribourg as dh_f

# output file
file = open("output/output-fribourg.json", 'w')

# translation mappings
translation = open("translations.json", 'r')
mapping = json.load(translation)
# translation mappings
mapping_keys = open("mapping_keys.json", 'r')
mapping2 = json.load(mapping_keys)

# all courses; from here, visit each sport and from there, each course
all_courses = 'http://www3.unifr.ch/sportuni/de/sportangebot/angebot-nach-aktivitaet.html'
courseprefix = 'http://www3.unifr.ch/sportuni/de/'

#category and uni objects
fri = {"Name": "Fribourg", "Code": "FRI"}
mock1 = {"Name": "Mock Category 1", "Code": "MOCK1"}
mock2 = {"Name": "Mock Category 2", "Code": "MOCK2"}
mock3 = {"Name": "Mock Category 3", "Code": "MOCK3"}

# helper function to remove all comments in a html document. https://stackoverflow.com/questions/23299557/beautifulsoup-4-remove-comment-tag-and-its-content
def deleteComments(data):
    for element in data(text=lambda text: isinstance(text, Comment)):
        element.extract()


# visit each sport page individually, compile list of all sports in distinctsports.
def scrapeMainPage(data):
    soup = BeautifulSoup(data, 'lxml')
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
            scrapeOneSport(req.content.decode('utf-8'))
        else:
            print('Could not load content of ' + link)


def scrapeOneSport(data):
    soup = BeautifulSoup(data, 'html5lib')
    print(soup.h2.get_text().strip())  # title of the sport
    individualCourses = soup.find_all(class_='box bg-grey-light')
    for c in individualCourses:
        l = re.search('cours.html\?cid=(\d*)&back=', c.get('onclick'))  # individual links
        if (l):
            cr = requests.get(courseprefix + 'sportangebot/cours.html?cid=' + l.group(1))  # course request
            if cr.status_code == 200:
                scrapeOneCourse(cr.content.decode('utf-8'), courseprefix + 'sportangebot/cours.html?cid=' + l.group(1))
            else:
                print('Could not load content of ' + courseprefix + 'sportangebot/cours.html?cid=' + l.group(1))


def scrapeOneCourse(data, link):
    soup = BeautifulSoup(data, 'html5lib')
    deleteComments(soup)
    sport = soup.h2.get_text().strip()
    table_data = [[cell.get_text() for cell in row("td")] for row in soup("tr")]
    datetime1 = ".*\d{2}\.\d{2}\.\d{4} \d{2}:\d{2} - \d{2}:\d{2}.*"
    datetime1re = re.compile(r'' + datetime1, re.DOTALL)  # course ends on same day
    datetime2 = ".*\d{2}\.\d{2}\.\d{4} \d{2}:\d{2} - \D{2} \d{2}\.\d{2}\.\d{4} \d{2}:\d{2}.*"
    datetime2re = re.compile(r'' + datetime2, re.DOTALL)  # course ends on different day
    jsonattr = []
    dates = []
    for row in table_data:
        if (len(row) == 2):
            jsonattr.append(row)
        elif (len(row) > 2 and re.match(datetime1re, row[0]) != None):
            d = re.match(datetime1re, row[0])[0].strip()
            dd = d[3:22] + d[3:14] + d[22:27]
            dates.append(dh_f.returnNiceDate(dd))
            #dates.append(d[3:22] + d[3:14] + d[22:27])  # format the date nicely
        elif (len(row) > 2 and re.match(datetime2re, row[0]) != None):
            d = re.match(datetime2re, row[0])[0].strip()
            dd = d[3:22] + d[25:41]
            dates.append(dh_f.returnNiceDate(dd))
            #dates.append(d[3:22] + d[25:41])  # format the date nicely
    if (len(dates) == 0):
        jsonattr.append(["Continuous", True])
    else:
        jsonattr.append(["Continuous", False])
    jsonattr.append(["Sport", sport])
    jsonattr.append(["Uni", fri])
    r = random.random()
    if (r < 0.3):
        jsonattr.append(["Category", mock1])
    elif (r < 0.7):
        jsonattr.append(["Category", mock2])
    else:
        jsonattr.append(["Category", mock3])
    jsonattr.append(["Link", link])
    jsonattr.append(["Dates", dates])


    # translate attributes according to mapping
    for attribute in jsonattr:
        if mapping[attribute[0]]:
            attribute[0] = mapping2[mapping[attribute[0]]]

    thiscourse = json.dumps(OrderedDict(jsonattr), sort_keys=False, indent=4)
    file.write(thiscourse)
    file.write(',\n')


try:
    r = requests.get(all_courses)
    if r.status_code == 200:
        file.write('[')
        scrapeMainPage(r.content.decode('utf-8'))
        file.write(']') #you have to manually delete the last comma
        file.close()
        print('---done---')
    else:
        print('Could not load content of ' + all_courses)
except requests.exceptions.ConnectionError as connErr:
    print('Error! Probably the url does not exist.')
    print(connErr)
except Exception as e:
    print(e)
