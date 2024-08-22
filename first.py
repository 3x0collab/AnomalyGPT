
import random
from AnomalyPromptGRP.func import convert_time, format_int, format_int_bin, is_time_between, get_first, clean, get_from_account, get_from_branch, get_actual_designate_from_user, get_respondent_details_from_user, get_from_alertworkflow, get_multi_value, get_user,get_user_via_designate,replaceParams,removeDuplicates,to_number,get_spf,get_group_designate,get_designate_email,get_multi_emails,get_designate_via_user
from AnomalyPromptGRP.date import  create_time, calculate_duedate, calculate_remindcounter, isWhatD, isLastD_M, isWhatM, isOver5Y
from AnomalyPromptGRP.datehelper import create_date
from AnomalyPromptGRP.common import load_queries
from AnomalyPromptGRP.config import MAP
from AnomalyPromptGRP.doc import make_doc
import datetime
import json
import re
from urllib.parse import urljoin


columns = ["1 Day", "2-7 Days", "8-14 Days", "15-28 Days", "29 Days - 3 months",
		   "3 months - 6 months", "6 months - 1 year", "1 year - 3 years", "3 years - 5 years", "Over 5 years"]


def get_status(execute, status_id=""):	
	query = f""" select ricaModelflag from rica_status
	where ricaStatusId='{status_id}' """
	return get_first(execute(query))


def step_1(execute, scenario=""):
	query =  load_queries.get('GET_SCENARIO').format(
				scenario=scenario
				 )
	# print(query)
	return get_first(execute(query))


def step_2(execute, v_nextrundate, v_nextruntime, v_lastrundate, v_lastruntime,group_field,spf):
	print(f"getting {group_field} list",spf.get("ricaClientName","").lower())

	if group_field == "branch":
		if 'keystone' in spf.get("ricaClientName","").lower():
			query = load_queries.get('GET_BRANCH_1KEYSTONE').format(
				v_lastrundate=v_lastrundate,
				v_lastruntime=v_lastruntime,
				 )

		else:
			query = load_queries.get('GET_BRANCH_1').format(
					v_lastrundate=v_lastrundate,
					v_lastruntime=v_lastruntime,
					 )

	else: 
		query = load_queries.get('GET_BRANCH_2').format(
				group_field=group_field,
				v_lastrundate=v_lastrundate,
				v_lastruntime=v_lastruntime,
				 ) 

	print(query)
	groupList = execute(query)
	return groupList

def step_2_5(execute, v_nextrundate, v_nextruntime, v_lastrundate, v_lastruntime,group_field):

	query = load_queries.get('GET_DIS_ACCOUNT_1').format(
				v_lastrundate=v_lastrundate,
				v_lastruntime=v_lastruntime,
				 )

	print('get distinct account',query)
	groupList = execute(query)
	return groupList


def get_transaction_details(execute, v_nextrundate, v_nextruntime, v_lastrundate, v_lastruntime,account,branch):

	result_message = f"\nAll Transaction Details for account: {account} \n "

	query = load_queries.get('GET_ACCT_TRANSACTIONS').format(
				account=account,
				v_lastrundate=v_lastrundate,
				v_lastruntime=v_lastruntime,
				 ) 

	print('get latest transactions',query)
	customer_transactions = execute(query)
	count = 0
	for transactions in  customer_transactions:
		count +=1
		result_message += f" \n Transaction {count}:\n "
		for row in transactions:
			result_message += f"{str(row).replace('Transaction_','') }: {transactions[row]} \n "
		
	return customer_transactions, result_message

def run_instructions(model,prompt="Why is the earth green?"):
	tokens = []
	print('prompt:',prompt)
	with model.chat_session():
		for token in model.generate(prompt[0:4507], streaming=True):
			tokens.append(token)

	output_res = "".join(tokens)
	# print("Output result: ", output_res)
	if "no suspicious transactions detected" in output_res.lower() or "no suspicious" in output_res.lower():
		return None 
	return output_res


	
