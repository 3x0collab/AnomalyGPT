import sys
import os
# import django
# sys.path.append(r'E:\rica\backend\bots')
# os.environ['DJANGO_SETTINGS_MODULE'] ='ricabackend.settings'
# django.setup()
from AnomalyPromptGRP.db_client import create_connection
from AnomalyPromptGRP.func import get_env_settings,get_ip,logError,replaceParams
from AnomalyPromptGRP.func import convert_time, format_int, format_int_bin, is_time_between, get_first, get_last, clean,GenRunDate,get_query_fields,get_multi_value,get_spf,get_footer_label,clean_emails,find_grouping,license_expired,get_expired_notification
from AnomalyPromptGRP.datahelper import getChart3Data,getLineChartData,generateAnalytics
from AnomalyPromptGRP.date import date_func, create_date, create_time
from AnomalyPromptGRP.doc import make_doc, create_trans_bar_chart, create_trans_pie_chart
from AnomalyPromptGRP.xlsx import create_lite_excel
from AnomalyPromptGRP.first import  step_1, step_2, step_4,  step_3,step_6,get_status
from AnomalyPromptGRP.config import LOG_PATH,FULL_LOG_PATH,STATUS,MAP
from AnomalyPromptGRP.common import load_queries
import re
from pathlib import Path
import datetime
from datetime import time 
import argparse 
import time 
from urllib.parse import urljoin
path = os.getcwd()
sys.path.append(path)
import json
import threading
# mysql get close after each query
from gpt4all import GPT4All
model = GPT4All(r'C:\anomalyGPT\llm\model.gguf',allow_download=False)

