

 
UPDATE_QUERY = """ 
            UPDATE RICA_ETL_SERVICES
             SET LAST_RUN_DATE = CONVERT(date, '{LAST_RUN_DATE}', 23),  
                LAST_RUN_TIME = CONVERT(time, '{LAST_RUN_TIME}', 114)
                    WHERE NAME = '{NAME}'
         
     """