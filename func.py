

from datetime import datetime as dt, time
import re
import datetime
import dateutil.relativedelta as REL
import os
from pathlib import Path
import sqlite3
import socket
from pathlib import Path
import datetime

from AnomalyPromptGRP.config import LOG_PATH,FULL_LOG_PATH,SQLITE_DIRS
from AnomalyPromptGRP.ricaLicense import genLicense


# BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_sqlite_con_dir():
    con = None
    for dir_ in SQLITE_DIRS:
        try:
            # print("CONNECTING TO PARAMETERS DATABASE... ",dir_)
            sqlite_dir =  os.path.join(dir_, "db_params.sqlite3") 
            sqlite3.connect(sqlite_dir)
            con = dir_
            print("PARAMS DB CONNECTED: ",dir_)
            break
        except Exception as e:
            pass
            # print("PARAMETERS DB NOT CONNECTED")
    return con


def get_ip():
    hostname = socket.gethostname()
    return f"http://{socket.gethostbyname(hostname)}:3000"

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


# def create_rule(rule,schedule_time):
#     sqlite_dir =  os.path.join(SQLITE_DIR if SQLITE_DIR else BASE_DIR, "db_params.sqlite3") 
#     try:

#         con = sqlite3.connect(sqlite_dir)
#         cur = con.cursor() 

#         # Create a table
#         cur.execute('''CREATE TABLE IF NOT EXISTS running_rules (
#                             rule TEXT PRIMARY KEY,
#                             schedule_time TEXT
#                     )''')


#         rules = [(rule,schedule_time)]

#         cur.executemany('INSERT INTO running_rules VALUES (?, ?)', rules)
#         con.commit()
#         con.close()
#     except:
#         pass


def clean_emails(emails):
    # Remove duplicates
    # unique_emails = list(set(emails))
    
    # Remove invalid emails
    # cleaned_emails = []
    # for email in unique_emails:
    #     if re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #         cleaned_emails.append(email)
    
    # return cleaned_emails
    return emails


def is_time_between(begin_time: time, end_time: time, check_time: time = None, both=False, output=False):
    """ 

    """

    check_time = check_time or dt.utcnow().time()

    if both:
        result: bool = check_time >= begin_time and check_time <= end_time
        a = 'both'
    else:
        a = ''
        result: bool = check_time >= begin_time and check_time < end_time

    if output:
        print(a)
        print("For", check_time)
        print("from", begin_time)
        print("To", end_time)
        print("Result", result)

    if begin_time < end_time:
        return result
    else:
        return result


def convert_time(time: str = None, output=False):
    """ This convert time to a more usuable format for use i.e 

        >>> convert_time('05:21PM') 
        >>> convert_time('04:54AM') 

        '05:21PM' -----> 17:21:00 
        '04:54AM' ----> 04:54:00 
    """
    now = dt.utcnow().strftime('%I:%M%p')
    time = time or now
    date_time_obj = dt.strptime(time, '%I:%M%p').time()

    if output:
        print('Inputted Time:', date_time_obj)
        print('Current time:', now)

    return date_time_obj

# def execute_list(cursor,query):
#     res = execute(text(query))
#     result = []
#     for i in res:
#         result.append(i)
#     return result


def to_number(string):
    return string.replace('-',"").replace(":","")

def format_int(x):
    """ This function checks if the variable passed in the function is none and return 0 else it returns back the same variable unchanged """
    if type(x) is not str:
        res = int(0 if x is None else x)
    else:
        res = x
    return res


def format_int_bin(x):
    res = 1 if x < 1 and type(x) is not str else x
    return res


def get_first(item):
    if len(item) > 0:
        return item[0]
    else:
        return ""

def get_query_fields(entryRecordList=[]):
    try:
        return [ x for x in list(entryRecordList[0].keys()) if x and x not in ["special_date","special_time"]]
    except IndexError:
        return []

def get_last(item):
    if len(item) > 0:
        return item[len(item)-1]
    else:
        return ""


def clean(string=''):
    if string:
        return re.sub(r'[-:\s\.]*', "", str(string))
    else:
        return ""


