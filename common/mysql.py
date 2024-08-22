

 
UPDATE_QUERY = """ 
            UPDATE RICA_ETL_SERVICES
                     SET LAST_RUN_DATE = CAST('{LAST_RUN_DATE}' AS DATE),
                     LAST_RUN_TIME = CAST('{LAST_RUN_TIME}' AS TIME)
                    WHERE NAME = '{NAME}'
         
     """
 