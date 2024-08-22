import os
import sys
import shutil
import csv
import datetime as dt
from datetime import datetime
from SNow.config import delimiter,quotechar,SQLITE_DIRS,source_folder as sf,target_folder as tf, errors_folder as ef, mappers as mp,time_formatter,date_formatter,DTTYPES,language
from SNow.config import DATABASE_TYPE,DATABASE_TYPE,DATABASE_PORT,DATABASE_NAME,USERNAME,PASSWORD,ORACLE_CLIENT_DIR,ODBC_DRIVER,TARGET_TABLE,LAST_RUN_DATE,LAST_RUN_TIME,SANCTION_API_KEY,SANCTION_API_URL,ADMIN_EMAILS,CHECK_SEARCHED_RECORDS_WHEN, CHECK_RECORDS_WHEN,CHECK_RECORDS_WEEKLY,RUN_MODE,CLIENT_API_URL,CLIENT_API_PARAMS,SEND_EMAIL,AI_SCAN
from SNow.ricaED import E 
from SNow.utils import logError,get_env_settings,get_sqlite_con_dir,send_email_error
from SNow.common import load_queries

import cx_Oracle
import sqlite3
from sqlalchemy import create_engine,inspect,MetaData,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError,DatabaseError
import pandas as pd
import threading
from pytz import utc
import time 
import re
import logging 
import json
import requests
from concurrent.futures import ThreadPoolExecutor


enc = E("@adr0it")
skipped_table_set = {}

def configure_logging():
	log_file = os.path.join(os.path.dirname(__file__), 'app.log')
	# logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



db_config = {}
db_config['DATABASE_TYPE'] = DATABASE_TYPE
db_config['DATABASE_TYPE'] = DATABASE_TYPE
db_config['DATABASE_PORT'] = DATABASE_PORT
db_config['DATABASE_NAME'] = DATABASE_NAME
db_config['USERNAME'] = USERNAME
db_config['PASSWORD'] = PASSWORD
db_config['ORACLE_CLIENT_DIR'] = ORACLE_CLIENT_DIR
db_config['ODBC_DRIVER'] = ODBC_DRIVER
db_config['TARGET_TABLE'] = TARGET_TABLE
db_config['LAST_RUN_DATE'] = LAST_RUN_DATE
db_config['LAST_RUN_TIME'] = LAST_RUN_TIME
db_config['ADMIN_EMAILS'] = ADMIN_EMAILS


 

