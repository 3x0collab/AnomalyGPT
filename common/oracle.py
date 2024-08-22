# get_customer_data_query=""" 

# select  'olusegun agagu Kokumo' as RICAFULLNAME,RICAREGISTERADDRESS_COUNTRY AS COUNTRY,to_char(RICADATECREATED,'YYYYMMDD') AS RICADATECREATED  from rica_customer 
# where CONCAT(to_char(RICADATECREATED,'YYYYMMDD'),to_char(RICATIMECREATED,'HHMISS') ) >= '{last_run_date}{last_run_time}'   
# AND ROWNUM < 2

#  """



 
UPDATE_QUERY = """ 
            UPDATE RICA_ETL_SERVICES
                     SET LAST_RUN_DATE = TO_DATE('{LAST_RUN_DATE}','yyyy-mm-dd'),  
                     LAST_RUN_TIME = TO_TIMESTAMP('{LAST_RUN_TIME}','HH24:MI:SS')
                    WHERE NAME = '{NAME}'
         
     """