delimiter='|'
quotechar='"'
SQLITE_DIRS=[r"C:\inetpub\wwwroot\iconcept4pro\backend",r"C:\rica\backend",r"E:\rica\backend",r'C:\inetpub\wwwroot\rica\backend',r'C:\inetpub\wwwroot\radarpro\backend'] #Optional: defaulted to base_dir where backend is located
source_folder = r'E:\rica_keystone_version\Z'
target_folder = r'E:\rica_keystone_version\Z_archived'
errors_folder = r'E:\rica_keystone_version\Z_errors'

mappers = "RICA_ACCOUNT_TEST->account;rica_journalentries->journal;RICA_T24_USER->user;"
date_formatter='%Y-%m-%d'
time_formatter='%H:%M:%S'
DTTYPES=['DATE','TIMESTAMP','NUMBER' ]
# Full Path in which the Logs for this exception will be located eg. C:\Users\Adroit\Desktop
FULL_LOG_PATH=r"C:\\" # defaulted to LOG_PATH 
language='en'

# [ DATABASE PARAMETERS ]
DATABASE_TYPE = 'Oracle' #MSSQL,MYSQL,ORACLE
DATABASE_PORT = ''
DATABASE_NAME = '127.0.0.1:1521/orcl'
USERNAME = 'RICA1'
PASSWORD = '@hky0pAYPJH1' #Eed password
ORACLE_CLIENT_DIR = r"D:\oracle\instantclient_19_11"
ODBC_DRIVER = 'ODBC Driver 17 for SQL Server' 
TARGET_TABLE='rica_customer'
LAST_RUN_DATE='' #%Y-%m-%d
LAST_RUN_TIME='' #%H:%M:%S

RUN_MODE = 'DATABASE' #DATABASE, API


# [ API PARAMETERS ]
CLIENT_API_URL='http://127.0.0.1:8000/customer/search/'
CLIENT_API_PARAMS = {
	
}

SANCTION_API_URL = "http://127.0.0.1:8000/api/search/multiple/"
SANCTION_API_KEY= "5a20-c829-0823-e9b3-vA87"
# API_URL = "https://radarproforfidandunion.pythonanywhere.com/api/search/multiple/"
# API_KEY= "f620-c824-0402-e9b3-vA87"
ADMIN_EMAILS= "oluwamotunde@gmail.com"

CHECK_RECORDS_WHEN = 30
CHECK_SEARCHED_RECORDS_WHEN =  24 * 60 * 60
CHECK_RECORDS_WEEKLY = 7 * 24 * 60 * 60

SEND_EMAIL =  True
AI_SCAN = True