def step_3(execute, scenarioRecord={}, exactValue={}, 
	emails=[], v_nextrundate=None, v_nextruntime=None, 
	v_lastrundate=None, v_lastruntime=None,group_field=None,spf={},model='',APP_URL="" ):

	v_scenarioId = scenarioRecord["ricaRuleId"]
	v_scenario = scenarioRecord["ricaRule"]
	v_typeId = scenarioRecord["ricaTypeId"]
	v_subtypeId = scenarioRecord["ricaSubTypeId"]
	v_requestor = scenarioRecord["ricaRequestor"]
	v_intervalOf = scenarioRecord["ricaIntervalOf"] 
	v_implications = scenarioRecord["ricaImplications"]  # Memo
	v_actions = get_multi_value(execute, 'RuleBuilder_ricaAction', v_scenarioId)
	v_groupBy =  scenarioRecord.get("ricaGroupBy","BRANCH")

	v_createstatus = scenarioRecord.get("ricaNewRecordStatus")
	if v_createstatus == None:
		v_createstatus = 'New'

	v_singleBatch = scenarioRecord["ricaModality"]
	v_totalPerBatch = scenarioRecord["ricaTotalPerBatch"]

	v_riskAssessment = "High"
	v_suggestedRisk = scenarioRecord.get('ricaSuggestedRisk')

	v_likelihood = scenarioRecord.get("ricaLikelihood")
	v_consequence = scenarioRecord.get("ricaConsequence")
	v_priority = scenarioRecord.get("ricaPriority")
	v_description = scenarioRecord.get("ricaDescription")  # Memo

	v_notifyBeforeDue = scenarioRecord.get("ricaNotifyBeforeDue") 

	
	ricaRespondentOverdueTime = scenarioRecord.get("ricaRespondentOverdueTime") or 0
	ricaInvestigatorOverdueTime = scenarioRecord.get("ricaInvestigatorOverdueTime") or 0
	ricaOwnerOverdueTime = scenarioRecord.get("ricaOwnerOverdueTime")  or 0
	ricaRespondentOverdueRepeat = scenarioRecord.get("ricaRespondentOverdueRepeat") or 0
	ricaInvestigatorOverdueRepeat = scenarioRecord.get("ricaInvestigatorOverdueRepeat") or 0
	ricaOwnerOverdueRepeat = scenarioRecord.get("ricaOwnerOverdueRepeat")  or 0

	v_overdueRiskMatrix = scenarioRecord.get("ricaOverdueRiskMatrix")
	v_overduePriority = scenarioRecord.get("ricaOverduePriority")

	v_autoClose = scenarioRecord.get("ricaAutoClose")
	v_autostatus = scenarioRecord.get("ricaAutoStatus")
	v_closeAfter = scenarioRecord.get("ricaCloseAfter")
	v_closeRisk = scenarioRecord.get("ricaCloseRisk")

	v_otherReceivers  = ""
	ricaRespondent  = ""
	ricaRespondentDesignate  = ""
	ricaInvestigator  = ""
	ricaInvestigatorDesignate  = ""
	ricaOwner  = ""
	ricaOwnerDesignate  = ""
	ricaNextOwner  = ""
	ricaNextOwnerDesignate  = ""
	ricaEnforcer  = ""	 



	all_records = [] 
	exceptionId = ''

	spfRecords = spf
	exceptions = {}

	branch_rule = r"{\s*branch_code\s*}"
	if re.search(branch_rule,scenarioRecord.get('ricaQueryPanel')):
		group_field_value = exactValue.get(group_field)
	else:
		group_field_value = ''

	exceptions[group_field_value] = [] 

	default_variables  ={
	'v_lastruntime':v_lastruntime,
	'v_lastrundate':v_lastrundate,
	'v_nextrundate':v_nextrundate,
	'v_nextruntime':v_nextruntime,	   
	}

	if v_lastruntime == '0000':
		v_lastruntime = "00:00"
	if v_nextruntime == '0000':
		v_nextruntime = "00:00"


	if group_field == 'branch':
		default_variables['branch_code'] = group_field_value
	else:
		default_variables['group_field'] = f'RICA{group_field.upper()}'
		default_variables[f'group_field_value'] = group_field_value

	exceptionsQuery = scenarioRecord.get('ricaQueryPanel')

	distinct_accounts = step_2_5(execute, v_nextrundate,v_nextruntime, v_lastrundate, v_lastruntime, group_field)

	entryRecordList =  []


	if group_field == 'branch':
		# Check group for respondent, else check designate
		v_respondent, v_respondent_emails  = get_designate_email(execute,"ricaRespondent",scenarioRecord,spfRecords,group_field_value,group_field,entryRecordList)
		# print('v_respondent_emails',scenarioRecord.get('ricaRespondent'))
		emails["to"].extend(v_respondent_emails)
	else:
		v_respondent = group_field_value
		# print('v_respondent',v_respondent)
		emails["to"].append(get_user(execute, v_respondent, 'ricaUserEmail',is_active="en-109"))
		ricaAssignee = v_respondent  
		ricaRespondent = v_respondent
		ricaRespondentDesignate = get_designate_via_user(execute,v_respondent ) 

   
	# Check group for ricaInvestigator, else check designate
	v_investigator, v_investigator_emails  = get_designate_email(execute,"ricaInvestigator",scenarioRecord,spfRecords,group_field_value,group_field,entryRecordList)
	emails["cc"].extend(v_investigator_emails)


	# Check group for ricaOwner, else check designate
	v_owner, v_owner_emails  = get_designate_email(execute,"ricaOwner",scenarioRecord,spfRecords,group_field_value,group_field,entryRecordList)
	emails["cc"].extend(v_owner_emails)


	# Check group for ricaNextOwner, else check designate
	v_nextowner, v_nextowner_emails  = get_designate_email(execute,"ricaNextOwner",scenarioRecord,spfRecords,group_field_value,group_field,entryRecordList)
	emails["cc"].extend(v_nextowner_emails)

	
	# Check group for ricaEnforcer, else check designate
	v_enforcer, v_enforcer_emails  = get_designate_email(execute,"ricaEnforcer",scenarioRecord,spfRecords,group_field_value,group_field,entryRecordList)
	emails["cc"].extend(v_enforcer_emails)


	# This is multi-value field and also users id
	v_otherReceivers = get_multi_value(execute, 'RuleBuilder_Receivers', v_scenarioId)
	# print('v_otherReceivers',v_otherReceivers )
	if v_otherReceivers:
		v_otherReceivers = [ x.get("ricaOtherReceiver") for x in v_otherReceivers ]
		emails["cc"].extend([x['ricaUserEmail'] for x in get_multi_emails(execute, 'RuleBuilder_Receivers', v_scenarioId)])

	# volunteers		
	# This is multi-value field and also designates
	v_otherDesignates = get_multi_value(execute, 'RuleBuilder_OtherDesignates', v_scenarioId)
	designate_users = None

	for dsg in v_otherDesignates:
		designate_users = get_designate_email(execute,"ricaOtherDesignate",dsg,spfRecords,group_field_value,group_field,entryRecordList)
		if len(designate_users) > 1:
			emails["cc"].extend(designate_users[1])
	
	# print(f'Other designates {v_otherDesignates} and other recievers: {v_otherReceivers}')
	print(f'records found for {group_field}: {group_field_value}',len(entryRecordList))
	# print('here',",")
	# if len(entryRecordList) == 0:
	#	 continue

	branchId = group_field_value  


	v_disposition = 'TRUE POSITIVE'
	ricaDetailId = ''

	print("group_field_value",group_field_value,group_field,entryRecordList)
	
	ricaBatchId = f"{clean(v_scenarioId)}-{clean(branchId)}-{clean(v_nextrundate)}-{clean(v_nextruntime)}".upper()
	exceptionId = f"{clean(v_scenarioId)}-{branchId}-{clean(str(create_date(datetime.datetime.now())))}-{clean(datetime.datetime.now().strftime('%H:%M:%S.%f'))[0:8]}".upper()
	
	ricaBatchId = ricaBatchId
	ricaTypeId = v_typeId
	ricaSubTypeId = v_subtypeId
	ricaScenarioId = v_scenarioId
	ricaScenario = v_scenario
	ricaAlertStatus = v_createstatus
	
	ricaRiskAssessment = v_riskAssessment
	ricaSuggestedRisk = v_suggestedRisk
	ricaPriority = v_priority
	ricaBranchId = branchId
	branch_name = get_from_branch(execute, branchId, 'branch_name')
	ricaCluster = get_from_branch(execute, branchId, 'ricaCluster')
	ricaZone = get_from_branch(execute, branchId, 'ricaZone')
	ricaRegion = get_from_branch(execute, branchId, 'ricaRegion')

	ricaRespondent = v_respondent
	ricaRespondentDesignate = scenarioRecord.get("ricaRespondent")
	ricaInvestigator = v_investigator
	ricaInvestigatorDesignate = scenarioRecord.get("ricaInvestigator")
	ricaOwner = v_owner
	ricaOwnerDesignate =  scenarioRecord.get("ricaOwner")
	ricaNextOwner = v_nextowner
	ricaNextOwnerDesignate = scenarioRecord.get("ricaNextOwner")
	ricaEnforcer = v_enforcer

	ricaLikelihood = v_likelihood
	ricaConsequence = v_consequence
	ricaCreatedBy = 'SYSTEM'
	ricaCreatedDate = v_nextrundate
	ricaCreatedTime = v_nextruntime
	ricaCreateDate = create_date(datetime.date.today())
	ricaCreateTime = create_time(datetime.datetime.now())

	due_date = calculate_duedate(datetime.datetime.now(), ricaRespondentOverdueTime)
	ricaDueDate = due_date['date']
	ricaDueTime = due_date['time'] 

	ricaLastActivity = ""
	ricaLastActivist = "SYSTEM"
	ricaLastActivityDate = create_date(datetime.date.today())
	radporLastActivityTime = v_nextruntime
	ricaCustomerNo = ""

	ricaStandardComment = ""
	ricaAlertComment = ""

	ricaRecoveryDate = create_date(datetime.date.today())
	ricaTotalAmountInvolved = 0.00 #int(entry.get('amount', 0))
	ricaAmount   = 0.00 #int(entry.get('amount', 0))
	ricaAvertedAmount   = 0.00
	ricaRecoverAmount   = 0.00
	ricaNetLossAmount   = 0.00  
	ricaRecoveryComment = ""
	ricaLastRunDate = v_lastrundate
	ricaLastRunTime = v_lastruntime
	ricaNextRunDate = v_nextrundate
	ricaNextRunTime = v_nextruntime
	ricaAssignor = v_owner

	ricaOldRespondent = ""
	ricaNewRespondent = ""
	ricaOldInvestigator = ""
	ricaNewInvestigator = ""
	ricaOldOwner = ""
	ricaNewOwner = ""
	ricaOldNextOwner = ""
	ricaNewNextOwner = ""
	ricaNewAssignee = ""
	ricaNoAttachment = 0
	ricaRiskScoring = ""
	ricaReturnStatus = ""
	ricaReturnTo = ""

	ricaValidateOverride = ""
	ricaAutoCaseCreate = ""
	ricaRegReportFlag = ""
	ricaReportWithinDate = create_date(datetime.date.today())
	ricaReportWithinTime = v_nextruntime
	ricaRegReportDate = create_date(datetime.date.today())
	ricaRegReportTime = create_time(datetime.datetime.now())

	ricaRegReportStatus = ""

	ricaNotifyBeforeDue = v_notifyBeforeDue 

	ricaOverdueRiskMatrix = v_overdueRiskMatrix
	ricaOverduePriority = v_overduePriority

	ricaExpectedRemindTime = create_time(datetime.datetime.now())
	ricaRemindCounter = get_from_alertworkflow(execute, v_createstatus, None, 'ricaRemindCounter',0)

	counter_date = calculate_remindcounter()

	ricaRemindNextDate = counter_date['date']
	ricaRemindNextTime = counter_date['time']

	ricaOverdueCounter = 0
	ricaAutoClose = v_autoClose
	ricaAutoStatus = v_autostatus
	ricaCloseAfter = v_closeAfter
	ricaCloseRisk = v_closeRisk
	ricaNewAlertStatus = ""
	ricaStatusReason = ""

	ricaNewAssigneeRole = ""
	ricaNewAssigneeName = ""
	ricaReassignRole = ""
	ricaReassignCriteria = ""
	ricaReassignee = ""
	ricaFindings = ""
	ricaActions = ""
	ricaGeneralComment = ""
	ricaDecision = ""
	ricaNewDisposition = ""
	ricaDecisionReason = ""
	ricaFinalRiskMatrix = ""
	ricaFinalLikelihood = ""
	ricaFinalConsequence = ""
	ricaFinalPriority = 0

	ricaOverrideDate = create_date(datetime.date.today())
	ricaOverrideTime = create_time(datetime.datetime.now())
	ricaTransDate = create_date(datetime.date.today())
	ricaTransTime = create_time(datetime.datetime.now())

	ricaEntityId = ""
	ricaEntityName = ""
	ricaHighlights = ""
	ricaFlowType = ""
	ricaCustomerNo = ""
	ricaCustomeName = ""
	ricaAccountNo = ""
	ricaTransId = ""
	ricaCurrency = ""
	ricaInputter = ""
	ricaAuthoriser = ""
	ricaAccountOfficer = ""
	ricaVerifier = ""
	ricaAssignee = v_respondent


	respondent_list = {}
	# print('\n\nexceptionId',exceptionId,'\n\n')
	exceptions[group_field_value].append(exceptionId)

	accountsList = []

	for acct in distinct_accounts:
		entryRecordList, trans_details = get_transaction_details(execute, v_nextrundate,v_nextruntime, v_lastrundate, v_lastruntime, acct.get('RICAACCOUNTID'),group_field_value)
		if len(entryRecordList) < 8:
			continue
		prompt = scenarioRecord.get('ricaQueryPanel')+'\n'+trans_details
		match_pattern = run_instructions(model, prompt)
		if match_pattern:
			accountsList.append(match_pattern)

		print('am here', match_pattern)
		if match_pattern and '205' in scenarioRecord.get('ricaCreateAlert') :

			for entry in entryRecordList[0:1]:
				journalId = str(exceptionId)+'-'+ str(entry.get("Transaction_ID")) 
				ricaEntityId = entry.get("ref_id","")
				ricaEntityName = entry.get('account_name',"")
				ricaHighlights = entry.get("Transaction_Narrative","")
				ricaFlowType = 'INFLOW' if entry.get('TRANSACTION_INDICATOR') == 'C' else  'OUTFLOW' if entry.get('TRANSACTION_INDICATOR') == 'D' else "" 
				
				if entry.get("Transaction_Account") != None and not entry.get("Transaction_Account"):
					ricaCustomerNo = get_from_account(execute, entry.get("Transaction_Account"), 'RICACUSTOMERID')
					ricaCustomerName = get_from_account(execute, entry.get("Transaction_Account"), 'RICAACCOUNTNAME')

				ricaAccountNo = entry.get("Transaction_Account")
				ricaAccountName = entry.get("account_name")
				ricaTotalAmountInvolved = float(entry.get('TRANSACTION_AMOUNT', 0.00))
				ricaAmount   = float(entry.get('TRANSACTION_AMOUNT', 0.00))

				ricaTransId = entry.get('Transaction_ID')
				ricaInputter = entry.get('Inputter',"")
				ricaAuthoriser = entry.get('Authoriser',"")
				ricaAccountOfficer = entry.get('account_officer',"")
				ricaVerifier = entry.get('verifier',"")
				ricaCurrency = entry.get('Transaction_Currency')


				write_alertconcat_query = load_queries.get('UPDATE_ALERTSCONCAT').format(
						journalId=journalId,
						exceptionId=exceptionId,
						ricaScenarioId=ricaScenarioId,
						ricaEntityId=ricaEntityId,
						ricaCustomerNo=ricaCustomerNo,
						ricaAccountNo=ricaAccountNo,
						branchId=branchId,
						ricaNewDisposition=ricaNewDisposition,
						ricaRiskAssessment=ricaRiskAssessment,
						ricaAmount=ricaAmount,
						ricaAvertedAmount=ricaAvertedAmount,
						ricaRecoverAmount=ricaRecoverAmount,
						ricaNetLossAmount=ricaNetLossAmount,
						ricaCreateDate=ricaCreateDate,
						ricaCreateTime=ricaCreateTime,
						 )   

				try:
					# pass
					execute(write_alertconcat_query,update=True, commit=True)
					print('write saved-concat')
				except Exception as e:
					print('write error-concat: ', e)



				if not v_respondent:
					v_respondent = spfRecords.get("ricaDefaultRespondent") 
				if not v_investigator:
					v_investigator = spfRecords.get("ricaDefaultInvestigator")
				if not v_owner:
					v_owner = spfRecords.get("ricaDefaultOwner") 



				write_query = load_queries.get('UPDATE_ALERTQUERY').format(
					exceptionId=exceptionId,
					ricaBatchId= ricaBatchId,
					ricaTypeId= ricaTypeId,
					ricaSubTypeId= ricaSubTypeId,
					ricaScenarioId= ricaScenarioId,
					ricaScenario= ricaScenario,
					ricaEntityId= ricaEntityId,
					ricaEntityName= ricaEntityName,
					ricaHighlights= ricaHighlights,
					ricaAlertStatus= ricaAlertStatus,
					ricaFlowType= ricaFlowType,
					ricaAssignee= ricaAssignee,
					ricaAssignor= ricaAssignor,
					ricaRiskAssessment= ricaRiskAssessment,
					ricaSuggestedRisk= ricaSuggestedRisk,
					ricaPriority= ricaPriority,
					ricaBranchId= ricaBranchId,
					branch_name= branch_name,
					ricaCluster= ricaCluster,
					ricaZone= ricaZone,
					ricaRegion=  ricaRegion,
					ricaRespondent= ricaRespondent,
					ricaRespondentDesignate= ricaRespondentDesignate,
					ricaInvestigator= ricaInvestigator,
					ricaInvestigatorDesignate= ricaInvestigatorDesignate,
					ricaOwner= ricaOwner,
					ricaOwnerDesignate= ricaOwnerDesignate,
					ricaNextOwner= ricaNextOwner,
					ricaNextOwnerDesignate= ricaNextOwnerDesignate,
					ricaEnforcer= ricaEnforcer,
					ricaLikelihood= ricaLikelihood,
					ricaConsequence= ricaConsequence,
					ricaCreatedBy= ricaCreatedBy,
					ricaCreateDate= ricaCreateDate,
					ricaCreateTime= ricaCreateTime,
					ricaDueDate= ricaDueDate,
					ricaLastActivity= ricaLastActivity,
					ricaLastActivist= ricaLastActivist,
					ricaLastActivityDate= ricaLastActivityDate,
					radporLastActivityTime=  radporLastActivityTime,
					ricaCustomerNo= ricaCustomerNo,
					ricaAccountNo= ricaAccountNo,
					ricaAccountName= ricaAccountName,
					ricaTransId= ricaTransId,
					ricaStandardComment= ricaStandardComment,
					ricaAlertComment= ricaAlertComment,
					ricaRecoveryDate= ricaRecoveryDate,
					ricaCurrency= ricaCurrency,
					ricaAmount= ricaAmount,
					ricaTotalAmountInvolved= ricaTotalAmountInvolved,
					ricaAvertedAmount= ricaAvertedAmount,
					ricaRecoverAmount= ricaRecoverAmount,
					ricaNetLossAmount= ricaNetLossAmount,
					ricaRecoveryComment= ricaRecoveryComment,
					ricaLastRunDate= ricaLastRunDate,
					ricaLastRunTime= ricaLastRunTime,
					ricaNextRunDate= ricaNextRunDate,
					ricaNextRunTime= ricaNextRunTime,
					ricaOldRespondent= ricaOldRespondent,
					ricaNewRespondent= ricaNewRespondent,
					ricaOldInvestigator= ricaOldInvestigator,
					ricaNewInvestigator= ricaNewInvestigator,
					ricaOldOwner= ricaOldOwner,
					ricaNewOwner= ricaNewOwner,
					ricaOldNextOwner= ricaOldNextOwner,
					ricaNewNextOwner= ricaNewNextOwner,
					ricaNewAssignee= ricaNewAssignee,
					ricaNoAttachment= ricaNoAttachment,
					ricaRiskScoring= ricaRiskScoring,
					ricaReturnStatus= ricaReturnStatus,
					ricaReturnTo= ricaReturnTo,
					ricaValidateOverride= ricaValidateOverride,
					ricaAutoCaseCreate= ricaAutoCaseCreate,
					ricaRegReportFlag= ricaRegReportFlag,
					ricaReportWithinDate= ricaReportWithinDate,
					ricaReportWithinTime= ricaReportWithinTime,
					ricaRegReportDate= ricaRegReportDate,
					ricaRegReportTime= ricaRegReportTime,
					ricaRegReportStatus= ricaRegReportStatus,
					ricaNotifyBeforeDue= ricaNotifyBeforeDue,
					ricaRespondentOverdueTime= ricaRespondentOverdueTime,
					ricaInvestigatorOverdueTime= ricaInvestigatorOverdueTime,
					ricaOwnerOverdueTime= ricaOwnerOverdueTime,
					ricaRespondentOverdueRepeat= ricaRespondentOverdueRepeat,
					ricaInvestigatorOverdueRepeat= ricaInvestigatorOverdueRepeat,
					ricaOwnerOverdueRepeat=  ricaOwnerOverdueRepeat,
					ricaOverdueRiskMatrix= ricaOverdueRiskMatrix,
					ricaOverduePriority= ricaOverduePriority,
					ricaExpectedRemindTime= ricaExpectedRemindTime,
					ricaRemindCounter= ricaRemindCounter,
					ricaRemindNextDate= ricaRemindNextDate,
					ricaRemindNextTime= ricaRemindNextTime,
					ricaOverdueCounter= ricaOverdueCounter,
					ricaAutoClose= ricaAutoClose,
					ricaAutoStatus= ricaAutoStatus,
					ricaCloseAfter= ricaCloseAfter,
					ricaCloseRisk  = ricaCloseRisk,
					ricaNewAlertStatus = ricaNewAlertStatus ,
					ricaStatusReason= ricaStatusReason,
					ricaNewAssigneeRole  = ricaNewAssigneeRole  ,
					ricaNewAssigneeName= ricaNewAssigneeName,
					ricaReassignRole= ricaReassignRole,
					ricaReassignCriteria= ricaReassignCriteria,
					ricaReassignee= ricaReassignee,
					ricaFindings= ricaFindings,
					ricaActions= ricaActions,
					ricaGeneralComment= ricaGeneralComment,
					ricaDecision= ricaDecision,
					ricaNewDisposition= ricaNewDisposition,
					ricaDecisionReason= ricaDecisionReason,
					ricaFinalRiskMatrix= ricaFinalRiskMatrix,
					ricaFinalLikelihood= ricaFinalLikelihood,
					ricaFinalConsequence= ricaFinalConsequence,
					ricaFinalPriority= ricaFinalPriority,
					ricaOverrideDate= ricaOverrideDate,
					ricaOverrideTime= ricaOverrideTime,
					ricaTransDate= ricaTransDate,
					ricaTransTime= ricaTransTime,
					ricaDueTime= ricaDueTime,
					ricaInputter= ricaInputter,
					ricaAuthoriser= ricaAuthoriser,
					ricaAccountOfficer= ricaAccountOfficer,
					ricaVerifier = ricaVerifier
						) 

				# print(write_query)
				print("write_query 1")
				try:
					# pass
					check_q = f"""select ricaAlertId from rica_alerts
					where ricaAlertId='{exceptionId}'"""
					check_q_res = execute(check_q)
					if not len(check_q_res):
						execute(write_query,update=True, commit=True)
						print('write saved0')

				except Exception as e:
					print('write error0: ', e)



			
			if len(entryRecordList):
				exceptionResult = step_4(entryRecordList)
				ricaScenarioId = scenarioRecord.get("ricaRuleId")
				# exceptionId = f"{clean(ricaScenarioId)}-{clean(v_nextrundate)}-{clean(datetime.datetime.now().strftime('%H:%M:%S.%f'))[0:8]}"
				ricaExceptionDescription =  scenarioRecord.get("ricaRule")
				ricaExceptionIndicator = ''
				ricaExceptionRunTime = create_time(datetime.datetime.now())
				ricaExceptionRunDate = create_date(datetime.date.today())
				try:
					ricaOtherReceivers = json.dumps(v_otherReceivers or [])
					ricaBranchs = branchId
				except Exception as e:
					ricaOtherReceivers = ""
					ricaBranchs = ""



				write_query2 =  load_queries.get('UPDATE_EXCEPTION_OUTPUT').format(
					exceptionId= exceptionId,
					ricaScenarioId= ricaScenarioId,
					ricaExceptionDescription= ricaExceptionDescription,
					ricaBranchs= ricaBranchs,
					ricaExceptionIndicator= ricaExceptionIndicator,
					ricaRespondent= ricaRespondent,
					ricaRespondentDesignate= ricaRespondentDesignate,
					ricaInvestigator= ricaInvestigator,
					ricaInvestigatorDesignate= ricaInvestigatorDesignate,
					ricaOwner= ricaOwner,
					ricaOwnerDesignate= ricaOwnerDesignate,
					ricaNextOwner= ricaNextOwner,
					ricaNextOwnerDesignate= ricaNextOwnerDesignate,
					ricaEnforcer= ricaEnforcer,
					ricaOtherReceivers= ricaOtherReceivers,
					exceptionResult= exceptionResult.replace("'","''"),
					ricaExceptionRunTime= ricaExceptionRunTime,
					ricaExceptionRunDate= ricaExceptionRunDate,

					) 
				try:
					# pass
					execute(write_query2,update=True, commit=True, bind_dicts={"exceptionResult":exceptionResult.replace("'","''")})
					print('write saved2 query')

				except Exception as e:
					print('write error2: ', e)

		send_email_out(execute,emails, spfRecords,scenarioRecord, entryRecordList,match_pattern,APP_URL,list(set(exceptions[group_field_value])))


	print("we're at the end")
	return (entryRecordList,exceptions,accountsList)
	