def remove_tuple_comma(data=()):
    data = tuple(set(data))
    return str(data).replace(",)", ")")

def getExceptionsData(execute,account_no,branch):

    alerts = f"""
     select distinct A.ricaAlertId, 
                                convert(varchar(10), ricaCreateDate,120) AS ricaCreateDate, 
                            ricaNetLossAmount,ricaRiskAssessment,ricaDisposition,ricaScenario,ricaScenarioId,ricaFlowType
                            from rica_alerts A
                            where ricaAlertId IN ( select distinct T.ricaAlertId
                                                    from rica_alertsconcat T
                                                    where T.ricaAccountNo='{account_no}' 
                                                    and T.ricaBranchId='{branch}'
                                                    and T.ricaAlertId = A.ricaAlertId)
                                                     """
    # print('here===1',alerts) 

    cases = f"""
        select distinct ricaCaseId, 
                 convert(varchar(10), ricaCreateDate,120) AS ricaCreateDate, 
            ricaNetLossAmount,ricaRiskAssessment,ricaDisposition,ricaScenario,ricaScenarioId,ricaFlowType
            from rica_cases
            where ricaAccountNo='{account_no}' 
            AND ricaPublishBy <> 'null'
        """

    return list(execute(alerts))+list(execute(cases))


def getAlarm(execute):
    alarm = f"""  select * from rica_risk_alarm
           """
    alarm = execute(alarm)
    return get_first(alarm)


def get_footer_label(execute):

    footer = execute(f""" 
         select ricaFooterLabel from rica_mail_alerts_spf 
     """)
    footer = get_first(footer)
    return footer.get('ricaFooterLabel') if footer else ""



 

def get_user(execute, user_id, key=None,is_active="",many=False):
    if is_active:
        query = f""" 
         select   ricaUserId,
        ricaUserEmail,
        ricaCoverages,
        ricaUserRole,ricaUserTitle,ricaFirstName,ricaMiddleName,ricaLastName
        ricaUserStatus from rica_user
             where (
              ricaUserId = '{user_id}'
              OR ricaAlternativeUserId = '{user_id}'
              )
             and ricaUserStatus = '{is_active}'
         """

    else:
        query = f""" 
             select   ricaUserId,
        ricaUserEmail,
        ricaCoverages,
        ricaUserRole,ricaUserTitle,ricaFirstName,ricaMiddleName,ricaLastName
        ricaUserStatus from rica_user
             where (
              ricaUserId = '{user_id}'
              OR ricaAlternativeUserId = '{user_id}'
              )
         """

    # print(query)
    userRecord = execute(query)
    if many:
        return userRecord
    else:
        if len(userRecord) == 0:
            return ""
        if key:
            return get_first(userRecord)[key]
        else:
            return get_first(userRecord)



def get_from_account(execute, accountId, key):

    account = execute(f""" 
         select * from rica_account
                           Where RICAACCOUNTNO = '{accountId}'
    """)

    account = get_first(account)

    if account:
        return account[key]


def get_from_branch(execute, branchId, key):

    query = f"""
        select * from rica_branch
        Where RICABRANCHID = '{branchId}'
    """
    # print(query)
    branch = execute(query)
    

    branch = get_first(branch)
    if branch:
        return branch[key]


def remove_None(string):
    print('ren=k', string)
    if string == "None" or not string:
        return ''

    return string


def get_from_cluster(execute, clusterId, key):

    cluster = execute(f"""
         select * from rica_cluster
                           Where RICACLUSTER = '{clusterId}'
     """)

    cluster = get_first(cluster)
    if cluster:
        return cluster[key]


def get_from_zone(execute, zoneId, key):

    zone = execute(f"""
         select * from rica_zone
                           Where RICAZONE = '{zoneId}'
     """)

    zone = get_first(zone)
    if zone:
        return zone[key]


def get_actual_designate_from_user(execute, user_id, key="RICAUSERROLE"):
    user = execute(f""" 
         select * from rica_user
                           Where RICAUSEREMAIL = '{user_id}'
     """)

    user = get_first(user)
    if user:
        return user[key]


 

