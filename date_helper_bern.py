from datetime import date, datetime, timedelta
import re

#Uni Bern phases:
ph1_start  = date(2017,8,21)
ph1_end    = date(2017,9,17)
ph2_start  = date(2017,9,18)
ph2_end    = date(2017,12,23)
ph3_start  = date(2018,1,8)
ph3_end    = date(2017,2,18)
ph4a_start = date(2018,2,19)
ph4a_end   = date(2018,4,3)
ph4b_start = date(2018,4,8)
ph4b_end   = date(2018,6,3)
ph5_start  = date(2018,6,4)
ph5_end    = date(2018,7,1)

delta_day = timedelta(days=1)
delta_week = timedelta(days=7)

winter_begin = date(2017,10,29)
winter_end = date(2018,3,24)

sameday = ".*\d{2}:\d{2}-\d{2}:\d{2}.*"
samedayre = re.compile(r'' + sameday, re.DOTALL)                # 12:30-15:45
oneday = ".*\d{2}\.\d{2}\.\d{4}.*"
onedayre = re.compile(r'' + oneday, re.DOTALL)                  # 12.12.2017
samemonth = ".*\d{2}\. - \d{2}\.\d{2}\.\d{4}.*"
samemonthre = re.compile(r'' + samemonth)                       # 05. - 06.12.2017
sameyear = ".*\d{2}\.\d{2}\. - \d{2}\.\d{2}\.\d{4}.*"
sameyearre = re.compile(r'' + sameyear)                         # 12.11. - 13.12.2017
differentyear = ".*\d{2}.\d{2}.\d{4} - \d{2}.\d{2}\.\d{4}.*"
differentyearre = re.compile(r'' + differentyear)               # 15.12.2017 - 20.01.2018
phases = "(.*\|){4}.*"
phasesre = re.compile(r'' + phases)                             #  1  |  2  |  3  |  4  |  5

#returns the weekday number (0-6) for a given German weekday name
def weekday(plain):
    if(plain == 'Montag'):
        return 0
    elif(plain == 'Dienstag'):
        return 1
    elif(plain == 'Mittwoch'):
        return 2
    elif(plain == 'Donnerstag'):
        return 3
    elif(plain == 'Freitag'):
        return 4
    elif(plain == 'Samstag'):
        return 5
    elif(plain == 'Sonntag'):
        return 6
    else:
        return None

#returns all dates between a start and end date
#that are on a given weekday
def weekdaysbetween(startdate, enddate, weekday):
    dates = []
    day = startdate
    #go to day of first instance
    while (day.weekday() != weekday):
        day = day + delta_day
    #advance in steps of a week
    while(day <= enddate):
        dates.append(day.strftime("%Y-%m-%d"))
        day = day + delta_week
    return dates

#extract date information from a list of Uni Bern-style key-value pairs
def getCoordinates (table_data):
    fld_day, fld_time, fld_period = None, None, None

    for item in table_data:
        if item[0] == 'day':
            fld_day = item[1]
        elif item[0] == 'time':
            fld_time = item[1]
        elif item[0] == 'date':
            fld_period = item[1]
    return fld_day, fld_time, fld_period

