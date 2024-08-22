
USERS1= """
       SELECT  ricaUserId,
       ricaUserEmail,
        ricaUserTitle,
        ricaFirstName,
        ricaMiddleName,
        ricaLastName,
        ricaUserPwd,
        ricaUserRole,
        ricaStaffNo,
        ricaUserStatus,
        ricaCountry,
        ricaCompany,
        ricaMainLanguage,
        ricaStaffGrade,
     date_format(ricaDateJoined,'%Y-%m-%d') AS ricaDateJoined,
                   date_format(ricaRecordDate,'%Y-%m-%d') AS ricaRecordDate,
       ricaOperation,
        ricaOperator,
        ricaLanguage,
        ricaWorkstation,
        ricaRecordTime,
        ricaUserLocation,
        ricaRecordCounter
         from rica_user
     """



GET_SPF=""" select ricaClientName,ricaStmpMailServer,ricaStmpMailPort,ricaStmpMailUser,ricaStmpMailPassword,
     ricaDefaultOwner,ricaDefaultRespondent,ricaDefaultInvestigator,ricaLicenseCode,ricaLicenseNotifyDur,
     date_format(ricaExpiryDate,'%Y-%m-%d') AS ricaExpiryDate 
     from rica_spf 
     where ricaSpfId='{lang}-SYSTEM' """



GET_ACCT_TRANSACTIONS = """
SELECT DISTINCT   
    RICATRANSID AS Transaction_ID,
    ricatranstype AS Transaction_Type,
    RICABRANCHCODE AS Transaction_Branch,  
    CAST(RICANARRATIVE AS CHAR(400)) AS Transaction_Narrative, 
    RICAENTRYDATE AS Transaction_Date,
    RICASPECIALTIME AS Transaction_Time,
    RICAINPUTTER AS Inputter, 
    RICATRANSMODE AS Transaction_Mode,  
    RICALCYCODE AS Transaction_Currency,
    RICALCYAMOUNT AS Transaction_Amount, 
    RICATRANSCODE AS Transaction_Indicator, 
    RICAACCOUNTID AS Transaction_Account,
    RICALOCATION AS Transaction_Location,
    RICADEVICE AS Transaction_Device
FROM RICA_JOURNALENTRIES
WHERE CONCAT(RICASPECIALDATE, RICASPECIALTIME) >= '{v_lastrundate}{v_lastruntime}'  
    AND RICAACCOUNTID = '{account}' 
ORDER BY Transaction_Date DESC, Transaction_Time DESC
LIMIT 10;

"""