def get_user_via_designate(execute, designate,branchCode, key="ricaUserId",many=False):
    try:
        if branchCode == "": 
            get_branch_info = f"""
                        select ricaCluster,ricaBranchId,ricaZone,ricaRegion from rica_branch 
            """
        else:
            get_branch_info = f"""
                    select ricaCluster,ricaBranchId,ricaZone,ricaRegion from rica_branch
            where ricaBranchid='{branchCode}'
            """
            

        get_branch_info = execute(get_branch_info)

        transform_branch = [ f'BRANCH*{x["ricaBranchId"]}' for x in get_branch_info]
        transform_cluster = [ f'CLUSTER*{x["ricaCluster"]}' for x in get_branch_info]
        transform_zone = [ f'ZONE*{x["ricaZone"]}' for x in get_branch_info]
        transform_region = [ f'REGION*{x["ricaRegion"]}' for x in get_branch_info]

        query= f""" 
             select ricaUserId, ricaCoverage,ricaDesignate from user_coverages
                    
                    Where  ( RICACOVERAGE IN {remove_tuple_comma(tuple(transform_branch))}
                    OR RICACOVERAGE IN {remove_tuple_comma(tuple(transform_cluster))}
                    OR RICACOVERAGE IN {remove_tuple_comma(tuple(transform_zone))}
                    OR RICACOVERAGE IN {remove_tuple_comma(tuple(transform_region))}
                    OR RICACOVERAGE = 'ALL*BRANCHES'
                    )
                    AND RICADESIGNATE = '{designate}'
         """

        # print(query)
        if len(transform_branch) or len(transform_cluster) or len(transform_zone) or len(transform_region):
            user = execute(query)

            if many:
                return user
            else:
                if key:
                    user = get_first(user)
                    if user:
                        return user[key]
                else:
                    return user 

    except Exception as e:
        print("designate error: ",e)
        return None



def get_designate_via_user(execute, user_id):
    try:
        query= f""" 
        SELECT DISTINCT 
          ricaUserRole FROM rica_user WHERE ricaUserId = '{user_id}'         

         """
        user = execute(query) 
        user = get_first(user) 
        if user:
            return user.get('ricaUserRole')
    except Exception as e:
        return

def get_user_branch_from_journal(execute, user_id,v_lastrundate,v_lastruntime):
    try:
        query= f""" 
         select DISTINCT ricaBranchCode, ricaBranchName from rica_journalentries 
               where RICASPECIALDATE  >= '{v_lastrundate}'
            and RICASPECIALTIME > '{v_lastruntime}'
            and RICAINPUTTER = '{user_id}'         

         """
        user = execute(query) 
        user = get_first(user)  
        return user
    except Exception as e:
        return {}


def get_group_designate(execute, group_id, key="ricaUserId"):
    try:
        if group_id:
            query= f""" 
            SELECT DISTINCT 
              ricaGroupDesignateId, ricaGroupDesignateEmail
            FROM rica_group_designates
            where ricagroupdesignateid IN (SELECT ricaGroup FROM rica_User_Groups WHERE ricaGroup = '{group_id}')           

             """
            user = execute(query) 

            if key:
                user = get_first(user)
                if user:
                    return user[key]
            else:
                return get_first(user)
        else:
            return None
    except Exception as e:
        print(e)
        return None


def get_group_member_emails(execute, group_id,key=None):
    try:
        if key:
            query= f""" 
               SELECT DISTINCT 
              ricaUserEmail
            FROM rica_user
            where ricaUserId IN (SELECT ricaUserId FROM rica_User_Groups WHERE ricaGroup = '{group_id}') 
              and ricaUserStatus LIKE '%109'            

             """
            users = execute(query) 
            return [ x[key] for x in users ]

        else: 
            query=f"""SELECT ricaUserId FROM rica_User_Groups WHERE ricaGroup = '{group_id}'"""
            users = execute(query) 
            return [ x['ricaUserId'] for x in users ]

    except Exception as e:
        return []


def get_respondent_details_from_user(execute, coverage, respondent=''):

    user = execute(f""" 
         select * from rica_user
                           Where RICACOVERAGES = '{coverage}'
                           and RICAUSERROLE = '{respondent}'
     """)

    user = get_first(user)
    if user:
        return user['ricaUserRole']
    else:
        return ""



 


