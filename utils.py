from datetime import datetime as dt, time
import re
import datetime
import dateutil.relativedelta as REL
import os
from pathlib import Path
from SNow.config import FULL_LOG_PATH,SQLITE_DIRS
import sqlite3


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



def gen_str(string):
    return str(string) if len(str(string)) > 1 else '0{}'.format(string)


def create_dir(path):
    if not os.path.exists(path):
        try: 
            os.mkdir(path) 
        except OSError as error:
            print('filepath error: ',error)



def get_date():
    now = datetime.datetime.now()
    ricaRecordDate = '{}{}{}'.format(
        now.year, gen_str(now.month), gen_str(now.day))
    ricaRecordTime = '{}:{}:{}'.format(
        gen_str(now.hour), gen_str(now.minute), gen_str(now.second))
    date_time = "{}-{}".format(ricaRecordDate, ricaRecordTime)
    return date_time


class logError():
    def __init__(self,filename=""):
        self.filename = str(filename)

    def log(self,log_args={},folder='RULE_ID'): 
        log_args['ricaLogDate'] = get_date().split("-")[0]
        log_args['ricaLogTime'] = get_date().split("-")[1]
        recordDate = get_date().split('-')[0]
        media_path = FULL_LOG_PATH
        
        create_dir(os.path.join(media_path,'ETL_SERVICES') )
        create_dir(os.path.join(media_path,'ETL_SERVICES', f'{folder}'.upper()))
        create_dir(os.path.join(media_path,'ETL_SERVICES', f'{folder}'.upper(),self.filename))


        res_path =   os.path.join(media_path,'ETL_SERVICES', f'{folder}'.upper(),self.filename) 


        try:
            filepath = os.path.join(res_path,recordDate.replace("-",""))
            if not os.path.exists(filepath+".txt"):
                header = list(log_args.keys())

                with open(filepath+".txt", "a") as fobj:
                    for x in header:
                        fobj.write(f"{x}|")
                    fobj.write('\n---------------------------------------------------------------------------------')

            with open(filepath+".txt", "a") as fobj:
                fobj.write("\n")
                for x in log_args.keys():
                    fobj.write(f"{log_args[x]}|")
            print('logged',filepath) 

        except Exception as e:
            print('log fail',e) 



def get_sqlite_con_dir():
    con = None
    for dir_ in SQLITE_DIRS:
        try:
            # print("CONNECTING TO PARAMETERS DATABASE... ",dir_)
            sqlite_dir =  os.path.join(dir_, "db_params.sqlite3") 
            sqlite3.connect(sqlite_dir)
            con = dir_
            # print("PARAMS DB CONNECTED: ",dir_)
            break
        except Exception as e:
            pass
            # print("PARAMETERS DB NOT CONNECTED")
    return con

def get_env_settings():
    DB_SETTINGS = {}
    try:
        con = sqlite3.connect(os.path.join(get_sqlite_con_dir(), "db_params.sqlite3")  )
        cur = con.cursor() 
        for row in cur.execute('SELECT * FROM SettingsParameter;'):
            DB_SETTINGS[row[0]] = row[1]
        con.close()
    except:
        pass
    return DB_SETTINGS



def send_email_error(service, error, spf={}):

    try:
        subject = f'{spf.get("ricaAppsId")}: [URGENT] Error in Rica Etl Payload Service Database Connection'
        html_content = service.get('MESSAGE',f"""
        <pre> 
        Hi,

        An error has cropped up with the database connection service. It's failing to connect due to possible configuration or connectivity problems. See the error below:

        {error}

        Please look into it urgently.

        Best regards.
        </pre>
        """).format(error=error) 
        

        recipient_list = str(service.get("ADMIN_EMAILS",spf.get("ADMIN_EMAILS"))).replace(" ","").split(",")

        from_email = spf.get("ricaStmpMailUser") or  spf.get("FROM_EMAIL")  
        host=spf.get("ricaStmpMailServer") 
        port= 587 if 'ionos' in spf.get("ricaStmpMailServer","") else  spf.get("ricaStmpMailPort")
        username=spf.get("ricaStmpMailUser")  
        password=spf.get("ricaStmpMailPassword")  
        to = []
        cc = []

        if isinstance(recipient_list,dict):
            to =   recipient_list.get('to',[]) 
            cc =   recipient_list.get('cc',[])

        else:
            to =  recipient_list
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = ','.join(to)
        msg['Cc'] = ','.join(cc)  

        print('from_email',from_email)
        print('port',port)

        html  = html_content
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        
        try:
            print('send mail to', to,cc)
            service = smtplib.SMTP(host, int(port))
            service.connect(host, int(port))
            service.ehlo()
            if str(port)=='587' or str(port)=='465' :
                service.starttls()
                service.login(username, password)

            service.sendmail(from_email,to+cc, msg.as_string())
            service.quit()
            print('mail sent')

        except Exception as e:
            print('mail error', e)
    except Exception as e:
        print("mail function braeak",e)