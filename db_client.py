
from AnomalyPromptGRP.func import get_env_settings
from AnomalyPromptGRP.ricaED import E 
import pandas as pd
from sqlalchemy import create_engine,text 

from urllib.parse import quote
DB_SETTINGS = get_env_settings()

enc = E("@adr0it")

# print('get_env_settings()', get_env_settings())


 

class create_connection():

    def __init__(self, MAP={}, close=False, commit=False,db_type=""):
        self.map = MAP
        self.db_type = db_type
        self.connection = self.connect()

    def connect(self):
        print('DATABASE_TYPE', str(DB_SETTINGS.get('DATABASE_TYPE')).lower())

        if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql' or str(self.db_type).lower()=='mysql':
            import pymysql
            import pymysql.cursors

            HOST = DB_SETTINGS.get('DATABASE_HOST')
            USER = DB_SETTINGS['DATABASE_USER']
            PASSWORD = enc.D(DB_SETTINGS['DATABASE_PASSWORD'])
            PASSWORD = quote(PASSWORD, safe='')
            NAME = DB_SETTINGS['DATABASE_NAME']

            con = pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                db=NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
            )
            return (con, con.cursor())

        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle' or str(self.db_type).lower()=='oracle':
            try:
                import cx_Oracle as Database
                if DB_SETTINGS.get('ORACLE_CLIENT_DIR', r"D:\oracle\instantclient_19_11"):
                    # print('setting custom cx_Oracle lib_dir',DB_SETTINGS.get('ORACLE_CLIENT_DIR', r"D:\oracle\instantclient_19_11"))
                    try:
                        Database.init_oracle_client(lib_dir=DB_SETTINGS.get('ORACLE_CLIENT_DIR', r"D:\oracle\instantclient_19_11"))
                    except Exception as e:
                        print('oracle_DBERR',e)
                    con = Database.connect(
                        DB_SETTINGS['DATABASE_USER'],  enc.D(DB_SETTINGS['DATABASE_PASSWORD']) , DB_SETTINGS['DATABASE_NAME'], encoding="UTF-8", nencoding="UTF-8", threaded=True)
                    return ( con,con.cursor())
                    
            except ImportError as e:
                raise Exception(
                    "Error loading cx_Oracle module: %s" % e)

        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mssql' or str(self.db_type).lower()=='mssql': 
            import pyodbc
            HOST = DB_SETTINGS.get('DATABASE_HOST')
            USER = DB_SETTINGS['DATABASE_USER']
            PASSWORD = enc.D(DB_SETTINGS['DATABASE_PASSWORD'])
            # PASSWORD = quote(PASSWORD, safe='')
            NAME = DB_SETTINGS['DATABASE_NAME']
            DRIVER = DB_SETTINGS.get('DATABASE_DRIVER') or 'ODBC Driver 17 for SQL Server'
            db_url = f"mssql+pyodbc://{USER}:{PASSWORD}@{HOST}/{NAME}?driver={DRIVER}&autocommit=true"
            # print('db_url',db_url)
            engine = create_engine(db_url) 


            return (engine, False) 
        else:
            pass
            # from django.db import connection
            # cursor = connection.cursor()
            # return cursor

    def execute(self, query,bind_dicts=None):
        if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql' or str(self.db_type).lower()=='mysql':
            result = []
            engine, cursor = self.connection
            try:
                cursor.execute(query,bind_dicts) if bind_dicts else cursor.execute(query)
                result = cursor.fetchall()
            finally:
                pass
            return result

        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mssql' or str(self.db_type).lower()=='mssql':
            result = []
            engine, cursor = self.connection
            # print('query',text(query))
            try:
                if ('update' in query.lower() and 'set' in query.lower()) or 'insert' in query.lower() :
                    with engine.connect() as connection:
                        connection.execute(text(query),bind_dicts) if bind_dicts else connection.execute(text(query))
                    engine.dispose()
                else:
                    df = pd.read_sql(query,engine)
                    df.rename(columns=self.map, inplace=True)
                    result = df.to_dict('records')
            finally:
                pass
            return result

        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle' or str(self.db_type).lower()=='oracle':
            con, cursor = self.connection
            result = []
            import cx_Oracle as Database
            try:
                result = self.fetchAllWIthColumns(cursor.execute(query,bind_dicts)) if bind_dicts else self.fetchAllWIthColumns(cursor.execute(query))

            finally:
                pass
            return result

        else:
            cursor = self.connection()
            result = self.fetchAllWIthColumns(cursor.execute(query))
            return result

    def close(self):
        if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql' or str(self.db_type).lower()=='mysql':
            con, cursor = self.connection
            con.close()
        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mssql' or str(self.db_type).lower()=='mssql':
            con, cursor = self.connection
            con.close()
        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle' or str(self.db_type).lower()=='oracle':
            con, cursor = self.connection
            cursor.close()
            con.close()
        else:
            pass

    def commit(self,query=""):
        if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql' or str(self.db_type).lower()=='mysql':
            con, cursor = self.connection
            con.commit()
        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mssql' or str(self.db_type).lower()=='mssql':
            con, cursor = self.connection
            # con.execute(text('COMMIT;'))
            # con.commit()
        elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle' or str(self.db_type).lower()=='oracle':
            con, cursor = self.connection
            con.commit()
        print('saved')

    def fetchAllWIthColumns(self, cursor):
        if cursor:
            # print("Return all rows from a cursor as a dict",cursor.description)
            columns = [ self.map.get(col[0], col[0])   
                       for col in cursor.description if cursor.description]
            return [
                dict(zip(columns, row))
                for row in self.get_cursor_data(cursor)
            ] 

    def get_cursor_data(self,cursor):
        cursor_data = []    
        if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle' or str(self.db_type).lower()=='oracle' :
            import cx_Oracle
            for row in cursor: 
                results = []    
                for my_lob in row:
                    if isinstance(my_lob, cx_Oracle.LOB):
                        data = my_lob.read() 
                        results.append(data)
                    else:
                        results.append(my_lob) 
                cursor_data.append(results)
        else:
            return cursor.fetchall()
            
        return cursor_data