def get_spf(execute,lang="en",query=""):
    spf = query.format(lang=lang) 
    spf = execute(spf)
    return get_first(spf)



def get_from_alertworkflow(execute, v_createstatus, v_riskMatrix, key,ret=None):
    if v_riskMatrix:
        data = execute(f""" 
             select * from alertworkflow_riskid
                               Where RICAALERTSTATUS = '{v_createstatus}'
                               and RICARISKID = '{v_riskMatrix}'
         """)
    else:
        query = f""" 
             select * from alertworkflow_riskid
                               Where RICAALERTSTATUS = '{v_createstatus}'
         """
        data = execute(query)

    data = get_first(data)
    if data:
        return data[key]
    else:
        if v_riskMatrix:
            return "00:00:00"
        else:
            return ret


def get_risk_scoring(execute, v_likelihood, v_consequence):
    data = execute(f""" 
         select * from rica_risk_matrix
                           Where RICALIKELIHOOD = '{v_likelihood}'
                           and RICASEVERITY = '{v_consequence}'
     """)

    data = get_first(data)
    if data:
        return data['ricaRiskCalc']
    else:
        return ""


def get_multi_value(execute, model, _id, ret_key=False):
    query = f"""
         select * from {model}
               Where ricaRuleId = '{_id}'
     """

    value = execute(query)
    if ret_key:
        value = get_first(value)
        if value:
            return value[ret_key]
    else:
        return list(value)


def get_multi_emails(execute, model, _id):
    query = f"""
    Select ricaUserEmail from rica_user
    where ricaUserId IN ( select distinct ricaOtherReceiver from {model}
               Where ricaRuleId = '{_id}')
     """
    # print(query)

    value = execute(query)
    try:
        return list(value)
    except:
        return []


def get_riskmatrix(execute, _id):
    query = f""" 
         select * from rica_risk_matrix
               Where RICAMATRIXID = '{_id}'
     """

    value = execute(query)

    value = get_first(value)
    if value:
        return value['ricaRisk']



def replaceParams(msg="",obj={}):
    for x in obj:
        val = "{"+x+"}"
        msg = re.sub(val,str(obj.get(x) or obj.get(str(x).upper()) ),msg)
    return msg


def removeDuplicates(data,field):
    res = {}
    for x in data:
        if not res.get(x[field]):
            res[x[field]] = x
    return list(res.values())


 