class AlertService():

    def __init__(self,rule):

        self.env_settings = get_env_settings()
        self.cursor = create_connection(MAP)
        self.scenario = rule


        self.APP_URL = self.env_settings.get("APP_URL",get_ip())
        self.BACKEND_URL = self.env_settings.get("BACKEND_URL",get_ip())

    
    def fetchAllWIthColumns(self,cursor):
        "Return all rows from AnomalyPromptGRP.a self.cursor as a dict"
        columns = [MAP.get(col[0], co[l0]) for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]



    def update_rica_scenarios(self,scenarioRecord,execute=None):
        copy_data = {}
        try:
            copy_data['ricaRunMode'] = scenarioRecord['ricaRunMode'] or "INTERVAL"  
            copy_data['ricaLastRunDate'] = scenarioRecord['ricaLastRunDate'] or datetime.date.today().strftime("%Y-%m-%d")
            copy_data['ricaLastRunTime'] = scenarioRecord['ricaLastRunTime'] or datetime.datetime.now().strftime("%H:%M:%S")

            # scenario_date = GenRunDate({**scenarioRecord,**copy_data}).run()

            # if scenario_date.get('ricaLastRunDate'): 
            #     last_run_date = scenario_date.get('ricaLastRunDate')
            #     last_run_time = scenario_date.get('ricaLastRunTime') 
            # else:
            last_run_date = datetime.date.today().strftime("%Y-%m-%d")
            last_run_time = datetime.datetime.now().strftime("%H:%M:%S")

            update_query =  load_queries.get('UPDATE_QUERY').format(
                ricaLastRunDate=last_run_date,
                ricaLastRunTime=last_run_time,
                ricaNextRunDate=last_run_date,
                ricaNextRunTime=last_run_time,
                ricaRuleId=scenarioRecord['ricaRuleId']
                 )


            # print('update_query',update_query,execute)
            try: 
                if execute:
                    execute(update_query,update=True, commit=True)
                else:
                    self.cursor.execute(update_query)
                    self.cursor.commit()
                # self.cursor.close()
            except Exception as e:
                print('write error', e)
            print('RULE UPDATED')

        except Exception as e:
            print('update _ error',e)

    def update_next_rundate(self,scenarioRecord,execute=None):
        copy_data = {}
        try:
            copy_data['ricaRunMode'] = scenarioRecord['ricaRunMode'] or "INTERVAL"  
            copy_data['ricaLastRunDate'] = datetime.date.today().strftime("%Y-%m-%d")
            copy_data['ricaLastRunTime'] = datetime.datetime.now().strftime("%H:%M:%S")

            scenario_date = GenRunDate({**scenarioRecord,**copy_data}).run()
            print('scenario_date',scenario_date)

            if scenario_date.get('ricaNextRunDate'): 
                next_run_date = scenario_date.get('ricaNextRunDate')
                next_run_time = scenario_date.get('ricaNextRunTime') 

                update_query =  load_queries.get('UPDATE_QUERY_NEXTRUNDATE').format(
                    ricaNextRunDate=next_run_date,
                    ricaNextRunTime=next_run_time,
                    ricaRuleId=scenarioRecord['ricaRuleId']
                     )

            print('update_query nextrun date',update_query)
            try: 
                if execute:
                    execute(update_query,update=True, commit=True)
                else:
                    self.cursor.execute(update_query)
                    self.cursor.commit()
                # self.cursor.close()
            except Exception as e:
                print('write error', e)
            print('RULE NEXT RUN DATE UPDATED')

        except Exception as e:
            print('update next run date_ error',e)




    # def execute(self,query, commit=False, close=False,update=None):
    #     # print("commiting", self.cursor)
    #     result = []
    #     try:
    #         result = self.cursor.execute(query)
    #     except Exception as e:
    #         date_now = str(datetime.date.today()).replace("-","")
    #         time_now = datetime.datetime.now()
    #         current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

    #         log_args = {
    #         "ricaLogId":f'Scenario-{self.scenario}-{date_now}-{current_time}',
    #         'ricaApplication':"Exception",
    #         'ricaScenario':self.scenario,
    #         'ricaQuery':str(query).encode("utf-8"),
    #         'ricaText':f"Exception: {self.scenario} encounted an error: {e}",
    #         'ricaSendTo':'',
    #         'branch':'',
    #         'ricaStatus':"Start",
    #         'ricaRunDate':date_now,
    #         'ricaRunTime':current_time,
           
    #         }

    #         logError("Error").log(log_args,self.scenario)

    #     # self.cursor.close()
    #     if commit:
    #         print("commiting", type(self.cursor))
    #         self.cursor.commit()
    #     if close:
    #         print("closing", type(self.cursor))
    #         self.cursor.close()
    #     return result


    def execute(self, query, commit=False, close=False, update=None, max_retries=5, retry_delay=5,bind_dicts=None):
        result = []
        retry_count = 0
        while retry_count < max_retries:
            try:
                result = self.cursor.execute(query,bind_dicts) if bind_dicts else self.cursor.execute(query) 
                if commit:
                    self.cursor.commit()
                if close:
                    self.cursor.close()
                return result
            except Exception as e:
                date_now = str(datetime.date.today()).replace("-","")
                time_now = datetime.datetime.now()
                current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

                log_args = {
                "ricaLogId":f'Scenario-{self.scenario}-{date_now}-{current_time}',
                'ricaApplication':"Exception",
                'ricaScenario':self.scenario,
                'ricaQuery':str(query).encode("utf-8"),
                'ricaText':f"Exception: {self.scenario} encounted an error: {e}",
                'ricaSendTo':'',
                'branch':'',
                'ricaStatus':"Start",
                'ricaRunDate':date_now,
                'ricaRunTime':current_time,
               
                }

                logError("Error").log(log_args,self.scenario)
                if "deadlock" in str(e).lower() and retry_count < max_retries - 1:
                    print(f"Retrying after {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    # retry_count += 1
                else:
                    break
        return result



    def custom_execute(self,cursor):

        def _cx(query, commit=False, close=False,update=None):
            if update:
                result = cursor.execute(query)
            else:
                result = self.fetchAllWIthColumns(cursor.execute(query))
            if commit:
                print("commiting", type(cursor))
                cursor.commit()
            if close:
                print("closing", type(cursor))
                cursor.close()
            return result
        return _cx





    def run_alerts(self,scenarioId,journalEntriesData=None,cursor=None,scenarioRecord=None):

        df = []
        f = [] 
        groupFieldList=[]
        all_emails = {
                    'to':[],
                    'cc':[],
                    }
        z=[]
        fields = ["RICATRANSID","RICATRANSTYPE","RICALCYAMOUNT","RICAFCYAMOUNT","RICAFCYCODE","RICALCYCODE","RICATRANSCODE","RICANARRATIVE","RICAENTRYTIME","RICAENTRYDATE","RICALOCATION","RICADEVICE","RICACUSTOMERNO","RICAACCOUNTID","RICAACCOUNTNAME"]


        print('scenarioRecord',scenarioId)
        cursor_execute = self.custom_execute(cursor) if cursor else self.execute
        spf = get_spf(cursor_execute, "en",load_queries.get('GET_SPF'))
        still_valid = license_expired(spf,self.env_settings)
        if still_valid:
            expired_notification = get_expired_notification(spf)
            scenarioRecord = scenarioRecord or step_1(cursor_execute, scenarioId)

            if not scenarioRecord:
                raise Exception(f"No rule found for {scenarioId}")
            ricaRunStatus = get_status(cursor_execute,scenarioRecord["ricaRunStatus"]) if scenarioRecord["ricaRunStatus"] else {'ricaModelflag':1}
            
            if scenarioRecord and ricaRunStatus and int(ricaRunStatus["ricaModelflag"]) and scenarioRecord["ricaQueryPanel"]:
                # print(scenarioRecord)
                v_lastrundate = scenarioRecord["ricaLastRunDate"] #'2021-01-06'
                v_lastruntime = scenarioRecord["ricaLastRunTime"]#'06:01:01' 
                v_nextrundate =  scenarioRecord["ricaNextRunDate"] #'2021-06-01' 
                v_nextruntime = scenarioRecord["ricaNextRunTime"]  #'08:11:01' 
                groupFieldList = []

                group_field = find_grouping(scenarioRecord.get("ricaRespondent"))

                branch_rule = r"{\s*branch_code\s*}"
                if not re.search(branch_rule,scenarioRecord.get('ricaQueryPanel')):
                   groupFieldList = [{'branch': ''}]
                   group_field = "branch"
                else:
                    groupFieldList = step_2(cursor_execute, str(create_date(v_nextrundate,'-')),
                                        str(create_time(v_nextruntime,':')), str(create_date(v_lastrundate,'-') ), 
                                        str(create_time(v_lastruntime,':')),
                                        group_field,spf
                                    )

                print(f'{group_field} found since lastrundate: ',len(groupFieldList)) 

                threads = []

                entryRecordLen = 0

                for exactValue in groupFieldList:  
                    emails = {
                    'to':[],
                    'cc':[],
                    }
                    # def thread_run_alert(exactValue,emails,v_nextrundate, v_nextruntime,v_lastrundate,v_lastruntime,group_field,spf):
                    print('Starting Inner Thread: ',exactValue)
                    entryRecordList,exceptions,accountsList = step_3(cursor_execute, scenarioRecord, exactValue, emails,str(create_date(v_nextrundate,'-')),
                                        str(create_time(v_nextruntime,':')), str(create_date(v_lastrundate,'-') ), str(create_time(v_lastruntime,':')),
                                        group_field,spf,model,self.APP_URL )                 

                        
                self.update_next_rundate(scenarioRecord,cursor_execute) 
                if str(STATUS).lower()=='production':
                    self.update_rica_scenarios(scenarioRecord,cursor_execute) 
                return (all_emails,groupFieldList,group_field)
            else:
                raise Exception("Scenario is Deactivated or encounter an error.")



    def gen_str(self,string):
        return str(string) if len(str(string)) > 1 else '0{}'.format(string)


    def get_date(self):
        now = datetime.datetime.now()
        ricaRecordDate = '{}{}{}'.format(
            now.year, self.gen_str(now.month), self.gen_str(now.day))
        ricaRecordTime = '{}:{}:{}'.format(
            self.gen_str(now.hour), self.gen_str(now.minute), self.gen_str(now.second))
        date_time = "{}-{}".format(ricaRecordDate, ricaRecordTime)
        return date_time


    def run_time_reached(self,date_str, time_str):
        try:
            if date_str and time_str:
                current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                try:
                    date_str = str(date_str).split(" ")[0]
                    time_str = str(time_str).split(" ")[1]
                except Exception as e:
                    print('efdf',e)

                print('date_str, time_str',date_str, time_str)

                format_1 = '%Y-%m-%d %H:%M:%S'
                format_2 = '%Y-%m-%d %H:%M:%S.%f'

                try:
                    given_datetime = datetime.datetime.strptime(str(date_str) + " " + str(time_str), format_1)
                except:
                    given_datetime = datetime.datetime.strptime(str(date_str) + " " + str(time_str), format_2)

                
                if str(given_datetime) <= str(current_datetime):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print('runtime reached errs: ',e)
            return True






    def runAlert(self,scenario = ""):

        group_field = ""

        try:
            print('\n\n')
            print("=====================================")
            print(f"   Running Instructions  -  {scenario}    ")
            print("=====================================")

            date_now = str(datetime.date.today()).replace("-","")
            time_now = datetime.datetime.now()
            current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

            log_args = {
            "ricaLogId":f'Scenario-{scenario}-{date_now}-{current_time}',
            'ricaApplication':"Exception",
            'ricaScenario':scenario,
            'ricaQuery':"",
            'ricaText':f"Exception: {scenario} run started on {date_now}",
            'ricaSendTo':'',
            'branch':'',
            'ricaStatus':"Start",
            'ricaRunDate':date_now,
            'ricaRunTime':current_time,
           
            }

            logError("Start").log(log_args,scenario)
            
            cursor_execute =  self.execute
            scenarioRecord = step_1(cursor_execute, scenario) 

            v_lastrundate = scenarioRecord["ricaLastRunDate"] #'2021-01-06'
            v_lastruntime = scenarioRecord["ricaLastRunTime"]#'06:01:01' 
            v_nextrundate =  scenarioRecord["ricaNextRunDate"] #'2021-06-01' 
            v_nextruntime = scenarioRecord["ricaNextRunTime"]  #'08:11:01' 
            default_variables  ={
            'v_lastruntime':str(create_time(v_lastruntime,':')),
            'v_lastrundate':str(create_date(v_lastrundate,'-') ),
            'v_nextrundate':str(create_date(v_nextrundate,'-')),
            'v_nextruntime':str(create_time(v_nextruntime,':')),     
            }

            if self.run_time_reached(scenarioRecord['ricaNextRunDate'], scenarioRecord['ricaNextRunTime']):
                emails,groupFieldList,group_field = self.run_alerts(scenario,scenarioRecord=scenarioRecord)

                
                log_args = {
                "ricaLogId":f'Scenario-{scenario}-{date_now}-{current_time}',
                'ricaApplication':"Exception",
                'ricaScenario':scenario,
                'ricaQuery': replaceParams(scenarioRecord.get("ricaQueryPanel"),default_variables) ,
                'ricaText':f"Exception: {scenario} run successfully on {date_now}",
                'ricaSendTo':', '.join(emails),
                group_field: json.dumps(groupFieldList),
                'ricaStatus':"Success",
                'ricaRunDate':date_now,
                'ricaRunTime':current_time,           
                }
                # print(log_args)
                logError("Success").log(log_args,scenario) 
            else:
                print(f'CURRENT DATETIME: {datetime.datetime.now()} , NEXT RUN DATE not reached until: ', str(create_date(v_nextrundate,'-')), str(create_time(v_nextruntime,':')))
        except Exception as e:
            print('RunTime Error found: ',e)
            date_now = str(datetime.date.today()).replace("-","")
            time_now = datetime.datetime.now()
            current_time = str(time_now.strftime("%H:%M:%S")).replace("-","")

            log_args = {
            "ricaLogId":f'Scenario-{scenario}-{date_now}-{current_time}',
            'ricaApplication':"Exception",
            'ricaQuery':replaceParams(scenarioRecord.get("ricaQueryPanel"),default_variables),
            'ricaScenario':scenario,
            'ricaText':f"Exception: {scenario} Error: {e}",
             'ricaSendTo':', '.join([]),
            group_field:', '.join([]),
            'ricaStatus':"Error",
            'ricaRunDate':date_now,
            'ricaRunTime':current_time,
           
                }
            logError("Error").log(log_args,scenario) 




if __name__=='__main__':
    parser = argparse.ArgumentParser(description ='Run Exception Services')  
    parser.add_argument('-r', dest ='rule',
                        action ='store', help ='run rule (seconds)',default=None)  

    args = parser.parse_args() 
    rule =  args.rule  #if args.rule else list(reversed(__file__.split("\\")))[1] 
    # print(get_env_settings())
    if rule:
         AlertService(rule).runAlert(scenario= rule)
    else:
        raise Exception("No rule provided")