#for a given table, returns an array with all exact dates and times
def extractDates(table_data):
    fld_day, fld_time, fld_period = getCoordinates(table_data)
    nicedates = []
    days = []

    # if course is always on the same day, and not multi-day
    if(weekday(fld_day) != None):
        day = weekday(fld_day)
        if (re.match(differentyearre, fld_period) != None):                 # 15.12.2017 - 20.01.2018
            days = weekdaysbetween(date(int(fld_period[6:10]), int(fld_period[3:5]), int(fld_period[0:2])),
                                   date(int(fld_period[19:23]), int(fld_period[16:18]), int(fld_period[13:15])), day)
        elif (re.match(sameyearre, fld_period) != None):                    # 12.11. - 13.12.2017
            days = weekdaysbetween(date(int(fld_period[15:19]), int(fld_period[3:5]), int(fld_period[0:2])),
                                   date(int(fld_period[15:19]), int(fld_period[12:14]), int(fld_period[9:11])), day)
        elif(re.match(samemonthre, fld_period) != None):                    # 05. - 06.12.2017
            days = weekdaysbetween(date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[0:2])),
                                   date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[6:8])), day)
        elif(re.match(oneday, fld_period)):                                 # 12.12.2017
            days.append(fld_period[6:10] + "-" + fld_period[3:5] + "-" + fld_period[0:2])
        elif(re.match(phasesre, fld_period) != None):                       #  1  |  2  |  3  |  4  |  5
            if('1' in fld_period):
                for dd in weekdaysbetween(ph1_start, ph1_end, day):
                    days.append(dd)
            if('2' in fld_period):
                for dd in weekdaysbetween(ph2_start, ph2_end, day):
                    days.append(dd)
            if('3' in fld_period):
                for dd in weekdaysbetween(ph3_start, ph3_end, day):
                    days.append(dd)
            if('4' in fld_period):
                for dd in weekdaysbetween(ph4a_start, ph4a_end, day):
                    days.append(dd)
                for dd in weekdaysbetween(ph4b_start, ph4b_end, day):
                    days.append(dd)
            if('5' in fld_period):
                for dd in weekdaysbetween(ph5_start, ph5_end, day):
                    days.append(dd)

        for d in days:
            dt = date(int(d[0:4]), int(d[5:7]), int(d[8:10]))
            winter = False
            if (dt >= winter_begin and dt <= winter_end):
                winter = True
            nicedate = {}
            if(fld_time != None):
                if(fld_time == "ganzer Tag"):                                   # ganzer Tag
                    if(winter):
                        nicedate["from"] = d + 'T' + '00:00:00+01:00'
                        nicedate["to"] = d + 'T' + '23:59:59+01:00'
                    else:
                        nicedate["from"] = d + 'T' + '00:00:00+02:00'
                        nicedate["to"] = d + 'T' + '23:59:59+02:00'
                elif(re.match(samedayre, fld_time) != None):                    # 05:45-06:30
                    if(winter):
                        nicedate["from"] = d + 'T' + fld_time[0:5] + ':00+01:00'
                        nicedate["to"] = d + 'T' + fld_time[6:11] + ':00+01:00'
                    else:
                        nicedate["from"] = d + 'T' + fld_time[0:5] + ':00+02:00'
                        nicedate["to"] = d + 'T' + fld_time[6:11] + ':00+02:00'
            else:                                                               # no time specified - treated as whole day
                if (winter):
                    nicedate["from"] = d + 'T' + '00:00:00+01:00'
                    nicedate["to"] = d + 'T' + '23:59:59+01:00'
                else:
                    nicedate["from"] = d + 'T' + '00:00:00+02:00'
                    nicedate["to"] = d + 'T' + '23:59:59+02:00'
            nicedates.append(nicedate)
        return nicedates

    # if course is multi-day
    else:
        nicedates = []
        sportdays = []
        startdays = []
        enddays = []
        if('-' in fld_day and len(fld_day) > 1):                                    # Montag-Sonntag
            days = fld_day.split('-')
            if(not (weekday(days[0]) == 0 and weekday(days[1]) >= 4)): # if condition true => continuous
                if (re.match(differentyearre, fld_period) != None):                 # 15.12.2017 - 20.01.2018
                    startdays = weekdaysbetween(date(int(fld_period[6:10]), int(fld_period[3:5]), int(fld_period[0:2])),
                                           date(int(fld_period[19:23]), int(fld_period[16:18]), int(fld_period[13:15])), weekday(days[0]))
                    enddays = weekdaysbetween(date(int(fld_period[6:10]), int(fld_period[3:5]), int(fld_period[0:2])),
                                           date(int(fld_period[19:23]), int(fld_period[16:18]), int(fld_period[13:15])), weekday(days[1]))
                elif (re.match(sameyearre, fld_period) != None):                    # 12.11. - 13.12.2017
                    startdays = weekdaysbetween(date(int(fld_period[15:19]), int(fld_period[3:5]), int(fld_period[0:2])),
                                           date(int(fld_period[15:19]), int(fld_period[12:14]), int(fld_period[9:11])), weekday(days[0]))
                    enddays = weekdaysbetween(date(int(fld_period[15:19]), int(fld_period[3:5]), int(fld_period[0:2])),
                                           date(int(fld_period[15:19]), int(fld_period[12:14]), int(fld_period[9:11])), weekday(days[1]))
                elif(re.match(samemonthre, fld_period) != None):                    # 05. - 06.12.2017
                    startdays = weekdaysbetween(date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[0:2])),
                                           date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[6:8])), weekday(days[0]))
                    enddays = weekdaysbetween(date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[0:2])),
                                           date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[6:8])), weekday(days[1]))
                elif(re.match(phasesre, fld_period) != None):                       #  1  |  2  |  3  |  4  |  5
                    if ('1' in fld_period):
                        for dd in weekdaysbetween(ph1_start, ph1_end, weekday(days[0])):
                            startdays.append(dd)
                        for dd in weekdaysbetween(ph1_start, ph1_end, weekday(days[1])):
                            enddays.append(dd)
                    if ('2' in fld_period):
                        for dd in weekdaysbetween(ph2_start, ph2_end, weekday(days[0])):
                            startdays.append(dd)
                        for dd in weekdaysbetween(ph2_start, ph2_end, weekday(days[1])):
                            enddays.append(dd)
                    if ('3' in fld_period):
                        for dd in weekdaysbetween(ph3_start, ph3_end, weekday(days[0])):
                            startdays.append(dd)
                        for dd in weekdaysbetween(ph3_start, ph3_end, weekday(days[1])):
                            enddays.append(dd)
                    if ('4' in fld_period):
                        for dd in weekdaysbetween(ph4a_start, ph4a_end, weekday(days[0])):
                            startdays.append(dd)
                        for dd in weekdaysbetween(ph4b_start, ph4b_end, weekday(days[0])):
                            startdays.append(dd)
                        for dd in weekdaysbetween(ph4a_start, ph4a_end, weekday(days[1])):
                            enddays.append(dd)
                        for dd in weekdaysbetween(ph4b_start, ph4b_end, weekday(days[1])):
                            enddays.append(dd)
                    if ('5' in fld_period):
                        for dd in weekdaysbetween(ph5_start, ph5_end, weekday(days[0])):
                            startdays.append(dd)
                        for dd in weekdaysbetween(ph5_start, ph5_end, weekday(days[1])):
                            enddays.append(dd)

                if(weekday(days[0]) < weekday(days[1])):
                    for i in range(0, len(startdays)):
                        nicedate = {}

                        #start date
                        sdate = date(int(startdays[i][0:4]), int(startdays[i][5:7]), int(startdays[i][8:10]))
                        winter = False
                        if (sdate >= winter_begin and sdate <= winter_end):
                            winter = True
                        if winter:
                            nicedate["from"] = startdays[i] + 'T00:00:00+01:00'
                        else:
                            nicedate["from"] = startdays[i] + 'T00:00:00+02:00'

                        #end date
                        edate = date(int(enddays[i][0:4]), int(enddays[i][5:7]), int(enddays[i][8:10]))
                        winter = False
                        if (edate >= winter_begin and edate <= winter_end):
                            winter = True
                        if winter:
                            nicedate["to"] = enddays[i] + 'T23:59:59+01:00'
                        else:
                            nicedate["to"] = enddays[i] + 'T23:59:59+02:00'
                        nicedates.append(nicedate)
                else:
                    if(len(startdays) == 1):
                        nicedate = {}
                        # start date. We have to reverse here, because the start date is later in the week
                        sdate = date(int(startdays[0][0:4]), int(startdays[0][5:7]), int(startdays[0][8:10]))
                        winter = False
                        if (sdate >= winter_begin and sdate <= winter_end):
                            winter = True
                        if winter:
                            nicedate["from"] = enddays[0] + 'T00:00:00+01:00'
                        else:
                            nicedate["from"] = enddays[0] + 'T00:00:00+02:00'

                        edate = date(int(enddays[0][0:4]), int(enddays[0][5:7]), int(enddays[0][8:10]))
                        winter = False
                        if (edate >= winter_begin and edate <= winter_end):
                            winter = True
                        if winter:
                            nicedate["to"] = startdays[0] + 'T23:59:59+01:00'
                        else:
                            nicedate["to"] = startdays[0] + 'T23:59:59+02:00'
                        nicedates.append(nicedate)
                    else:
                        for i in range(0, len(startdays)-1):
                            nicedate = {}

                            #start date
                            sdate = date(int(startdays[i][0:4]), int(startdays[i][5:7]), int(startdays[i][8:10]))
                            winter = False
                            if (sdate >= winter_begin and sdate <= winter_end):
                                winter = True
                            if winter:
                                nicedate["from"] = startdays[i] + 'T00:00:00+01:00'
                            else:
                                nicedate["from"] = startdays[i] + 'T00:00:00+02:00'

                            #end date
                            edate = date(int(enddays[i+1][0:4]), int(enddays[i+1][5:7]), int(enddays[i+1][8:10]))
                            winter = False
                            if (edate >= winter_begin and edate <= winter_end):
                                winter = True
                            if winter:
                                nicedate["to"] = enddays[i+1] + 'T23:59:59+01:00'
                            else:
                                nicedate["to"] = enddays[i+1] + 'T23:59:59+02:00'
                            nicedates.append(nicedate)
            else:
                return "CONT"   # if the offer is always on

        # sport takes place on two different (not necessarily adjacent) days every week
        elif('/' in fld_day):                                              # Montag/Dienstag
            days = fld_day.split('/')
            firstday, secondday = weekday(days[0]), weekday(days[1])
            if (re.match(differentyearre, fld_period) != None):  # 15.12.2017 - 20.01.2018
                for day in weekdaysbetween(date(int(fld_period[6:10]), int(fld_period[3:5]), int(fld_period[0:2])),
                                           date(int(fld_period[19:23]), int(fld_period[16:18]), int(fld_period[13:15])),
                                           firstday):
                    sportdays.append(day)
                for day in weekdaysbetween(date(int(fld_period[6:10]), int(fld_period[3:5]), int(fld_period[0:2])),
                                           date(int(fld_period[19:23]), int(fld_period[16:18]), int(fld_period[13:15])),
                                           secondday):
                    sportdays.append(day)
            elif (re.match(sameyearre, fld_period) != None):  # 12.11. - 13.12.2017
                for day in weekdaysbetween(date(int(fld_period[15:19]), int(fld_period[3:5]), int(fld_period[0:2])),
                                        date(int(fld_period[15:19]), int(fld_period[12:14]), int(fld_period[9:11])),
                                           firstday):
                    sportdays.append(day)
                for day in weekdaysbetween(date(int(fld_period[15:19]), int(fld_period[3:5]), int(fld_period[0:2])),
                                      date(int(fld_period[15:19]), int(fld_period[12:14]), int(fld_period[9:11])),
                                          secondday):
                    sportdays.append(day)
            elif (re.match(samemonthre, fld_period) != None):  # 05. - 06.12.2017
                for day in weekdaysbetween(date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[0:2])),
                                        date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[6:8])),
                                           firstday):
                    sportdays.append(day)
                for day in weekdaysbetween(date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[0:2])),
                                      date(int(fld_period[12:16]), int(fld_period[9:11]), int(fld_period[6:8])),
                                           secondday):
                    sportdays.append(day)

            elif (re.match(phasesre, fld_period) != None):  # 1  |  2  |  3  |  4  |  5
                if ('1' in fld_period):
                    for dd in weekdaysbetween(ph1_start, ph1_end, firstday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph1_start, ph1_end, secondday):
                        sportdays.append(dd)
                if ('2' in fld_period):
                    for dd in weekdaysbetween(ph2_start, ph2_end, firstday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph2_start, ph2_end, secondday):
                        sportdays.append(dd)
                if ('3' in fld_period):
                    for dd in weekdaysbetween(ph3_start, ph3_end, firstday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph3_start, ph3_end, secondday):
                        sportdays.append(dd)
                if ('4' in fld_period):
                    for dd in weekdaysbetween(ph4a_start, ph4a_end, firstday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph4b_start, ph4b_end, firstday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph4a_start, ph4a_end, secondday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph4b_start, ph4b_end, secondday):
                        sportdays.append(dd)
                if ('5' in fld_period):
                    for dd in weekdaysbetween(ph5_start, ph5_end, firstday):
                        sportdays.append(dd)
                    for dd in weekdaysbetween(ph5_start, ph5_end, secondday):
                        sportdays.append(dd)

            for d in sportdays:
                nicedate = {}
                dd = date(int(d[0:4]), int(d[5:7]), int(d[8:10]))
                winter = False
                if (dd >= winter_begin and dd <= winter_end):
                    winter = True
                if(re.match(samedayre, fld_time) != None):                    # 05:45-06:30
                    if(winter):
                        nicedate["from"] = d + 'T' + fld_time[0:5] + ':00+01:00'
                        nicedate["to"] = d + 'T' + fld_time[6:11] + ':00+01:00'
                    else:
                        nicedate["from"] = d + 'T' + fld_time[0:5] + ':00+02:00'
                        nicedate["to"] = d + 'T' + fld_time[6:11] + ':00+02:00'
                else:
                    if winter:
                        nicedate["from"] = d + 'T00:00:00+01:00'
                        nicedate["to"] = d + 'T23:59:59+01:00'
                    else:
                        nicedate["from"] = d + 'T00:00:00+02:00'
                        nicedate["to"] = d + 'T23:59:59+02:00'
                nicedates.append(nicedate)
        else:
            return "NEVER" # if no date is set

        return nicedates