import re
import datetime
#import json
#from collections import OrderedDict

datetime1 = ".*\d{2}\.\d{2}\.\d{4} \d{2}:\d{2} - \d{2}:\d{2}.*"
datetime1re = re.compile(r'' + datetime1, re.DOTALL)  # course ends on same day

#dates =[
#['Di 19.09.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 26.09.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 03.10.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 10.10.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 17.10.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 24.10.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 07.11.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde '],
#['Di 14.11.2017 12:15 - 13:15', 'Séverine Nager Monnard', 'Zweisprachig', 'Sporthalle Miséricorde ']]

# "19.09.2017 12:15 - 19.09.2017 13:15"
# "2015-03-25T12:00:00-06:30"

winter_begin = datetime.date(2017,10,29)
winter_end = datetime.date(2018,3,24)

def returnNiceDate(date):
    nicedate = {}
    # start date
    start = datetime.date(int(date[6:10]), int(date[3:5]), int(date[0:2]))
    # winter time
    if(start >= winter_begin and start <= winter_end):
        nicedate["from"] = date[6:10] + "-" + date[3:5] + "-" + date[0:2] + "T" + date[11:16] + ":00+01:00"
    # summer time
    else:
        nicedate["from"] = date[6:10] + "-" + date[3:5] + "-" + date[0:2] + "T" + date[11:16] + ":00+02:00"

    # end date
    end = datetime.date(int(date[25:29]), int(date[22:24]), int(date[19:21]))
    # start date
    if(end >= winter_begin and end <= winter_end):
        nicedate["to"] = date[25:29] + "-" + date[22:24] + "-" + date[19:21] + "T" + date[30:35] + ":00+01:00"
    # summer time
    else:
        nicedate["to"] = date[25:29] + "-" + date[22:24] + "-" + date[19:21] + "T" + date[30:35] + ":00+02:00"
    return nicedate

################TEST
#dates_new = []
#for row in dates:
#    d = re.match(datetime1re, row[0])[0].strip()
#    dd = d[3:22] + d[3:14] + d[22:27]
#    dates_new.append(returnNiceDate(dd))
#
#dates_final = [["Dates", dates_new]]
#
#print(json.dumps(OrderedDict(dates_final), sort_keys=False, indent=4))