class GenRunDate():
    '''
        Scenario Run Date
    '''

    def __init__(self, params={}):
        self.params = params

        self.run_mode = self.params.get('ricaRunMode')

        merge_date = self.merge_to_datetime(str(self.params.get('ricaLastRunDate')), str(self.params.get('ricaLastRunTime')))
        self.params['ricaLastRunDate'] = merge_date
        self.params['ricaLastRunTime'] = merge_date

        if self.params.get('ricaYearly'):
            self.params['ricaYearly'] = self.merge_to_datetime(str(self.params.get('ricaYearly')))

        self.result = dict()
        self.weeks = {'SUNDAY': 0, 'MONDAY': 1, 'TUESDAY': 2,
                      'WEDNESDAY': 3, 'THURSDAY': 4, 'FRIDAY': 5, 'SATURDAY': 6}
        self.weekdays = {'SUNDAY': REL.SU, 'MONDAY': REL.MO, 'TUESDAY': REL.TU,
                         'WEDNESDAY': REL.WE, 'THURSDAY': REL.TH, 'FRIDAY': REL.FR, 'SATURDAY': REL.SA}

        if not self.run_mode == 'INTERVAL':
            self.daily = self.getNextDate(self.params.get('ricaDaily', [])) if len(
                self.params.get('ricaDaily', [])) > 0 else "00:00"

    def create_date(self, date):
        return datetime.date(date.year, date.month, date.day)

    def create_datetime(self, date):
        return datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

    def create_custom_datetime(self, year, month, day, hour, minute, second=0):
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    def merge_to_datetime(self, date, time=str(datetime.datetime.now())):
        date = str(date)[0:10].split("-")
        time = str(time).split(' ')
        if len(time) > 1:
            time = time[1][0:8].split(":") 
        else:
            time = time[0][0:8].split(":") 
        return self.create_custom_datetime(date[0], date[1], date[2], time[0], time[1], time[2])

    def create_time(self, date):
        return datetime.time(date.hour, date.minute, date.second)

    def getNextDate(self, daily=[]):
        daily.sort()
        now = datetime.datetime.now()
        result = self.params.get('ricaDaily')[0]

        last_time = self.params['ricaLastRunTime']
        last_time = datetime.datetime.strptime(
            str(last_time), "%Y-%m-%d  %H:%M:%S")
        last_time = self.create_datetime(last_time)
        last_time.replace(year=now.year, month=now.month, day=now.day)

        for x in daily:
            date = self.gen_date_from_daily(x)
            if last_time > date:
                continue
            else:
                result = x
                break
        # print(result)
        return result

    def split_date(self, date):
        try:
            format_datetime = datetime.datetime.strptime(
                str(date), "%Y-%m-%d  %H:%M:%S.%f")
        except:
            format_datetime = datetime.datetime.strptime(
                str(date), "%Y-%m-%d  %H:%M:%S")
        
        return {
            'date': self.create_date(format_datetime),
            'time': self.create_time(format_datetime),
        }

    def updatenextrun(self, date):
        split_datetime = self.split_date(date)
        f_date = split_datetime['date']
        f_time = split_datetime['time']

        self.updatelastrun()
        self.result['ricaNextRunDate'] = f_date
        self.result['ricaNextRunTime'] = f_time

    def updatelastrun(self):
        self.result['ricaLastRunDate'] = self.create_date(datetime.date.today())
        self.result['ricaLastRunTime'] = self.create_time(datetime.datetime.now())

    def gen_date_from_daily(self, daily):
        now = datetime.datetime.now()
        split_daily = daily.split(":")
        hour = split_daily[0]
        minute = split_daily[1]
        modify_now = now.replace(hour=int(hour), minute=int(
            minute), second=now.second, microsecond=now.microsecond)
        return modify_now

    def run(self):

        if self.run_mode == 'INTERVAL' and self.params.get('ricaIntervalOf',30):
            print('run mode',self.params.get('ricaLastRunDate'),  datetime.timedelta(minutes=int(self.params['ricaIntervalOf'])), self.params.get('ricaLastRunDate') + datetime.timedelta(minutes=int(self.params['ricaIntervalOf']))  )
            date = self.params.get('ricaLastRunDate') + datetime.timedelta(minutes=int(self.params['ricaIntervalOf']))
            self.updatenextrun(date)

        elif self.run_mode == 'DAILY':
            now = datetime.datetime.now()
            day = self.daily
            modify_now = self.gen_date_from_daily(day)
            if now < modify_now:
                date = modify_now
            else:
                date = now + datetime.timedelta(days=1)
                date = date.replace(hour=modify_now.hour, minute=modify_now.minute,
                                    second=now.second, microsecond=now.microsecond)
            self.updatenextrun(date)

        elif self.run_mode == 'WEEKLY':
            if self.params.get('ricaWeekly'):
                now = datetime.datetime.now()
                day = self.daily
                modify_now = self.gen_date_from_daily(day)

                if self.weeks.get(self.params['ricaWeekly']) == datetime.datetime.today().isoweekday() and now < modify_now:
                    date = modify_now
                else:
                    rd = REL.relativedelta(days=1, weekday=self.weekdays.get(
                        self.params.get('ricaWeekly')))
                    date = now + rd
                    date = date.replace(hour=modify_now.hour, minute=modify_now.minute,
                                        second=now.second, microsecond=now.microsecond)
                self.updatenextrun(date)

        elif self.run_mode == 'MONTHLY':
            if self.params.get('ricaMonthly'):
                now = datetime.datetime.now()
                day = self.daily
                modify_now = self.gen_date_from_daily(day)

                if self.params.get('ricaMonthly') == now.day and now < modify_now:
                    date = modify_now
                else:
                    date = now + REL.relativedelta(months=+1)
                    date = date.replace(day=int(self.params['ricaMonthly']), hour=modify_now.hour,
                                        minute=modify_now.minute, second=now.second, microsecond=now.microsecond)
                self.updatenextrun(date)

        elif self.run_mode == 'YEARLY':
            if self.params.get('ricaYearly'):
                now = datetime.datetime.now()
                modify_now = self.gen_date_from_daily(self.daily)
                year_date = self.create_datetime(self.params.get('ricaYearly'))
                year_date = year_date.replace(
                    year=now.year, hour=now.hour, minute=now.minute, second=now.second, microsecond=now.microsecond)
                if year_date < modify_now:
                    date = year_date.replace(
                        hour=modify_now.hour, minute=modify_now.minute, second=now.second, microsecond=now.microsecond)
                else:
                    date = year_date + REL.relativedelta(years=+ 1)
                    date = date.replace(hour=modify_now.hour, minute=modify_now.minute,
                                        second=now.second, microsecond=now.microsecond)
                self.updatenextrun(date)

        return self.result