class DatabaseConnector():
	"""docstring for DatasetConnector""" 

	def __init__(self,file_path,dir_name,service={}):
		self.dir_name = dir_name
		self.file_path = file_path
		self.db_type = service.get('DATABASE_TYPE')
		self.host = service.get('DATABASE_TYPE')
		self.port = service.get('DATABASE_PORT')
		self.db_name = service.get('DATABASE_NAME')
		self.username = service.get('USERNAME')
		self.password = service.get('PASSWORD')
		self.oracle_client_dir = service.get('ORACLE_CLIENT_DIR')
		self.odbc_driver = service.get('ODBC_DRIVER') 
		self.service = service
		self.state = True
		if str(RUN_MODE).lower() =='api':
			self.connect_to_api()
		else:
			self.connect_to_database()


	def connect_to_api(self):
		pass

	def connect_to_database(self):
		credentials = get_env_settings() 

		try:
			# Extract form inputs
			db_type = self.db_type or str(credentials['DATABASE_TYPE']).lower() 
			host = self.host or credentials.get('DATABASE_HOST') 
			port = self.port or credentials.get('DATABASE_PORT') 
			db_name = self.db_name or credentials['DATABASE_NAME'] 
			username = self.username or credentials['DATABASE_USER']
			password = enc.D(  self.password or credentials['DATABASE_PASSWORD']) 

			# Database connection URL
			db_type = db_type.lower()
			if db_type == 'postgresql':
				db_url = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'
			elif db_type == 'mysql':
				db_url = f'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'
			elif db_type == 'sqlite':
				db_url = f'sqlite:///{db_name}'
			elif db_type == 'oracle':
				try:
					cx_Oracle.init_oracle_client(r"{}".format(self.oracle_client_dir or credentials.get('ORACLE_CLIENT_DIR', r"D:\oracle\instantclient_19_11")))
				except:
					pass
				spldb = db_name.split(':')
				spldb2 = spldb[1].split('/')
				db_url = f'oracle://{username}:{password}@{spldb[0]}:{spldb2[0]}/{spldb2[1]}'
			elif db_type == 'mssql':
				driver = self.odbc_driver or 'ODBC Driver 17 for SQL Server'
				db_url = f'mssql+pyodbc://{username}:{password}@{host}:{port}/{db_name}?driver={driver}' 
			elif db_type == 'sqlite':
				db_url = f'sqlite:///{db_name}' 
			elif db_type == 'MariaDB':
				db_url = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'
			else:
				raise ValueError('Invalid database type')
			# Connect to the database 
			print('Loading DB configs.. ' )

			date_now = str(dt.date.today()).replace("-","")
			time_now = dt.datetime.now()
			current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

			log_args = {
			"ricaLogId":f'Table-{self.dir_name}-{date_now}-{current_time}',
			'ricaApplication':"ETL Service State",
			'Folder':self.dir_name,
			'ricaText':f"ETL: Create Engine, connecting to db..",
			'ricaStatus':"Ongoing",
			'ricaRunDate':date_now,
			'ricaRunTime':current_time,					   
			}
			logError("State").log(log_args,'Main')

			self.engine = create_engine(db_url)
			self.engine.connect()
			Session = sessionmaker(bind=self.engine)
			self.session = Session()
			log_args['ricaText'] = f"ETL: DB Connected.."
			logError("State").log(log_args,'Main')
			# print('Connected',db_url)
			self.state =  True
		except DatabaseError  as e:
			print('eeeeeeeee',e)
			date_now = str(dt.date.today()).replace("-","")
			time_now = dt.datetime.now()
			current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

			log_args = {
			"ricaLogId":f'Table-DB-{date_now}-{current_time}',
			'ricaApplication':f"ETL Service Name:  {self.service['NAME']}",
			'Folder':db_url,
			'ricaText':f"Error: {e}",
			'ricaStatus':"Error",
			'ricaRunDate':date_now,
			'ricaRunTime':current_time,					   
			}
			logError("Error").log(log_args,'Main')
			if self.service.get('ADMIN_EMAILS'):
				db_connector = DatabaseConnector('',"")
				spf = db_connector.get_spf()
				send_email_error(self.service, '\n'.join([f"{key}: {value}" for key, value in log_args.items()]),spf)
			else:
				send_email_error(self.service, '\n'.join([f"{key}: {value}" for key, value in log_args.items()]),credentials)
			self.state =  False

			# sys.exit(0)


	def process_transaction_data(self,full=False):
		date_now = str(dt.date.today()).replace("-","")
		time_now = dt.datetime.now()
		current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

		log_args = {
		"ricaLogId":f'Table-{date_now}-{current_time}',
		'ricaApplication':"ETL Service State",
		'Folder':self.service.get('TARGET_TABLE'),
		'ricaText':f"ETL: Loading DB configs..",
		'ricaStatus':"Ongoing",
		'ricaRunDate':date_now,
		'ricaRunTime':current_time,					   
		}
		logError("State").log(log_args,'Main')


		data = None
		last_run_date, last_run_time = self.get_last_run_info()

		get_config_query = text(load_queries.get('get_customer_data_query').format(
					last_run_date=last_run_date,last_run_time=last_run_time ) )
		print(get_config_query)
		
		result = self.session.execute(get_config_query) 
		self.save_last_run_info()
		column_names = [desc[0] for desc in result.cursor.description]  # Retrieve column names from the ResultSet
		total_data = []
		while True:
			rows = result.fetchmany(50)  # Retrieve 50 rows at a time
			if not rows:
				break
			data = [dict(zip(column_names, row)) for row in rows]
			connect_to_rica_api(data) #connect to API
			# time.sleep(5) 

		return data



	def get_account_data(self):
		data = None
		last_run_date, last_run_time = self.get_last_run_info()

		get_config_query = text(load_queries.get('get_customer_account').format(
					last_run_date=last_run_date,last_run_time=last_run_time ) )
		print(get_config_query)
		
		result = self.session.execute(get_config_query) 
		self.save_last_run_info()
		column_names = [desc[0] for desc in result.cursor.description]  # Retrieve column names from the ResultSet
		total_data = []
		while True:
			rows = result.fetchmany(50)  # Retrieve 50 rows at a time
			if not rows:
				break
			data = [dict(zip(column_names, row)) for row in rows]
			connect_to_rica_api(data) #connect to API
			# time.sleep(5) 

		return data


	
	
	def save_last_run_info(self,filename="anomaly_last_run_info.txt"):
		last_run_date = dt.datetime.now().strftime('%Y%m%d')
		last_run_time = dt.datetime.now().strftime('%H%M%S')
		with open(filename, 'w') as file:
			file.write(f"LAST_RUN_DATE={last_run_date}\n")
			file.write(f"LAST_RUN_TIME={last_run_time}")


	def get_last_run_info(self,filename="anomaly_last_run_info.txt"):
		last_run_date = dt.datetime.now().strftime('%Y%m%d')
		last_run_time = dt.datetime.now().strftime('%H%M%S')
		try:
			with open(filename, 'r') as file:
				lines = file.readlines()
			last_run_date = last_run_date
			last_run_time = last_run_time
			for line in lines:
				if line.startswith("LAST_RUN_DATE"):
					last_run_date = line.split('=')[1].strip()
				elif line.startswith("LAST_RUN_TIME"):
					last_run_time = line.split('=')[1].strip()
			return last_run_date, last_run_time
		except FileNotFoundError:
			print(f"File '{filename}' not found. Returning ",last_run_date, last_run_time )
			return last_run_date, last_run_time  



