# Exception Configurations
# Exception ID to run
RULE_ID='*'
# Seconds in which the exception we'll be reschedule
SCHEDULE_TIME=120 #seconds
# Seconds in which new rules will be check
RULE_CHECK_TIME=60*3 # seconds
# Short Location in which the Logs for this exception will be located eg. Desktop, Documents etc
LOG_PATH='Desktop' #Optional: defaulted to Desktop
# Full Path in which the Logs for this exception will be located eg. C:\Users\Adroit\Desktop
FULL_LOG_PATH=r"C:\\" #Optional : defaulted to LOG_PATH 
# The  Directory in which Sqlite File (Optional) is located eg. E:\rica\backend
SQLITE_DIRS=[r'C:\inetpub\wwwroot\rica\backend',r"C:\inetpub\wwwroot\iconcept4pro\backend",r"C:\rica\backend",r"E:\rica\backend",r'C:\inetpub\wwwroot\radarpro\backend',r'E:\radarpro\ic4probackend'] #Optional: defaulted to base_dir where backend is located
# Development Status
STATUS=r"production" # production/development (This will not update last_run_date if in development)
# thread pool executor 
THREAD_POOL=51 #  creates a thread pool executor with a maximum of 51 threads
# process pool executor
PROCESS_POOL=5 # creates a process pool executor with a maximum of 5 processes.
# allowed concurrent instances
MAX_INSTANCES=3 # specify the maximum number of allowed concurrent instances of a job.