check_dicts = {
'ricaRespondent':"ricaDefaultRespondent",
'ricaOwner':"ricaDefaultOwner",
'ricaInvestigator':"ricaDefaultInvestigator",
'ricaNextOwner':"ricaDefaultNextOwner",
}

    



def get_designate_email(execute,post_val="ricaRespondent",scenarioRecord={},spfRecords={},group_field_value="",group_field="",entryRecordList=[]):
    # print('designate', post_val)
    try:
        attr_val = scenarioRecord.get(post_val)
        emails = []
        v_resp= None
        # Check group for post_val, else check designate
        group = get_group_designate(execute, attr_val,None)
        if group:
            v_resp = group["ricaGroupDesignateId"]
            if not group.get("ricaGroupDesignateEmail"):
                member_emails = get_group_member_emails(execute,group["ricaGroupDesignateId"],"ricaUserEmail")
                if len(member_emails) > 0:
                    emails.extend(member_emails)
                else:
                    member_designate = [ find_grouping(x) for x in get_group_member_emails(execute,group["ricaGroupDesignateId"])]
                    for designate in member_designate:
                        if designate == 'branch':
                            v_val = get_user_via_designate(execute, attr_val or spfRecords.get(check_dicts.get(post_val)) ,group_field_value,many=True)   # This is designate
                            if v_val:
                                emails.extend([ get_user(execute, resp.get("ricaUserId"), 'ricaUserEmail',is_active="en-109") for resp in v_val  ])
                            v_resp = attr_val
                        else:
                            for record in entryRecordList:
                                trans_desg_user = record.get(designate)
                                if trans_desg_user and str(record.get(group_field))==str(group_field_value):
                                    emails.append(get_user(execute, trans_desg_user, 'ricaUserEmail',is_active="en-109"))
            else:
                print('GROUP',group)
                emails.append(group["ricaGroupDesignateEmail"])
        else:
            v_val = get_user_via_designate(execute, attr_val or spfRecords.get(check_dicts.get(post_val)) ,group_field_value,many=True)   # This is designate
            # print('v_val',attr_val or spfRecords.get(check_dicts.get(post_val)) ,group_field_value,v_val)
            if v_val and len(v_val):
                emails.extend([ get_user(execute, resp.get("ricaUserId"), 'ricaUserEmail',is_active="en-109") for resp in v_val  ])
            else:
                user_email = get_user(execute,attr_val, 'ricaUserEmail',is_active="en-109")
                if user_email:
                    emails.append(user_email)

            v_resp = attr_val
    except Exception as e:
        print("Get_designate_email Error: ",str(e))

    # print('emails',emails,v_resp)
    return (v_resp, emails)


 
 

