from datetime import date, datetime, timedelta
import re

#Uni Bern phases:
ph1_start  = date(2017,8,21)
ph1_end    = date(2017,9,17)
ph2_start  = date(2018,1,8)
ph2_end    = date(2017,12,23)
ph3_start  = date(2018,2,19)
ph3_end    = date(2017,2,18)
ph4a_start = date(2018,2,19)
ph4a_end   = date(2018,4,3)
ph4b_start = date(2018,4,8)
ph4b_end   = date(2018,6,3)
ph5_start  = date(2018,6,4)
ph5_end    = date(2018,7,1)

delta_day = timedelta(days=1)
delta_week = timedelta(days=7)

samedaytime = "\d{2}:\d{2}-\d{2}:\d{2}"
samedaytimere = re.compile(r'' + samedaytime, re.DOTALL)  # course has a defined start and end time on same day

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
        dates.append(day.strftime("%d.%m.%Y"))
        day = day + delta_week
    return dates

#extract date information from a list of Uni Bern-style key-value pairs
def getCoordinates (table_data):
    fld_day, fld_time, fld_period = None, None, None
    #fld_time = None
    #fld_period = None

    for item in table_data:
        if item[0] == 'Tag':
            fld_day = item[1]
        elif item[0] == 'Zeit':
            fld_time = item[1]
        elif item[0] == 'Datum/Phase':
            fld_period = item[1]
    return fld_day, fld_time, fld_period

#for a given table, returns an array with all exact times
def extractDates(table_data):
    dates = []
    fld_day, fld_time, fld_period = getCoordinates(table_data)
    if(weekday(fld_day) != None):
        print (fld_time)
        print (fld_period)


#    if(fld_time == None):
#        print ('NO DATES')
#        return dates
#    elif(fld_time == 'ganzer Tag'):
#        print('ganzer Tag')
#    elif(re.match(samedaytimere, fld_time) != None):
#        print('startet und endet am selben Tag')
##    else:
#       print("PROBLEM! NEW CASE! " + fld_time)


#table_data = [['Tag', 'Dienstag'], ['Zeit', '12:15-13:30'], ['Datum/Phase', ' 1  |  2  |  3  |  4  |  5 '], ['Ort', 'ATRIUM12 Raum Beta'], ['Leistungsniveau', 'B'], ['Inhalt/Programm', 'Der Live-Perkussionist Ibrahim\xa0Ndiaye begleitet mit seinen Perkussionsinstrumenten die Tänzerinnen und Tänzer im Training.'], ['Teilnahmevoraussetzungen', 'In den ersten drei Semesterwochen des Herbst- und Frühjahrssemesters ist ein unverbindliches Reinschnuppern (mit gültigem Unisportausweis resp. UNICARD) möglich. Danach wird eine lückenlose Teilnahme erwünscht.'], ['Anmeldung', 'Ohne Anmeldung'], ['Anzahl freie Plätze', 'Unbeschränkt'], ['Ausrüstung', 'Bequeme Sportbekleidung; Afro Dance\xa0wird barfuss getanzt.'], ['Leitung des Angebots', 'Cornelia KaiserIbrahima Ndiaye'], ['Links', 'www.afrotanz.ch'], ['Unterrichtssprache', 'Deutsch'], ['Bereichsleitung', 'Simone Büchi']]

#extractDates(table_data)
