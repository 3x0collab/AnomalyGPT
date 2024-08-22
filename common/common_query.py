GET_SPF=""" select ricaStmpMailServer,ricaStmpMailPort,ricaStmpMailUser,ricaStmpMailPassword,ricaStmpMailAddress,ricaAppsId,ricaReleaseNo
     from rica_spf 
     where ricaSpfId='{lang}-SYSTEM' """




get_customer_account=""" 

    SELECT RICAACCOUNTID 
    FROM RICA_JOURNALENTRIES
       where CONCAT(RICASPECIALDATE,RICASPECIALTIME) >= '{last_run_date}{last_run_time}'  
     

 """


get_customer_data_query=""" 
  SELECT DISTINCT C1.RICATRANSID,
                C1.RICAENTRYSERIALNO,
                C1.RICATRANSREFID,
                C1.RICABRANCHCODE,
                CAST(C1.RICANARRATIVE AS VARCHAR(400)) AS RICANARRATIVE,
                C1.RICAENTRYDATE,
                C1.RICAINPUTTER,
                C1.RICAAUTHORISER,
                C1.RICAVALUEDATE,
                C1.RICATRANSMODE,
                C1.RICALCYCODE,
                C1.RICALCYAMOUNT,
                C1.RICALCYAMOUNT as CR_AMOUNT,
                C2.RICALCYAMOUNT as DR_AMOUNT,
                C1.RICAFCYCODE,
                C1.RICAFCYAMOUNT,
                C1.RICARATE,
                C1.RICATRANSTYPE,
                C1.RICATRANSCODE as CREDIT_INDICATOR,
                C1.RICAACCOUNTID as CREDIT_ACCOUNT,
                C2.RICATRANSCODE AS DEBIT_INDICATOR,
                C2.RICAACCOUNTID as DEBIT_ACCOUNT
FROM (
    SELECT *
    FROM RICA_JOURNALENTRIES
       where CONCAT(RICASPECIALDATE,RICASPECIALTIME) >= '{last_run_date}{last_run_time}'  
      AND ricatranscode = 'C' 
      and ricaaccountid='{account_id}'
) C1
LEFT JOIN (
    SELECT *
    FROM RICA_JOURNALENTRIES
         where CONCAT(RICASPECIALDATE,RICASPECIALTIME) >= '{last_run_date}{last_run_time}'  
      AND ricatranscode = 'D' 
        and ricaaccountid='{account_id}'
) C2
ON C1.RICALCYAMOUNT = C2.RICALCYAMOUNT
   AND C1.RICAVALUEDATE = C2.RICAVALUEDATE
   AND C1.RICATRANSID = C2.RICATRANSID



 """

get_all_customer_data_query=""" 

select DISTINCT ricaaccountid   from RICA_JOURNALENTRIES 

 """



GET_PARAMETER=""" select ricaName, ricaValue from rica_parameter 
where LOWER(ricaName) = 'anomalygpt receiver'  """