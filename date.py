
from datetime import datetime as dt
now = dt.now()
import datetime
from dateutil.relativedelta import relativedelta



def date_func(now=dt.now()):
    ''' This function gets current time and date {now}'''
    run_time = now.strftime('%H:%M:%S.%f %p')
    # run_date = now.strftime("%d-%b-%y")
    run_date = now.strftime('yyyy-mm-dd')
    return run_time,run_date

run_time, run_date = date_func()

# print(run_time)
# print(run_date)

date = now.strftime('yyyy-mm-dd')
# print(date)


def create_datetime(date,minute= 0):
    if not date:
        return None
    return datetime.datetime(date.year,date.month,date.day,date.hour,date.minute,date.second) + datetime.timedelta(minutes=int(minute))

def create_date(date,repl=None):
    if not date:
        return None
    return  str(datetime.date(date.year,date.month,date.day)).replace(repl,"") if repl else datetime.date(date.year,date.month,date.day)

def create_time(date,repl=None):
    if not date:
        return None
    return str(datetime.time(date.hour,date.minute)).replace(repl,"")[0:4] if repl else datetime.time(date.hour,date.minute,date.second)

def calculate_remindcounter(date = datetime.datetime.now(),counter=0):
    v_date = date +  datetime.timedelta(minutes=int(counter))
    return {
        'date':create_date(v_date),
        'time':create_time(v_date),
        }


def calculate_duedate(date,overduetime = 24*60):
    v_date = create_datetime(date,overduetime)
    return {
        'date':create_date(v_date),
        'time':create_time(v_date),
        }



def getToday():
    now = datetime.datetime.now()
    today =  create_date(now)
    return (today,'==')

def isWhatD(v_nextrundate,fromdate,todate,label=""):
    dt = datetime.datetime    
    now = v_nextrundate
    fromdate =  now +  datetime.timedelta(days=fromdate) if label == 'ToExpire' else  now - datetime.timedelta(days=fromdate)
    fromdate = create_date(fromdate)

    todate = now +  datetime.timedelta(days=todate) if label == 'ToExpire' else  now - datetime.timedelta(days=todate) 
    todate = create_date(todate)

    return (fromdate,todate,'>=')

    
def isLastD_M(v_nextrundate,fromdate,tomonth,label=""):
    dt = datetime.datetime 
    now = v_nextrundate
    fromdate = now +  datetime.timedelta(days=fromdate) if label == 'ToExpire' else now -  datetime.timedelta(days=fromdate) 
    fromdate = create_date(fromdate)

    tomonth = now + relativedelta(months=+tomonth) if label == 'ToExpire' else now - relativedelta(months=+tomonth)
    tomonth = create_date(tomonth)

    return (fromdate,tomonth,'>=')


def isWhatM(v_nextrundate,frommonth,tomonth,label=""):
    dt = datetime.datetime 
    now = v_nextrundate
    frommonth = now +  relativedelta(months=+frommonth) if label == 'ToExpire' else now -  relativedelta(months=+frommonth)
    frommonth = create_date(frommonth)

    tomonth = now + relativedelta(months=+tomonth) if label == 'ToExpire' else now - relativedelta(months=+tomonth) 
    tomonth = create_date(tomonth)

    return (frommonth,tomonth,'>')

def isOver5Y(v_nextrundate,frommonth,label=""):
    dt = datetime.datetime 
    now = v_nextrundate
    frommonth = now +  relativedelta(months=+frommonth) if label == 'ToExpire' else  now -  relativedelta(months=+frommonth)
    frommonth = create_date(frommonth)

    return (frommonth,'>')