def send_email_out(cursor_execute,emails,spf,scenarioRecord, entryRecordList,match_pattern,APP_URL,exceptions):
	print("Send out email",emails)
	if len(entryRecordList) > 0:
		fields =  list(entryRecordList[0].keys()) 
	fields = [ MAP.get(x,x) for x in fields ]
	z = entryRecordList
	z = list(map(lambda e: {**e,'RISK':scenarioRecord['ricaSuggestedRisk']} , z)) 
	template_var = {
		"emails": emails,
		 'scenario_id': scenarioRecord["ricaRuleId"], 
		'scenario': scenarioRecord["ricaRule"], 
		'implications': scenarioRecord["ricaImplications"],
		'actions': [x['ricaAction'] for x in get_multi_value(cursor_execute, 'Scenario_ricaAction', scenarioRecord["ricaRuleId"]) ],
			 "exceptions": [{'url':f"{urljoin(APP_URL,'#login')}?refer=true&link=Alerts_Management&args={x}",'name':x} for x in exceptions ],
			  "analysis": [],
			"xlsx_attach":[],
			"footer":"",
			"expired_notification":"",
			"match_pattern":match_pattern,
	}
	current_branch = ""
	make_doc([], z, z, branch=[{'branch': ''}], current_branch=current_branch ,
			 xlsx=[], template_var=template_var,spf=spf,columns=fields,group_field='branch')



def step_4(journal=[]):
	try:
		table = "<table ><tr>"
		fields = journal[0].keys()
		for x in fields:
			table = table + f"<th>{x}</th>"
		table = table + "</tr>"
		for jn in journal:
			fields = jn.values()
			table = table + "<tr>"
			for x in fields:
				table = table + f"<th>{x}</th>"
			table = table + "</tr>" 
		table = table + "</table>"
	except Exception as e:
		print('step4',e)
	return table






def step_6(entryRecordList=[],branchId="",group_field="branch"):
	try:

		filterBranch = entryRecordList
		if branchId:
			filterBranch = list(filter(lambda e:e.get(group_field)==branchId,entryRecordList ))
		selectAccountsOnly = list(map(lambda e:e.get('account'),filterBranch ))
		selectAccountsOnly = list(filter(lambda e:e ,selectAccountsOnly ))
		return list(set(selectAccountsOnly))
	except Exception as e:
		print('Step 6 \n', e)
		return []