# class create_connection():
#   def __init__(self,MAP={},close_con=True):
#       self.map = MAP
#       self.connection = self.connect()
#       self.close_con = close_con

#   def connect(self):
#       print('DATABASE_TYPE',str(DB_SETTINGS.get('DATABASE_TYPE')).lower())


#       if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql':
#           import pymysql
#           import pymysql.cursors

#           HOST = DB_SETTINGS.get('DATABASE_HOST')
#           USER = DB_SETTINGS['DATABASE_USER']
#           PASSWORD = enc.D(DB_SETTINGS['DATABASE_PASSWORD'])
#           NAME = DB_SETTINGS['DATABASE_NAME']

#           con=pymysql.connect(
#               host=HOST,
#               user=USER,
#               password = PASSWORD,
#               db=NAME,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor
#           )
#           return (con,con.cursor())

#       elif str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle':
#           import cx_Oracle
#           con = cx_Oracle.connect(DB_SETTINGS['DATABASE_USER'] , enc.D(DB_SETTINGS['DATABASE_PASSWORD']), DB_SETTINGS['DATABASE_NAME'])
#           return (con,con.cursor())

#       else:
#           from django.db import connection
#           cursor = connection.cursor()
#           return  cursor

#   def execute(self,query):
#       if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql':
#           result=[]
#           con, cursor = self.connection
#           try:
#               # cursor = cursor.cursor()
#               with cursor as cur:
#                   cur.execute(query)
#                   result = cur.fetchall()
#           finally:
#               pass
#               # if self.close_con:
#               #   cursor.close()
#               #   con.close()
#           return result

#       elif  str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle':
#           con, cursor = self.connection
#           result = []
#           try:
#               result = self.fetchAllWIthColumns(cursor.execute(query))
#           finally:
#               pass
#               # if self.close_con:
#               #   cursor.close()
#               #   con.close()
#           return result

#       else:
#           cursor = self.connection
#           result = self.fetchAllWIthColumns(cursor.execute(query))
#           return result


#   def close(self):
#       if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql' or str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle':
#           con, cursor = self.connection
#           cursor.close()
#           con.close()
#       else:
#           pass

#   def commit(self):
#       if str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'oracle' or str(DB_SETTINGS.get('DATABASE_TYPE')).lower() == 'mysql':
#           con, cursor = self.connection
#           con.commit()

#   def fetchAllWIthColumns(self,cursor):
#       "Return all rows from a cursor as a dict"
#       columns = [self.map.get(col[0],col[0]) for col in cursor.description]
#       return [
#           dict(zip(columns, row))
#           for row in cursor.fetchall()
#       ]