MAP = {
"RICARULEID":"ricaRuleId",
"RICARULE":"ricaRule",
"RICATYPEID":"ricaTypeId",
"RICASUBTYPEID":"ricaSubTypeId",
"RICAREQUESTOR":"ricaRequestor",
"RICAPURPOSE":"ricaPurpose",
"RICAINTERVALOF":"ricaIntervalOf",
"RICANEXTRUNDATE":"ricaNextRunDate",
"RICANEXTRUNTIME":"ricaNextRunTime",
"RICALASTRUNDATE":"ricaLastRunDate",
"RICALASTRUNTIME":"ricaLastRunTime",
"RICAACTION":"ricaAction",
"RICAIMPLICATIONS":"ricaImplications",
"RICAGROUPBY":"ricaGroupBy",
"RICARESPONDENT":"ricaRespondent",
"RICAOWNER":"ricaOwner",
"RICAINVESTIGATOR":"ricaInvestigator",
"RICANEXTOWNER":"ricaNextOwner",
"RICAOTHERRECEIVERS":"ricaOtherReceivers",
"RICAOTHERRECEIVER":"ricaOtherReceiver",
"RICAOTHERDESIGNATES":"ricaOtherDesignates",
"RICAENFORCER":"ricaEnforcer",
"RICADAILY":"ricaDaily",

"RICARUNMODE":"ricaRunMode",
"RICAWEEKLY":"ricaWeekly",
"RICAMONTHLY":"ricaMonthly",
"RICAQUARTERLY":"ricaQuarterly",
"RICAYEARLY":"ricaYearly",

"RICANEWRECORDSTATUS":"ricaNewRecordStatus",
"RICAMODALITY":"ricaModality",
"RICATOTALPERBATCH":"ricaTotalPerBatch",
"RICARESPONDENT":"ricaRespondent",
"RICASUGGESTEDRISK":"ricaSuggestedRisk",
"RICALIKELIHOOD":"ricaLikelihood",
"RICACONSEQUENCE":"ricaConsequence",
"RICAPRIORITY":"ricaPriority",
"RICADESCRIPTION":"ricaDescription",
"RICANOTIFYBEFOREDUE":"ricaNotifyBeforeDue",
"RICAOVERDUETIME":"ricaOverdueTime",
"RICAOVERDUEREPEAT":"ricaOverdueRepeat",
"RICAREPEATCHANGEAFTER":"ricaRepeatChangeAfter",
"RICAREPEATTIMECHANGE":"ricaRepeatTimeChange",
"RICAOVERDUERISKMATRIX":"ricaOverdueRiskMatrix",
"RICAOVERDUEPRIORITY":"ricaOverduePriority",
"RICAOVERDUENOTE":"ricaOverdueNote",
"RICAREGULATORYREPORT":"ricaRegulatoryReport",
"RICAREPORTWITHIN":"ricaReportWithin",
"RICAAUTOCLOSE":"ricaAutoClose",
"RICAAUTOSTATUS":"ricaAutoStatus",
"RICACLOSEAFTER":"ricaCloseAfter",
"RICACLOSERISK":"ricaCloseRisk",
"RICARUNSTATUS":"ricaRunStatus",
"RICASTATUSREASON":"ricaStatusReason",
"RICASTATUSDATE":"ricaStatusDate",
"RICASTATUSTIME":"ricaStatusTime",
"RICASTATUSINITIATOR":"ricaStatusInitiator",
"RICAUSERID":"ricaUserId",
"RICAUSEREMAIL":"ricaUserEmail",
"RICAUSERTITLE":"ricaUserTitle",
"RICAFIRSTNAME":"ricaFirstName",
"RICAMIDDLENAME":"ricaMiddleName",
"RICALASTNAME":"ricaLastName",
"RICAID":"ricaBranchId",
"RICABRANCHNAME":"branch_name",
"RICABRANCHMNEMONIC":"ricaBranchMnemonic", 
"ricaBranchName":"branch_name",
"RICACOUNTRY":"ricaCountry",
"RICASTATE":"ricaState",
"RICACOUNTYLG":"ricaCountyLg",
"RICAPHONE":"ricaPhone",
"RICAEMAIL":"ricaEmail",
"RICADATEOPEN":"ricaDateOpen",
"RICADATECLOSE":"ricaDateClose",
"RICABRANCHID":"ricaBranchId",
"RICACLUSTER":"ricaCluster",
"RICAZONE":"ricaZone",
"RICAREGION":"ricaRegion",
"RICACLASS":"ricaClass",
"RICAREMARKS":"ricaPerformance",
"RICAPERFORMANCE":"ricaRemarks", 
"RICAREMINDCOUNTER":"ricaRemindCounter", 
"RICAALERTSTATUS":"ricaAlertStatus", 
"RICAQUERYPANEL":"ricaQueryPanel", 
"RICAMODELFLAG":"ricaModelflag", 
"RICACOVERAGES":"ricaCoverages", 
"RICAUSERROLE":"ricaUserRole", 
"RICAUSERSTATUS":"ricaUserStatus", 
"RICADEFAULTOWNER":"ricaDefaultOwner", 
"RICADEFAULTRESPONDENT":"ricaDefaultRespondent", 
"RICADEFAULTINVESTIGATOR":"ricaDefaultInvestigator", 
"RICALICENSECODE":"ricaLicenseCode", 
 
"RICAALARMID": "ricaAlarmId",
    "RICACRETERIAVALUE1": "ricaCreteriaValue1",
    "RICACRETERIA1": "ricaCreteria1",
    "RICACRETERIAVALUE2": "ricaCreteriaValue2",
    "RICACRETERIA2": "ricaCreteria2",
    "RICACRETERIAVALUE3": "ricaCreteriaValue3",
    "RICACRETERIA3": "ricaCreteria3",
    "RICAALARMDESC": "ricaAlarmDesc",
    "RICAINDAY1": "ricaInDay1",
    "RICAIN2TO7DAYS": "ricaIn2To7Days",
    "RICAIN8TO14DAYS": "ricaIn8To14Days",
    "RICAIN15TO28DAYS": "ricaIn15To28Days",
    "RICAIN29DAYSTO3MONTHS": "ricaIn29DaysTo3Months",
    "RICAIN3MONTHSTO6MONTHS": "ricaIn3MonthsTo6Months",
    "RICAIN6MONTHSTO1YEAR": "ricaIn6MonthsTo1Year",
    "RICAIN1YEARTO3YEARS": "ricaIn1YearTo3Years",
    "RICAIN3YEARSTO5YEARS": "ricaIn3YearsTo5Years",
    "RICAINOVER5YEARS": "ricaInOver5Years",
    "RICAINFREQDAY1": "ricaInFreqDay1",
    "RICAINFREQ2TO7DAYS": "ricaInFreq2To7Days",
    "RICAINFREQ8TO14DAYS": "ricaInFreq8To14Days",
    "RICAINFREQ15TO28DAYS": "ricaInFreq15To28Days",
    "RICAINFREQ29DAYSTO3MONTHS": "ricaInFreq29DaysTo3Months",
    "RICAINFREQ3MONTHSTO6MONTHS": "ricaInFreq3MonthsTo6Months",
    "RICAINFREQ6MONTHSTO1YEAR": "ricaInFreq6MonthsTo1Year",
    "RICAINFREQ1YEARTO3YEARS": "ricaInFreq1YearTo3Years",
    "RICAINFREQ3YEARSTO5YEARS": "ricaInFreq3YearsTo5Years",
    "RICAINFREQOVER5YEARS": "ricaInFreqOver5Years",
    "RICAOUTDAY1": "ricaOutDay1",
    "RICAOUT2TO7DAYS": "ricaOut2To7Days",
    "RICAOUT8TO14DAYS": "ricaOut8To14Days",
    "RICAOUT15TO28DAYS": "ricaOut15To28Days",
    "RICAOUT29DAYSTO3MONTHS": "ricaOut29DaysTo3Months",
    "RICAOUT3MONTHSTO6MONTHS": "ricaOut3MonthsTo6Months",
    "RICAOUT6MONTHSTO1YEAR": "ricaOut6MonthsTo1Year",
    "RICAOUT1YEARTO3YEARS": "ricaOut1YearTo3Years",
    "RICAOUT3YEARSTO5YEARS": "ricaOut3YearsTo5Years",
    "RICAOUTOVER5YEARS": "ricaOutOver5Years",
    "RICAOUTFREQDAY1": "ricaOutFreqDay1",
    "RICAOUTFREQ2TO7DAYS": "ricaOutFreq2To7Days",
    "RICAOUTFREQ8TO14DAYS": "ricaOutFreq8To14Days",
    "RICAOUTFREQ15TO28DAYS": "ricaOutFreq15To28Days",
    "RICAOUTFREQ29DAYSTO3MONTHS": "ricaOutFreq29DaysTo3Months",
    "RICAOUTFREQ3MONTHSTO6MONTHS": "ricaOutFreq3MonthsTo6Months",
    "RICAOUTFREQ6MONTHSTO1YEAR": "ricaOutFreq6MonthsTo1Year",
    "RICAOUTFREQ1YEARTO3YEARS": "ricaOutFreq1YearTo3Years",
    "RICAOUTFREQ3YEARSTO5YEARS": "ricaOutFreq3YearsTo5Years",
    "RICAOUTFREQOVER5YEARS": "ricaOutFreqOver5Years",
    "RICARECORDDATE": "ricaRecordDate",

    "RICAALERTID": "ricaAlertId", 
    "RICACASEID": "ricaCaseId", 
    "RICANETLOSSAMOUNT": "ricaNetLossAmount", 
    "RICADISPOSITION": "ricaDisposition",
    "RICARISKASSESSMENT": "ricaRiskAssessment",
    "RICACREATEDATE": "ricaCreateDate",
    "RICACREATETIME": "ricaCreateTime",
    "RICASCENARIO": "ricaScenario",
    "RICASCENARIOID": "ricaScenarioId",
    "RICAFLOWTYPE": "ricaFlowType",
    "RICASTMPMAILSERVER": "ricaStmpMailServer",
    "RICASTMPMAILPORT": "ricaStmpMailPort",
    "RICASTMPMAILUSER": "ricaStmpMailUser",
    "RICASTMPMAILPASSWORD": "ricaStmpMailPassword",
    "SPECIAL_DATE": "special_date",
    "SPECIAL_TIME": "special_time",
    "RICASPECIALDATE": "special_date",
    "RICASPECIALTIME": "special_time",
    "RICABRANCHCODE": "branch",
     "ricaBranchCode": "branch",
    "RICABRANCHNAME": "branch_name",
    "BRANCH_NAME": "branch_name",
    "ACCOUNT_NAME": "account_name",
    "BRANCH": "branch",
    "AMOUNT": "amount",
    "ACCOUNT": "account",
    "TRANS_TYPE": "trans_type",
    "TRANS_ID": "trans_id",
    "REF_ID": "ref_id",
    "INPUTTER": "inputter",
    "VERIFIER": "verifier",
    "AUTHORISER": "authoriser",
    "TRANS_CODE": "trans_code",
    "CUSTOMER_NO": "customer_no",
    "CUSTOMER_NAME": "customer_name",
    "DETAILS": "details",
    "ENTRY_DATE": "entry_date",
    "RICAGROUPDESIGNATEID": "ricaGroupDesignateId",
    "RICAGROUPDESIGNATEEMAIL": "ricaGroupDesignateEmail",
    "RICAMAPPER": "ricaMapper",
    "RECORDID": "recordid",
    "ID": "ID",  
    "INPUTTER": "inputter",  
    "AUTHORISER": "authoriser",  
    "VERIFIER": "verifier",  
    "ACCOUNT_OFFICER": "account_officer",
    "RICAFOOTERLABEL": "ricaFooterLabel",
    "RICALICENSENOTIFYDUR": "ricaLicenseNotifyDur",
    "RICAEXPIRYDATE": "ricaExpiryDate",
    "RICAOTHERDESIGNATE": "ricaOtherDesignate",
    "RICACLIENTNAME": "ricaClientName",
    "ricaaccountid": "RICAACCOUNTID",
    "TRANSACTION_ID": "Transaction_ID",
    "TRANSACTION_TYPE": "Transaction_Type",
    "TRANSACTION_BRANCH": "Transaction_Branch",
    "TRANSACTION_NARRATIVE": "Transaction_Narrative",
    "TRANSACTION_DATE": "Transaction_Date",
    "TRANSACTION_TIME": "Transaction_Time",
    "INPUTTER": "Inputter",
    "TRANSACTION_MODE": "Transaction_Mode",
    "TRANSACTION_CURRENCY": "Transaction_Currency",
    "TRANSACTION_AMOUNT": "Transaction_Amount",
    "TRANSACTION_INDICATOR": "Transaction_Indicator",
    "TRANSACTION_ACCOUNT": "Transaction_Account",
    "TRANSACTION_LOCATION": "Transaction_Location",
    "TRANSACTION_DEVICE": "Transaction_Device",
    "RICACREATEALERT": "ricaCreateAlert",
}






 