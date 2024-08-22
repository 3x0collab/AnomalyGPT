from datetime import datetime as dt
import datetime
from dateutil.relativedelta import relativedelta
import re
format_date = "%Y%m%d"
format_date2 = "%Y-%m-%d"
 


def insertDatHelper(todayData, eachData,column='',type=""):
    for key in todayData:
        if (key != 'metric' and key != 'Total'):
            if (column == key):
                if (type == 'amount'):
                    todayData = { **todayData,key: int(todayData[key]) + int(eachData.get('amount')) }
                else:
                    todayData = { **todayData, key: int(todayData[key]) +1}          

    return todayData

def create_date(date):
    if not date:
        return None
    if type(date) ==str: 
        try:
            date = dt.strptime(date,format_date)
        except:
            date = dt.strptime(date,format_date2)
        return datetime.date(date.year,date.month,date.day) 
    else:
        return  datetime.date(date.year,date.month,date.day)


def isToday(date):
    return create_date(dt.now()) == create_date(date)


def isWhatD(transition_date,fromdate=1,todate=7,label=""):
    dt = datetime.datetime    
    transition_date = create_date(transition_date)
    now = dt.now()

    fromdate =  now +  datetime.timedelta(days=fromdate) if label == 'ToExpire' else  now - datetime.timedelta(days=fromdate)
    fromdate = create_date(fromdate)

    todate = now +  datetime.timedelta(days=todate) if label == 'ToExpire' else  now - datetime.timedelta(days=todate) 
    todate = create_date(todate)

    return transition_date >= todate and transition_date <= fromdate 

    
def isLastD_M(transition_date,fromdate,tomonth,label=""):
    dt = datetime.datetime 
    transition_date=create_date(transition_date)
    now = dt.now()

    fromdate = now +  datetime.timedelta(days=fromdate) if label == 'ToExpire' else now -  datetime.timedelta(days=fromdate) 
    fromdate = create_date(fromdate)

    tomonth = now + relativedelta(months=+tomonth) if label == 'ToExpire' else now - relativedelta(months=+tomonth)
    tomonth = create_date(tomonth)

    return transition_date >= tomonth and transition_date <= fromdate 


def isWhatM(transition_date,frommonth,tomonth,label=""):
    dt = datetime.datetime 
    transition_date = create_date(transition_date)
    now = dt.now()

    frommonth = now +  relativedelta(months=+frommonth) if label == 'ToExpire' else now -  relativedelta(months=+frommonth)
    frommonth = create_date(frommonth)

    tomonth = now + relativedelta(months=+tomonth) if label == 'ToExpire' else now - relativedelta(months=+tomonth) 
    tomonth = create_date(tomonth)

    return transition_date > tomonth and transition_date < frommonth 

def isOver5Y(transition_date,frommonth,label=""):
    dt = datetime.datetime 
    transition_date = create_date(transition_date)
    now = dt.now()
    frommonth = now +  relativedelta(months=+frommonth) if label == 'ToExpire' else  now -  relativedelta(months=+frommonth)
    frommonth = create_date(frommonth)
    return transition_date < frommonth






def dateSplit(results,objKey,eachData,type_="amount"):
    endDate = None    
    print(str(eachData.get("special_date")))

    if isToday(str(eachData.get("special_date"))):
      if type_ == 'map_amount':
        eachData['RICADATETYPE'] = 'Today'
        return eachData      

        results[objKey] = insertDatHelper(results[objKey], eachData, "Today",type_)

    
    if isWhatD(str(eachData.get("special_date")),1,7):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = '2 - 7 Days'
            return eachData

        results[objKey] = insertDatHelper(results[objKey], eachData, '2 - 7 Days',type_)

    
    if isWhatD(str(eachData.get("special_date")),8,14):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = '8 - 14 Days'
            return eachData

        results[objKey] = insertDatHelper(results[objKey], eachData, '8 - 14 Days',type_)


    if isWhatD(str(eachData.get("special_date")),15,28):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = '15 - 28 Days'
            return eachData

        results[objKey] = insertDatHelper(results[objKey], eachData, '15 - 28 Days',type_)
    
    if isLastD_M(str(eachData.get("special_date")),29,3):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = '29 Days - 3 Months'
            return eachData
      
        results[objKey] = insertDatHelper(results[objKey], eachData, '29 Days - 3 Months',type_)
    

    if isWhatM(str(eachData.get("special_date")),3,6):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = 'Above 3 Months - 6 Months'
            return eachData

        results[objKey] = insertDatHelper(results[objKey], eachData, 'Above 3 Months - 6 Months',type_)
    

    if isWhatM(str(eachData.get("special_date")),6,12):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = 'Above 6 Months - 1 Year'
            return eachData

        results[objKey] = insertDatHelper(results[objKey], eachData, 'Above 6 Months - 1 Year',type_)
    

    if isWhatM(str(eachData.get("special_date")),12,12*3):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = 'Above 1 Year - 3 Years'
            return eachData
      
        results[objKey] = insertDatHelper(results[objKey], eachData, 'Above 1 Year - 3 Years',type_)
    

    if isWhatM(str(eachData.get("special_date")),12*3,12*5):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = 'Above 3 Years - 5 Years'
            return eachData
      
        results[objKey] = insertDatHelper(results[objKey], eachData, 'Above 3 Years - 5 Years',type_)
    


    if isOver5Y(str(eachData.get("special_date")),12*5):
        if type_ == 'map_amount':
            eachData['RICADATETYPE'] = 'Above 5 Years'
            return eachData
      
        results[objKey] = insertDatHelper(results[objKey], eachData, 'Above 5 Years',type_)
    

    return results