def find_grouping(v_groupBy):
    DISTINCT_FIELD = 'branch'
    if v_groupBy.upper() == 'INPUTTER':
        DISTINCT_FIELD = "inputter"
    elif v_groupBy.upper() == 'AUTHORISER':
        DISTINCT_FIELD = 'authoriser'
    elif v_groupBy.upper() == 'VERIFIER':
        DISTINCT_FIELD = 'verifier'
    elif v_groupBy.upper() == 'ACCOUNTOFFICER':
        DISTINCT_FIELD = 'account_officer'
    elif v_groupBy.upper() == 'BRANCH':
        DISTINCT_FIELD = 'branch'
    elif v_groupBy.upper() == 'DEPARTMENT':
        DISTINCT_FIELD = 'branch'
    elif v_groupBy.upper() == 'CLUSTER':
        DISTINCT_FIELD = 'branch'
    elif v_groupBy.upper() == 'ZONE':
        DISTINCT_FIELD = 'branch'
    elif v_groupBy.upper() == 'REGION':
        DISTINCT_FIELD = 'branch'
    elif v_groupBy.upper() == 'CUSTOMER':
        DISTINCT_FIELD = 'RICACUSTOMER'
    elif v_groupBy.upper() == 'ACCOUNT':
        DISTINCT_FIELD = 'account'
    elif v_groupBy.upper() == 'PRODUCT':
        DISTINCT_FIELD = 'RICAPRODUCTCODE'
    elif v_groupBy.upper() == 'TRANSACTION-TYPE':
        DISTINCT_FIELD = 'trans_type'
    elif v_groupBy.upper() == 'ACCOUNT-TYPE':
        DISTINCT_FIELD = 'trans_type'
    elif v_groupBy.upper() == 'CATEGORY':
        DISTINCT_FIELD = 'trans_type'
    return DISTINCT_FIELD



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

    def log(self,log_args={},scenario='RULE_ID'): 
        log_args['ricaLogDate'] = get_date().split("-")[0]
        log_args['ricaLogTime'] = get_date().split("-")[1]
        recordDate = get_date().split('-')[0]
        media_path = os.path.normpath(FULL_LOG_PATH) if FULL_LOG_PATH else os.path.normpath(os.path.expanduser(f"~/{LOG_PATH}")) 
        scenario = scenario.strip()
        create_dir(os.path.join(media_path,'ANOMALY_PROMPTS') )
        create_dir(os.path.join(media_path,'ANOMALY_PROMPTS', f'{scenario}_LOGS'.upper()))
        create_dir(os.path.join(media_path,'ANOMALY_PROMPTS', f'{scenario}_LOGS'.upper(),self.filename))


        res_path =   os.path.join(media_path,'ANOMALY_PROMPTS', f'{scenario}_LOGS'.upper(),self.filename) 


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



def license_expired(spf,DB_SETTINGS):
    db_name = DB_SETTINGS['DATABASE_NAME']
    license_creator3 = genLicense()
    expiry_date = license_creator3.extract_date(spf.get("ricaLicenseCode"))
    no_of_users = license_creator3.extract_noofusers(spf.get("ricaLicenseCode"))  

    license = genLicense(server_name="", mac_addr="",
                         db_name=db_name, expiry_date=expiry_date,no_of_users=no_of_users).verify_license(spf.get("ricaLicenseCode"))
    if license =='VALID':
        return True


def get_expired_notification(spf):
    date1 = datetime.datetime.strptime(spf.get('ricaExpiryDate'), '%Y-%m-%d')
    today = datetime.datetime.now()

    days = (date1 - today).days
    diff = 30 if spf['ricaLicenseNotifyDur'] < 15 else spf['ricaLicenseNotifyDur']

    if days >= 0 and days < diff:
        return ("License will expire ") + (' Today' if days==0 else f'in {days} ') + ("Day" if days ==1 else "Days")
    elif days < 0:
        return "License has expired"
    else:
        return ""





if __name__ == "__main__":  # NORUNTESTS

    last_run_date = datetime.date.today()
    last_run_time = datetime.time(16, 24)
    year = last_run_date + REL.relativedelta(months=+4)
    params = {
        "ricaDaily": ["12:30", "10:12"],
        'ricaLastRunDate': last_run_date,
        'ricaLastRunTime': last_run_time,
        'ricaRunMode': 'WEEKLY',
        'ricaIntervalOf': 5,
        'ricaWeekly': 'MONDAY',
        'ricaMonthly': '13',
        "ricaYearly": year

    }

    # print(GenRunDate(params).run())


