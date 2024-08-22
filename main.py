


from AnomalyPromptGRP.db_client import create_connection
from AnomalyPromptGRP.func import get_sqlite_con_dir
MAP = {
	'RICARULEID':'ricaRuleId',
	'RICARULE':'ricaRule',
	'ID':'ricaRuleId'
}
cursor = None

while True:
	try:
		print("CONNECTING TO DATABASE...")
		cursor = create_connection(MAP)
		print("CONNECTED...")	
		break
	except Exception as e:
		print("CONNECTION FAILED: ",e)



from AnomalyPromptGRP.config import SCHEDULE_TIME,RULE_CHECK_TIME,THREAD_POOL, PROCESS_POOL,MAX_INSTANCES,RULE_ID
from AnomalyPromptGRP.run import AlertService
# from AnomalyPromptGRP.scheduler import BotScheduler

from pytz import utc
from datetime import datetime
import os
import sqlite3
from concurrent.futures import ThreadPoolExecutor

sqlite_con_dir = get_sqlite_con_dir() 



import time
import threading
import random
# import asyncio
# cwd = os.getcwd() 

scheduled_jobs_map = set()


def retrieve_jobs_to_schedule(rule_id=""):
	# print("rules id",rule_id)
	if rule_id =='*':
		loc_rules = """select distinct ricaRuleId,ricaRule from rica_prompt_builders
			where ricaRunStatus LIKE '%-208'"""
	else:
		loc_rules = f"""select distinct ricaRuleId,ricaRule from rica_prompt_builders
			where ricaRuleId = '{rule_id}' """
	
	rules = cursor.execute(loc_rules)
	print("rules",rules)
	return list(rules) #[{'ricaRuleId':'test1','ricaRule':'test1 ricaRule'}]  

def execute_job(job):
	print("executing job with ricaRuleId: " + str(job['ricaRuleId']))
	try:
		while True:
			Als = AlertService(str(job['ricaRuleId']))
			Als.runAlert(str(job['ricaRuleId']))
			time.sleep(10)
	except Exception as e:
		print('Execute error: ',e)

def main():
    with ThreadPoolExecutor(max_workers=200) as executor:  # Adjust the max_workers as needed
        while True:
            try:
                jobs = retrieve_jobs_to_schedule("*")
                for job in jobs:
                    job_id = str(job['ricaRuleId'])
                    print("Setting up Prompt: ", job_id)
                    if job_id not in scheduled_jobs_map:
                        scheduled_jobs_map.add(job_id)
                        executor.submit(execute_job, job)
            except Exception as e:
                # Handle exceptions from retrieving jobs
                print('schedule_jobs error: ', e)

            time.sleep(RULE_CHECK_TIME)


# def test_rule(rule):
# 	AlertService(rule).runAlert(rule)

 
if __name__ == '__main__':
	main()
	# test_rule('test1')