def connect_to_rica_api(cus_info):
	try:
		date_now = str(dt.date.today()).replace("-","")
		time_now = dt.datetime.now()
		current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")
		log_args = {
		"ricaLogId":f'RICA-API',
		'ricaApplication':"API Service State",
		'Folder':"Main",
		'ricaText':f"Connecting to API ..",
		'ricaStatus':"Ongoing",
		'ricaRunDate':date_now,
		'ricaRunTime':current_time,					   
		}
		logError("State").log(log_args,'Main')	  

		request_body  = {
		 "queries": list(map( lambda x: {'name': x.get('RICAFULLNAME'),'nationality':x.get('COUNTRY') },cus_info )),
			"merge_results":False,
			"send_email":SEND_EMAIL,
			"ai_scan":AI_SCAN,
			"scan_reason":'Fidelity',
			}

		default_headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Authorization': f"Bearer <{SANCTION_API_KEY}>",

		}

		# Make the GET request
		# print(request_body)
		try:
			response = requests.post(SANCTION_API_URL, json=request_body, headers=default_headers)
			response.raise_for_status()
			results = response.json().get('results')
			# print(results)
			if results:
				for name_data in cus_info:
					if not len(results.get(name_data.get('RICAFULLNAME'))):
						save_data_to_json(name_data)
					else:
						save_data_to_json({
							 'RICAFULLNAME': name_data.get('RICAFULLNAME'),
							 'RICADATECREATED': name_data.get('RICADATECREATED'),
							'results':results.get(name_data.get('RICAFULLNAME')),
							}, 'RECORDSFOUNDINLIST')


		except requests.exceptions.RequestException as e:
			print(f"Error connecting to Postman API: {e}")

	except Exception as e:
		print('Exception catch: ',e)
		date_now = str(dt.date.today()).replace("-","")
		time_now = dt.datetime.now()
		current_time = str(time_now.strftime("%H:%M:%S")).replace(":","")

		log_args = {
				"ricaLogId":f'Error-{date_now}-{current_time}',
				'ricaApplication':"RICA-API",
				'ricaFileName':"Unknown",
				'Folder':'RICA-API',
				'ricaTable':'RICA-API',
				'ricaText':f"Error: {str(e)}",
				'ricaStatus':"Failed",
				'ricaRunDate':date_now,
				'ricaRunTime':current_time,
				}

		logError("Error").log(log_args,'RICA-API') 

 






def check_records():
	running_flag = True
	db_connector = DatabaseConnector('',"")
	try:
		while running_flag:
			services = db_connector.get_account_data()
			print("Getting and checking transaction records records")
			services = db_connector.process_transaction_data()
			print("Check records, sleeping for ", CHECK_RECORDS_WHEN,'seconds')
			time.sleep(CHECK_RECORDS_WHEN)  # Adjust the interval as needed
	except KeyboardInterrupt:
		running_flag = False  # Gracefully stop the loop if Ctrl+C is pressed




def main():
	with ThreadPoolExecutor(max_workers=3) as executor:
		future_one = executor.submit(check_records)

		future_one.result()




if __name__ == '__main__':
    main()


def test():
	print("Testing")
	# main()

