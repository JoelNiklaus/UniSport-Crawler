from datetime import date, timedelta, datetime

delta_day = timedelta(days=1)
delta_week = timedelta(days=7)

winter_begin = date(2017,10,29)
winter_end = date(2018,3,24)

def iswinter(dt):
    if (dt >= winter_begin and dt <= winter_end):
        return True
    return False

#returns the weekday number (0-6) for a given French weekday name
def weekday(plain):
    if(plain == 'Lundi'):
        return 0
    elif(plain == 'Mardi'):
        return 1
    elif(plain == 'Mercredi'):
        return 2
    elif(plain == 'Jeudi'):
        return 3
    elif(plain == 'Vendredi'):
        return 4
    elif(plain == 'Samedi'):
        return 5
    elif(plain == 'Dimanche'):
        return 6
    else:
        return None

#returns the weekday number (0-6) for a given French weekday name
def month(plain):
    if(plain == 'janvier'):
        return 1
    elif(plain == 'février'):
        return 2
    elif(plain == 'mars'):
        return 3
    elif(plain == 'avril'):
        return 4
    elif(plain == 'mai'):
        return 5
    elif(plain == 'juin'):
        return 6
    elif(plain == 'juillet'):
        return 7
    elif(plain == 'août'):
        return 8
    elif(plain == 'septembre'):
        return 9
    elif(plain == 'octobre'):
        return 10
    elif(plain == 'novembre'):
        return 11
    elif(plain == 'décembre'):
        return 12
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

def nice_dates(dates, times):
    alldates = []
    beginday = dates[0]
    beginmonth = month(dates[1])
    endday = dates[2]
    endmonth = month(dates[3])

    for time in times:
        params = time.split(':')
        fromtime, totime = "00:00:00", "23:59:59"
        if len(params[1]) == 5:
            fromtime = params[1][0:2] + ':' + params[1][3:5] + ':00'
        else:
            fromtime = params[1][0:2] + ':00:00'
        if len(params[2]) == 5:
            totime = params[2][0:2] + ':' + params[2][3:5] + ':00'
        else:
            totime = params[2][0:2] + ':00:00'

        sportdates = weekdaysbetween(date(2017, beginmonth, int(beginday)), date(2017, endmonth, int(endday)), weekday(params[0]))

        for sportdate in sportdates:
            nicedate = {}
            if iswinter(date(int(sportdate[0:4]), int(sportdate[5:7]), int(sportdate[8:10]))):
                nicedate['from'] = sportdate + "T" + fromtime + "+01:00"
                nicedate['to'] = sportdate + "T" + fromtime + "+01:00"
            else:
                nicedate['from'] = sportdate + "T" + totime + "+02:00"
                nicedate['to'] = sportdate + "T" + totime + "+02:00"
            alldates.append(nicedate)
    return alldates