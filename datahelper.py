
import numpy as np
import pandas as pd
import random
from AnomalyPromptGRP.func import convert_time, format_int, format_int_bin, is_time_between, get_first, clean, get_from_account, get_from_branch, get_actual_designate_from_user, get_respondent_details_from_user, get_from_alertworkflow, get_multi_value, get_user,getExceptionsData,getAlarm
from AnomalyPromptGRP.date import create_date, create_time, calculate_duedate, calculate_remindcounter # isWhatD, isLastD_M, isWhatM, isOver5Y
import datetime
from AnomalyPromptGRP.doc import create_pie_chart,create_bar_chart,create_line_chart
from AnomalyPromptGRP.datehelper import dateSplit,isToday,isWhatD,isLastD_M,isWhatM,isOver5Y
import functools
import random
from AnomalyPromptGRP.xlsx import create_excel
import copy

columns = [ 'Today', '2 - 7 Days','8 - 14 Days','15 - 28 Days','29 Days - 3 Months',
 'Above 3 Months - 6 Months','Above 6 Months - 1 Year','Above 1 Year - 3 Years'
 ,'Above 3 Years - 5 Years', 'Above 5 Years']

 


def createDynamicColors():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

 
def defaultNumField(field):
 	return int(field) if field else 0

 
def formatNumber(field):
 	return int(field) if field else 0

 
def getCummulative(c={},scheme={}):
	total = 0
	if not c:
		c = {}
	cummulative = scheme
	for key in scheme:
		if ((key != 'metric') and (key != 'Total')):
			total  = total + c.get(key,0)
			cummulative[key]  =  total	 

	return cummulative


def getGap(inflow={},outflow={},scheme={}):
	if not inflow:
		inflow = {}
	if not outflow:
		outflow = {}

	for key in inflow:
		if (key != 'metric' and key != 'Total'):
			scheme[key]  =  defaultNumField(inflow.get(key)) - defaultNumField(outflow.get(key))

	return scheme



def getAverages(data={},total=0,scheme={}):
	if not data:
		data = {}
	for key in data:
		if (key == 'metric' and key == 'Total'):
			scheme[key]  =  round( Number(data[key]/total) if defaultNumField(data[key]/total) else defaultNumField(data[key]/total),2)
	return scheme

def getMax(data=[], scheme={}):
	if len(data) > 0:
		for key in scheme:
			if key == 'metric' and key == 'Total':
				scheme[key]  = sorted(data, key=lambda i: i[key],reverse=True)[0][key]

	return scheme


def getMin(data=[], scheme={}):
	if len(data) > 0:
		for key in scheme:
			if key == 'metric' and key == 'Total':
				scheme[key]  = sorted(data, key=lambda i: i[key])[0][key]

	return scheme




def genInflowOutflowAnalytics(data=[]):
	scheme = {}
	scheme['metric'] = ""
	scheme["Today"] = 0
	scheme["2 - 7 Days"] = 0
	scheme["8 - 14 Days"] = 0
	scheme["15 - 28 Days"] = 0
	scheme["29 Days - 3 Months"] = 0
	scheme["Above 3 Months - 6 Months"] = 0
	scheme["Above 6 Months - 1 Year"] = 0
	scheme["Above 1 Year - 3 Years"] = 0
	scheme["Above 3 Years - 5 Years"] = 0
	scheme["Above 5 Years"] = 0 
	scheme["Total"] = 0 


	scheme_divider = {
	'metric': "","Today" : "","2 - 7 Days" : "","8 - 14 Days" : "","15 - 28 Days" : "",
	"29 Days - 3 Months" : "","Above 3 Months - 6 Months" : "","Above 6 Months - 1 Year" : "",
	"Above 1 Year - 3 Years" : "","Above 3 Years - 5 Years" : "","Above 5 Years" : "","Total" : "", 
	}

	scheme_copy =  {}
 
	inflow_results = {}

	total_Inflow = {}

	cummulative_Inflow = {}

	outflow_results = {}
	
	total_Outflow = {}


	cummulative_Outflow = {}

	gap = {}
	cummulative_gap = {}

	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Inflow %Contributed"
	inflow_percent = scheme_copy

	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Outflow %Contributed"
	outflow_percent = scheme_copy


	scheme_divider['metric'] = "Frequency Count"
	scheme_line = scheme_divider

	average_Inflow = {}
	minimum_Inflow = {}
	maximum_Inflow = {}

	average_Outflow = {}
	minimum_Outflow = {}
	maximum_Outflow = {}

	inflow_freq_results = {}
	total_freq_Inflow = {}

	outflow_freq_results = {}
	total_freq_Outflow = {}

	chart_data = []


	for eachData in data:
		objKey = f'{eachData.get("trans_type")}' 

		if eachData["trans_code"] == 'C':
			scheme['metric'] = objKey

			if not inflow_results.get(objKey): 
				inflow_results[objKey] = scheme
			
			inflow_results = dateSplit(inflow_results,objKey,eachData)

			if not total_Inflow.get("Total Inflow"):  
				scheme['metric'] = "Total Inflow"
				total_Inflow["Total Inflow"] = scheme

			total_Inflow = dateSplit(total_Inflow,"Total Inflow",eachData)




		if eachData.get("trans_code") == 'D':
			scheme['metric'] = objKey

			if not outflow_results.get(objKey):
				outflow_results[objKey] = scheme

			outflow_results = dateSplit(outflow_results,objKey,eachData)

			if not total_Outflow.get("Total Outflow"):
			  	scheme['metric'] = "Total Outflow"
			  	total_Outflow["Total Outflow"] = scheme

			total_Outflow = dateSplit(total_Outflow,"Total Outflow",eachData)



		if eachData.get("trans_code") == 'C':
			scheme['metric'] = objKey

			if not inflow_freq_results.get(objKey):
				inflow_freq_results[objKey] = scheme

			inflow_freq_results = dateSplit(inflow_freq_results,objKey,eachData,'frequency')

			if not total_freq_Inflow.get("Total Inflow Freq."):
				scheme['metric'] = "Total Inflow Freq."
				total_freq_Inflow["Total Inflow Freq."] = scheme

			total_freq_Inflow = dateSplit(total_freq_Inflow,"Total Inflow Freq.",eachData,'frequency')




		if eachData.get("trans_code") == 'D':
			scheme['metric'] = objKey

			if not outflow_freq_results.get(objKey):
				outflow_freq_results[objKey] = scheme

			outflow_freq_results = dateSplit(outflow_freq_results,objKey,eachData,'frequency')

			if not total_freq_Outflow.get("Total Outflow Freq."):
				scheme['metric'] = "Total Outflow Freq."
				total_freq_Outflow["Total Outflow Freq."] = scheme

			total_freq_Outflow = dateSplit(total_freq_Outflow,"Total Outflow Freq.",eachData,'frequency')


		eachData = dateSplit(inflow_results,objKey,eachData,'map_amount')


	# print('======>',total_Outflow)

	scheme_copy = {}
	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Cummulative Inflow"
	cummulative_Inflow = getCummulative(total_Inflow.get('Total Inflow'), scheme_copy)


	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Cummulative Outflow"
	cummulative_Outflow = getCummulative(total_Outflow.get('Total Outflow'), scheme_copy)


	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "GAP"
	gap = getGap(total_Inflow.get('Total Inflow'),total_Outflow.get('Total Outflow'),scheme_copy)


	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Cummulative GAP"
	cummulative_gap = getCummulative(gap, scheme_copy)



	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Average (Inflow)"
	average_Inflow = getAverages(total_Inflow.get('Total Inflow'),len(inflow_results.items()),scheme_copy)

	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Minimum (Inflow)"
	minimum_Inflow =  getMin(inflow_results.items(),scheme_copy)


	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Maximum (Inflow)"
	maximum_Inflow =  getMax(inflow_results.items(),scheme_copy)


	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Average (Outflow)"
	average_Outflow = getAverages(total_Outflow.get('Total Outflow')  ,len(inflow_results.items()),scheme_copy)

	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Minimum (Outflow)"
	minimum_Outflow =  getMin(inflow_results.items(),scheme_copy)


	scheme_copy =  copy.copy(scheme)
	scheme_copy['metric'] = "Maximum (Outflow)"
	maximum_Outflow =  getMax(inflow_results.items(),scheme_copy)

	# print('dfk',inflow_results.items(),inflow_results)

	calc_data = [
		*[inflow_results[x] for x in inflow_results],total_Inflow.get('Total Inflow',{**scheme,'metric':"Total Inflow"}),
		*[outflow_results[x] for x in outflow_results],total_Outflow.get('Total Outflow',{**scheme,'metric':"Total Outflow"} ),
		gap,cummulative_Inflow,cummulative_Outflow,cummulative_gap,inflow_percent,outflow_percent,
		average_Inflow,minimum_Inflow,maximum_Inflow,average_Outflow,minimum_Outflow,maximum_Outflow,
		scheme_line,
		*[inflow_freq_results[x] for x in inflow_freq_results],total_freq_Inflow.get('Total Inflow Freq.',{**scheme,'metric':"Total Inflow Freq."}),
		*[outflow_freq_results[x] for x in outflow_freq_results],total_freq_Outflow.get('Total Outflow Freq.',{**scheme,'metric':"Total Outflow Freq."})
	 ]


	ret_data = {
		 'columns':list(scheme.keys()),
		'data': calc_data,
		'chart_data':data
	}
	return ret_data






def groupRecordInSelected(data=[], property=""):
	branchObj = {}
	for eachData in data:
		objKey = f'{eachData[property]}'
		if (branchObj.get(objKey)):
			branchObj[objKey].append(eachData)
		else:
			branchObj[objKey] = [eachData]

	return branchObj



def calculateCounterTrans(dataObject,calc_field):
	calculatedArray = {}
	for each in dataObject:
		eachBranchRecords = dataObject[each]
		calculatedArray[each] = 0

		for eachData in eachBranchRecords:
			calculatedArray[each] = int(calculatedArray[each]) +  (eachData[calc_field] if calc_field else 1)

	return calculatedArray


def generateScheme(dataFilterData=[], field="ricaRiskAssessment"):
	result = {}
	for eachData in dataFilterData:
		objKey = f'{eachData[field]}'
		if eachData.get(objKey):
			if not result.get(objKey):
				result[objKey] = 0
	return result


def insertDataHelper(todayData, eachData, notSelected,expected=0):
	todayData = { **todayData, 'Total Amount Involved': todayData['Total Amount Involved'] + formatNumber(eachData["ricaNetLossAmount"]) }
	if (eachData.get('ricaAlertId') ):
		todayData = { **todayData, 'Alerts Freq': todayData['Alerts Freq'] + 1 }
	
	if (eachData.get('ricaCaseId') ):
		todayData = { **todayData, 'Cases Freq': todayData['Cases Freq'] + 1 }
	
	objKey = eachData.get("ricaRiskAssessment")
	if (todayData.get(objKey) ):
		todayData = { **todayData, [objKey]: todayData[objKey] + 1 }

	if (eachData.get("ricaDisposition") == 'True Positive' ):
		todayData = { **todayData, 'True Positive': todayData['True Positive'] + 1 }

	return todayData


chart_columns =[ 'Today', '2 - 7 Days','8 - 14 Days','15 - 28 Days','29 Days - 3 Months',
 'Above 3 Months - 6 Months','Above 6 Months - 1 Year','Above 1 Year - 3 Years'
 ,'Above 3 Years - 5 Years', 'Above 5 Years']



def getChart3Data(data=[], columns = chart_columns, title="",filename=""):
	return create_pie_chart(data, columns,title,filename)


def getBarChartData(dataFilterData, key_columns=['ricaLinkZone','ricaRiskAssessment'],title="", map={},columns=[]):
	return create_bar_chart(dataFilterData, key_columns,title)



		 
def renderGridAmountChart(analysisData=[]):
	chartA1A = getChart3Data(list(filter(lambda e:e["trans_code"]=='C',analysisData["chart_data"])),['RICADATETYPE','amount'],'Amount Transaction Types (Inflow)' )
	chartA1B = getChart3Data(list(filter(lambda e:e["trans_code"]=='D',analysisData["chart_data"])),['RICADATETYPE','amount'],'Amount Transaction Types (Outflow)')
	chartA2A  = getLineChartData(analysisData["chart_data"], ['RICADATETYPE','trans_code','amount'],'IN-OUT Flow Amount',{'C':"Total Inflow",'D':'Total Outflow'},chart_columns )
	
	return (chartA1A,chartA1B,chartA2A)

def renderGridFreqChart(analysisData=[]):
	chartB1A = getChart3Data(list(filter(lambda e:e["trans_code"]=='C',analysisData["chart_data"])),['RICADATETYPE',''],'Freq. Transaction Types (Inflow)' )
	chartB1B = getChart3Data(list(filter(lambda e:e["trans_code"]=='D',analysisData["chart_data"])),['RICADATETYPE',''],'Freq. Transaction Types (Outflow)')
	chartB2A  = getLineChartData(analysisData["chart_data"], ['RICADATETYPE','trans_code',''],'IN-OUT Flow Freq.',{'C':"Total Inflow",'D':'Total Outflow'},chart_columns )
	return (chartB1A,chartB1B,chartB2A)

 

def renderExceptionData(exceptionData):
	pass
	# return calculateDataForException(exceptionData.data,alarm)
	

def renderExceptionFreqChart(flowType='Inflow',exceptionData=[]):
	chartC1A = getChart3Data(exceptionData["data"][0:10],['metric','Total Amount Involved'],f'{flowType} (Amount Involved)' )
	chartC1B  = getLineChartData(exceptionData["chart_data"], ['RICADATETYPE','exDif','exDifValue'],f'3 - Month {flowType} Analysis',type_='bar' )
	chartC1C = getChart3Data(exceptionData["initial_data"],['ricaRiskAssessment',''],f'{flowType} Risk Assessment')
	return (chartC1A,chartC1B,chartC1C)




def renderTimeSeriesChart(flowType="Inflow",data=[]):
	chart1  = getLineChartData(data.initial_data, ['RICADATETYPE','special_time','amount'],f'3 - Month {flowType} Time Series',{'C':"Total Inflow",'D':'Total Outflow'} ,chart_columns)

def renderAlertCasesFreqChart(usedData):
	chart1  = getLineChartData(usedData.chart_data, ['ricaScenarioId','Scenario',''],f'Alert Analysis',{None:'Scenario'},[] )
	chart2 = getChart3Data(usedData.chart_data,['ricaRiskAssessment',''],f'Risk Assessment')
	

def calculateDataForException(dataFilterData=[], alarm ={},flow_type='INFLOW'):
	notSelected = []
	scheme =  {  "Total Amount Involved": 0, "Alerts Freq": 0 , "Cases Freq": 0 , 'Expected':0,'Difference':0,
					**generateScheme(dataFilterData),"True Positive":0}
	todayData = { 'metric': "Today", **scheme,'Total': 0 }
	l2D_7D = { 'metric': "2 - 7 Days",**scheme,'Total': 0 }
	l8D_14D = { 'metric': "8 - 14 Days", **scheme,'Total': 0}
	l15D_28D = { 'metric': "15 - 28 Days", **scheme,'Total': 0 }
	l29D_3M = { 'metric': "29 Days - 3 Months", **scheme,'Total': 0 }
	l3M_6M = { 'metric': "Above 3 Months - 6 Months", **scheme,'Total': 0 }
	l6M_1Y = { 'metric': "Above 6 Months - 1 Year", **scheme,'Total': 0}
	l1Y_3Y = { 'metric': "Above 1 Year - 3 Years", **scheme,'Total': 0}
	l3Y_5Y = { 'metric': "Above 3 Years - 5 Years", **scheme, 'Total': 0}
	over_5Y = { 'metric': "Above 5 Years",**scheme,'Total': 0 }
	totalCustomer = { 'metric':'Total No. of Records',  **scheme,'Total': 0}

	for eachData in dataFilterData:
		totalCustomer = insertDataHelper(totalCustomer, eachData, notSelected)

		if isToday(str(eachData.get("ricaCreateDate"))):
			todayData = insertDataHelper(todayData, eachData, notSelected)
			eachData['RICADATETYPE'] = 'Today'

		if isWhatD(str(eachData.get("ricaCreateDate")),1,7):
			l2D_7D = insertDataHelper(l2D_7D, eachData, notSelected)
			eachData['RICADATETYPE'] = '2 - 7 Days'

		if isWhatD(str(eachData.get("ricaCreateDate")),8,14):
			l8D_14D = insertDataHelper(l8D_14D, eachData, notSelected)
			eachData['RICADATETYPE'] = '8 - 14 Days'

		if isWhatD(str(eachData.get("ricaCreateDate")),15,28):
			l15D_28D = insertDataHelper(l15D_28D, eachData, notSelected)
			eachData['RICADATETYPE'] = '15 - 28 Days'

		if isLastD_M(str(eachData.get("ricaCreateDate")),29,3):
			l29D_3M = insertDataHelper(l29D_3M, eachData, notSelected)
			eachData['RICADATETYPE'] = '29 Days - 3 Months'

		if isWhatM(str(eachData.get("ricaCreateDate")),3,6):
			l3M_6M = insertDataHelper(l3M_6M, eachData, notSelected)
			eachData['RICADATETYPE'] = 'Above 3 Months - 6 Months'

		if isWhatM(str(eachData.get("ricaCreateDate")),6,12):
			l6M_1Y = insertDataHelper(l6M_1Y, eachData, notSelected)
			eachData['RICADATETYPE'] = 'Above 6 Months - 1 Year'

		if isWhatM(str(eachData.get("ricaCreateDate")),12,12*3):
			l1Y_3Y = insertDataHelper(l1Y_3Y, eachData, notSelected)
			eachData['RICADATETYPE'] = 'Above 1 Year - 3 Years'

		if isWhatM(str(eachData.get("ricaCreateDate")),12*3,12*5):
			l3Y_5Y = insertDataHelper(l3Y_5Y, eachData, notSelected)
			eachData['RICADATETYPE'] = 'Above 3 Years - 5 Years'

		if isOver5Y(str(eachData.get("ricaCreateDate")),12*5):
			over_5Y = insertDataHelper(over_5Y, eachData, notSelected)
			eachData['RICADATETYPE'] = 'Above 5 Years'

	
	todayData['Expected'] =   alarm.get('ricaInFreqDay1',0) if flow_type=='INFLOW' else  alarm.get('ricaOutFreqDay1',0)
	todayData['Difference'] =  formatNumber(todayData['Expected']) - (formatNumber(todayData['Alerts Freq']) + formatNumber(todayData['Cases Freq']) ) 

	l2D_7D['Expected'] =	 alarm.get('ricaInFreq2To7Days',0) if flow_type=='INFLOW' else  alarm.get('ricaOutFreq2To7Days',0)
	l2D_7D['Difference'] =  formatNumber(l2D_7D['Expected']) - (formatNumber(l2D_7D['Alerts Freq']) + formatNumber(l2D_7D['Cases Freq']) ) 

	l8D_14D['Expected'] =	alarm.get('ricaInFreq8To14Days',0)  if flow_type=='INFLOW' else  alarm.get('ricaOutFreq8To14Days',0)
	l8D_14D['Difference'] =  formatNumber(l8D_14D['Expected']) - (formatNumber(l8D_14D['Alerts Freq']) + formatNumber(l8D_14D['Cases Freq']) ) 

	l15D_28D['Expected'] =	 alarm.get('ricaInFreq15To28Days',0) if flow_type=='INFLOW' else   alarm.get('ricaOutFreq15To28Days',0)
	l15D_28D['Difference'] =  formatNumber(l15D_28D['Expected']) - (formatNumber(l15D_28D['Alerts Freq']) + formatNumber(l15D_28D['Cases Freq']) ) 

	l29D_3M['Expected'] =	alarm.get('ricaInFreq29DaysTo3Months',0)  if flow_type=='INFLOW' else  alarm.get('ricaOutFreq29DaysTo3Months',0)
	l29D_3M['Difference'] =  formatNumber(l29D_3M['Expected']) - (formatNumber(l29D_3M['Alerts Freq']) + formatNumber(l29D_3M['Cases Freq']) ) 

	l3M_6M['Expected'] =   alarm.get('ricaInFreq3MonthsTo6Months',0) if flow_type=='INFLOW' else   alarm.get('ricaOutFreq3MonthsTo6Months',0)
	l3M_6M['Difference'] =  formatNumber(l3M_6M['Expected']) - (formatNumber(l3M_6M['Alerts Freq']) + formatNumber(l3M_6M['Cases Freq']) ) 

	l6M_1Y['Expected'] =	alarm.get('ricaInFreq6MonthsTo1Year',0) if flow_type=='INFLOW' else   alarm.get('ricaOutFreq6MonthsTo1Year',0)
	l6M_1Y['Difference'] =  formatNumber(l6M_1Y['Expected']) - (formatNumber(l6M_1Y['Alerts Freq']) + formatNumber(l6M_1Y['Cases Freq']) ) 

	l1Y_3Y['Expected'] =	 alarm.get('ricaInFreq1YearTo3Years',0)  if flow_type=='INFLOW' else  alarm.get('ricaOutFreq1YearTo3Years',0)
	l1Y_3Y['Difference'] =  formatNumber(l1Y_3Y['Expected']) - (formatNumber(l1Y_3Y['Alerts Freq']) + formatNumber(l1Y_3Y['Cases Freq']) ) 

	l3Y_5Y['Expected'] =	alarm.get('ricaInFreq3YearsTo5Years',0) if flow_type=='INFLOW' else   alarm.get('ricaOutFreq3YearsTo5Years',0)
	l3Y_5Y['Difference'] =  formatNumber(l3Y_5Y['Expected']) - (formatNumber(l3Y_5Y['Alerts Freq']) + formatNumber(l3Y_5Y['Cases Freq']) ) 

	over_5Y['Expected'] =	alarm.get('ricaInFreqOver5Years',0)  if flow_type=='INFLOW' else  alarm.get('ricaOutFreqOver5Years',0)
	over_5Y['Difference'] =  formatNumber(over_5Y['Expected']) - (formatNumber(over_5Y['Alerts Freq']) + formatNumber(over_5Y['Cases Freq']) ) 

	totalCustomer['Expected'] =  todayData['Expected'] + l2D_7D['Expected']+ l8D_14D['Expected']+l15D_28D['Expected'] +  l29D_3M['Expected']+ l3M_6M['Expected']+  l6M_1Y['Expected']+l1Y_3Y['Expected']+ l3Y_5Y['Expected'] +  over_5Y['Expected']
	totalCustomer['Difference'] =  formatNumber(totalCustomer['Expected']) - (formatNumber(totalCustomer['Alerts Freq']) + formatNumber(totalCustomer['Cases Freq']) ) 



	ret_data = {
	'columns':["metric",*[x for x in scheme] ],
	'data': [todayData, l2D_7D, l8D_14D,l15D_28D,l29D_3M,l3M_6M,l6M_1Y,l1Y_3Y,l3Y_5Y,over_5Y,totalCustomer],
	'chart_data':processExceptionBarChartMap([todayData, l2D_7D, l8D_14D,l15D_28D,l29D_3M]),
	'initial_data':dataFilterData,
	}


	return ret_data


def getDatelabel(key):
	return [
	 "Today",  
	  "2 - 7 Days", 
	 "8 - 14 Days",  
	 "15 - 28 Days",  
	 "29 Days - 3 Months", 
	 "Above 3 Months - 6 Months", 
	 "Above 6 Months - 1 Year",  
	 "Above 1 Year - 3 Years",  
	"Above 3 Years - 5 Years",  
	 "Above 5 Years"][key]



def processExceptionBarChartMap(mapData=[]):
	mapFilterData = []
	for key, eachData in enumerate(mapData):
		mapFilterData.append({**eachData,"exDif":"Actual","exDifValue":eachData['Alerts Freq'] + eachData['Cases Freq'],'RICADATETYPE':getDatelabel(key) })
		mapFilterData.append({**eachData,"exDif":"Expected","exDifValue":eachData['Expected'],'RICADATETYPE':getDatelabel(key)})

	return mapFilterData








def calculateDataForAlertDetails(dataFilterData=[],notSelected = []):

	schemeData =  { 'Description':"","Total Freq":0, "Total Amount Involved": 0,"True Disposition":0 
	 ,  "Total Alerts": 0 ,"Total Cases": 0 , **generateScheme(dataFilterData)
	}
	alert_analysis = {}

	for eachData in dataFilterData:
		objKey = eachData['ricaScenarioId']

		alert_analysis[objKey] = {  **schemeData, **alert_analysis.get(objKey,{}),
		'metric':objKey,
		'Description':eachData['ricaScenario'],
		"Total Freq":alert_analysis[objKey]["Total Freq"] + 1 if alert_analysis.get(objKey) else 1,
		"Total Amount Involved": alert_analysis[objKey]["Total Amount Involved"] + formatNumber(eachData.get('ricaNetLossAmount')) if alert_analysis.get(objKey)  else formatNumber(eachData.get('ricaNetLossAmount')),
		"True Disposition": alert_analysis[objKey]["True Disposition"] + formatNumber(1 if eachData.get('ricaDisposition') == 'True Positive'  else 0) if alert_analysis.get(objKey)  else formatNumber( 1 if eachData.get('ricaDisposition') == 'True Positive' else 0),
		"Total Alerts": alert_analysis[objKey]["Total Alerts"] + formatNumber(1 if eachData.get('ricaAlertId')  else 0) if alert_analysis.get(objKey)  else formatNumber( 1 if eachData.get('ricaAlertId')  else 0),
		"Total Cases": alert_analysis[objKey]["Total Cases"] + formatNumber(1 if eachData.get('ricaCaseId')  else 0) if alert_analysis.get(objKey)  else formatNumber(1 if eachData.get('ricaCaseId')  else  0),
		}

		riskKey = eachData["ricaRiskAssessment"]
		# print('===',alert_analysis[objKey] ,objKey,riskKey )

		if alert_analysis[objKey].get(riskKey):
			alert_analysis[objKey][riskKey] =  alert_analysis[objKey][riskKey] + 1
		else:
			alert_analysis[objKey][riskKey] =   1


		alert_analysis["Total"] = { 
		**schemeData, **alert_analysis.get("Total",{}),
		'metric':"Total",
		'Description':"",
		"Total Freq": alert_analysis["Total"]["Total Freq"] + 1 if alert_analysis.get('Total')  else 1,
		"Total Amount Involved": alert_analysis["Total"]["Total Amount Involved"] + formatNumber(eachData.get('ricaNetLossAmount')) if alert_analysis.get('Total')  else formatNumber(eachData.get('ricaNetLossAmount')),
		"True Disposition":  alert_analysis["Total"]["True Disposition"] + formatNumber( 1 if eachData.get('ricaDisposition') == 'True Positive'  else 0) if alert_analysis.get('Total')  else formatNumber( 1 if eachData.get('ricaDisposition') == 'True Positive'  else 0),
		"Total Alerts": alert_analysis["Total"]["Total Alerts"] + formatNumber( 1 if eachData.get('ricaAlertId')  else 0) if alert_analysis.get('Total')  else  formatNumber(1 if eachData.get('ricaAlertId')  else 0),
		"Total Cases":alert_analysis["Total"]["Total Cases"] + formatNumber(1 if eachData.get('ricaCaseId')  else 0) if alert_analysis.get('Total')  else   formatNumber( 1 if eachData.get('ricaCaseId')  else 0),

		}

		if alert_analysis['Total'].get(riskKey):
			alert_analysis['Total'][riskKey] =  alert_analysis['Total'][riskKey] + 1
		else:
			alert_analysis['Total'][riskKey] =   1





	returnData = [ alert_analysis[x] for x in alert_analysis]
	# print('returnData',returnData)


	ret_data = {
	'columns':["metric",*schemeData.keys()] ,
		'data':  returnData,
		 'chart_data':dataFilterData
	  
	}

	return ret_data

 


def getKeyTime(time):
	if (len(time) == 3):
		time = f'0${time}'
	time = time[0:2]
	timeInNumber = int(time)

	if (timeInNumber == 12):
		return f'{timeInNumber}PM'
	elif (timeInNumber > 12):
		return f'{timeInNumber - 12}PM'

	return f'{timeInNumber}AM'





def insertTimeSeriesDataHelper(todayData, eachData, notSelected,calc_field='amount'):
	todayData = { **todayData, 'Total': todayData['Total'] + (  1 if calc_field == 'frequency' else formatNumber(eachData.get('amount')) ) }
	todayData = { **todayData, getKeyTime(eachData["special_time"]): todayData[getKeyTime(eachData["special_time"])] + (  1 if calc_field == 'frequency' else formatNumber(eachData.get('amount')) ) }
	return todayData



def calculateDataForTimeSeries(dataFilterData=[],calc_field='amount'):
	notSelected = []
	scheme =  { '12AM': 0, '1AM': 0,'1AM': 0, '2AM': 0, '3AM': 0, '4AM': 0, '5AM': 0, '6AM': 0,
	'7AM': 0, '8AM': 0, '9AM': 0, '10AM': 0, '11AM': 0, '12PM': 0, '1PM': 0, '2PM': 0, '3PM': 0, '4PM': 0, '5PM': 0,
	'6PM': 0, '7PM': 0, '8PM': 0, '9PM': 0, '10PM': 0, '11PM': 0, }

	todayData = { 'metric': "Today", **scheme,'Total': 0 }
	l2D_7D = { 'metric': "2 - 7 Days",**scheme,'Total': 0 }
	l8D_14D = { 'metric': "8 - 14 Days", **scheme,'Total': 0}
	l15D_28D = { 'metric': "15 - 28 Days", **scheme,'Total': 0 }
	l29D_3M = { 'metric': "29 Days - 3 Months", **scheme,'Total': 0 }
	totalCustomer = { 'metric':'Total',  **scheme,'Total': 0}

	for eachData in dataFilterData: 

		if isToday(str(eachData.get("special_date"))):
			todayData = insertTimeSeriesDataHelper(todayData, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = 'Today'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatD(str(eachData.get("special_date")),1,7):
			l2D_7D = insertTimeSeriesDataHelper(l2D_7D, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = '2 - 7 Days'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatD(str(eachData.get("special_date")),8,14):
			l8D_14D = insertTimeSeriesDataHelper(l8D_14D, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = '8 - 14 Days'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatD(str(eachData.get("special_date")),15,28):
			l15D_28D = insertTimeSeriesDataHelper(l15D_28D, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = '15 - 28 Days'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isLastD_M(str(eachData.get("special_date")),29,3):
			l29D_3M = insertTimeSeriesDataHelper(l29D_3M, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = '29 Days - 3 Months'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatM(str(eachData.get("special_date")),3,6):
			l3M_6M = insertTimeSeriesDataHelper(l3M_6M, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = 'Above 3 Months - 6 Months'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatM(str(eachData.get("special_date")),6,12):
			l6M_1Y = insertTimeSeriesDataHelper(l6M_1Y, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = 'Above 6 Months - 1 Year'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatM(str(eachData.get("special_date")),12,12*3):
			l1Y_3Y = insertTimeSeriesDataHelper(l1Y_3Y, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = 'Above 1 Year - 3 Years'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isWhatM(str(eachData.get("special_date")),12*3,12*5):
			l3Y_5Y = insertTimeSeriesDataHelper(l3Y_5Y, eachData, notSelected,calc_field)
			eachData['RICADATETYPE'] = 'Above 3 Years - 5 Years'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

		if isOver5Y(str(eachData.get("special_date")),12*5):
			over_5Y = insertTimeSeriesDataHelper(over_5Y, eachData,notSelected, calc_field)
			eachData['RICADATETYPE'] = 'Above 5 Years'
			totalCustomer = insertTimeSeriesDataHelper(totalCustomer, eachData, notSelected,calc_field)

	ret_data = {
		'columns':["metric",*scheme.keys(),"Total"] ,
		'data': [todayData, l2D_7D, l8D_14D,l15D_28D,l29D_3M,totalCustomer],
		'chart_data':[todayData, l2D_7D, l8D_14D,l15D_28D,l29D_3M],
		'initial_data':dataFilterData,}




	return ret_data



 
def processTimeSeriesBarChartMap(mapData=[]):
	mapFilterData = []

	for key, eachData in enumerate(mapData):
		mapFilterData.append({**eachData,"exDif":"Actual","exDifValue":eachData['Alerts Freq'] + eachData['Cases Freq'],'RICADATETYPE':getDatelabel(key) })
		mapFilterData.push({**eachData,"exDif":"Expected","exDifValue":eachData['Expected'],'RICADATETYPE':getDatelabel(key)})

	return mapFilterData



		

month_list = ['January','February','March','April','May','June','July','August','September','October','November','December']

def getDay(val):
	return 'Day '+str(val).split('-')[2] if len(str(val).split('-')) > 2 else val

def getYear(val):
	return str(val).split('-')[0] if len(str(val).split('-')) > 0  else val

def getMonth(val):
	try:
		return month_list[String(val).split('-')[1]] if len(str(val).split('-')) > 1  else val
	except:
		return val


def getCurrentMonth():
	return month_list[datetime.datetime.now().month-1]



def reduce_check(acc,c,obj):
	acc[c] = obj[c]
	return acc

def sortObj(obj):
	data = list(obj.keys())
	data.sort()
	return functools.reduce(lambda acc,c:  reduce_check(acc,c,obj),data,{})




def getLineChartData(dataFilterData, key_columns=['ricaLinkZone','ricaRiskAssessment'],title="", map={},columns=[],type_='line',filename=None):
	# print(dataFilterData)
	key1=key_columns[0]
	key2=key_columns[1]

	try:
		key3=key_columns[2]
	except:
		key3 = ""


	resultObj = {}
	distinctType = {}
	count = 0


	for eachData in dataFilterData:
		key =  str(map.get(eachData.get(key2)) or eachData.get(key2)).upper()

		if (not distinctType.get(key)):
			distinctType[key] = count
			count += 1

	for eachData in dataFilterData:
		key = getDay(eachData.get(key1))
		# print('key',key,count,eachData)
		if not resultObj.get(key):
			resultObj[key] = []		  
			for i in range(count):
				resultObj[key].append(0)
			# print('key',key,count,resultObj[key])

		resultObj = sortObj(resultObj)

		index = distinctType[str( map.get(eachData.get(key2)) or eachData.get(key2)).upper()]
		resultObj[key][index] +=  formatNumber(eachData[key3]) if key3 else 1


	datasetArray = []
	finalDataSet = {}
	labels = columns if columns else []
	for i in range(count):
		datasetArray.append([]) 

	# print('gggg-test',datasetArray)

	if columns:
		for eachKey in labels:
			# print('gggg',eachKey,datasetArray,'====',resultObj)
			if resultObj.get(eachKey):
				arrayData = resultObj[eachKey]
				for i in range(len(arrayData)):
					datasetArray[i].append(arrayData[i])
			else:
				# for i in range(len(distinctType.keys())):
				for i in range(count):
					datasetArray[i].append(0)

	else:
		for eachKey in resultObj:
			labels.append(eachKey)
			arrayData = resultObj.get(eachKey)
			for i in range(len(arrayData)):
				datasetArray[i].append(arrayData[i])

	for eachData in datasetArray:
		label = ''
		for eachKey in distinctType:
			keyIndex = distinctType[eachKey]
			if keyIndex == index:
				label = eachKey

		# bgColor = createDynamicColors()
		finalDataSet[label]=eachData



	data =  {  'labels': labels,**finalDataSet	}
	

	# print(data)
	return create_line_chart(data,"labels",title) if type_=='line' else create_bar_chart(data,"labels",title,filename)



def getTimeSeriesData(data=[],flow_type='C',timeSeriesType='amount'):
	return calculateDataForTimeSeries(list(filter(lambda e:e["trans_code"]==flow_type,data)),timeSeriesType)


def getDataForTimeSeriesChart(dataFilterData=[], calc_field='amount'):
	notSelected = []
	accepted_dates = ['Today','2 - 7 Days','8 - 14 Days','15 - 28 Days','29 Days - 3 Months']

	dataFilterData = list(filter(lambda e:e["RICADATETYPE"] in accepted_dates,dataFilterData))

	objData = {}
	sampleObj = {
	  'branch': '', 'date': '', 'teller': '', '12AM': 0, '1AM': 0, '2AM': 0, '3AM': 0, '4AM': 0, '5AM': 0, '6AM': 0,
	  '7AM': 0, '8AM': 0, '9AM': 0, '10AM': 0, '11AM': 0, '12PM': 0, '1PM': 0, '2PM': 0, '3PM': 0, '4PM': 0, '5PM': 0,
	  '6PM': 0, '7PM': 0, '8PM': 0, '9PM': 0, '10PM': 0, '11PM': 0
	}

	for eachData in dataFilterData:
		key = eachData["RICADATETYPE"]

		if not objData.get(key):
			objData[key] = { **sampleObj }

		objData[key]["date"] = eachData["RICADATETYPE"]

		objData[key][getKeyTime(eachData["special_time"])] += (int(eachData["amount"]) if calc_field == 'amount' else 1)


	objData = list(map(lambda eachData:objData[eachData],objData.keys()))

	labels = ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM']

	ret_val = {
	  'DATE TYPE': labels,

	}

	for key,x in enumerate(objData):
		ret_val = {**ret_val, **generateTimeSeriesMap(key,objData,labels)}

	# print(ret_val)

	return ret_val


 
def generateTimeSeriesMap(eachData,objData,labels):
	dataVal = objData[eachData]		
	return {
	  dataVal["date"]:[ dataVal[eachLab] for eachLab in labels ]
	  }




def generateAnalytics(analysis_data,execute=lambda x:x,account_no="",branchid="All",scenario="All"):


	# print('analysis========>',analysis_data,'\n\n')

	if not analysis_data:
		pass

	analytics_result = []
	excel_file = ""

	if len(analysis_data):
		sheet1 = genInflowOutflowAnalytics(analysis_data)
		analytics_result.append(sheet1)

		sheet2 = renderGridAmountChart(sheet1)
		analytics_result.append(sheet2)
		
		sheet3 = renderGridFreqChart(sheet1)
		analytics_result.append(sheet3)


		alarm = getAlarm(execute) or {}
		print('here===1')
		gridExceptionData = getExceptionsData(execute,account_no,branchid)
		exceptionData = calculateDataForException(list(filter(lambda e:e["ricaFlowType"]=='INFLOW',gridExceptionData)),alarm,'INFLOW')
		sheet4 = (exceptionData, *renderExceptionFreqChart("Inflow",exceptionData))
		analytics_result.append(sheet4)

		outflowExceptionData = calculateDataForException(list(filter(lambda e:e["ricaFlowType"]=='OUTFLOW',gridExceptionData)),alarm,'OUTFLOW')
		sheet5 = (outflowExceptionData, *renderExceptionFreqChart("Outflow",outflowExceptionData))
		analytics_result.append(sheet5)

		# amount inflow Timeseries
		inflow_timeseries_amount = getTimeSeriesData(analysis_data,'C','amount' )
		inflow_timeseries_amount_chart =getDataForTimeSeriesChart(list(filter(lambda e:e["trans_code"]=='C',analysis_data)),'amount' )
		sheet6 = (inflow_timeseries_amount,create_line_chart(inflow_timeseries_amount_chart,"DATE TYPE",title="3 - Month Inflow Time Series (Amount.)") )
		analytics_result.append(sheet6)

		# amount outflow Timeseries
		inflow_timeseries_amount = getTimeSeriesData(analysis_data,'D','amount' )
		inflow_timeseries_amount_chart =getDataForTimeSeriesChart(list(filter(lambda e:e["trans_code"]=='D',analysis_data)),'amount' )
		sheet7 = (inflow_timeseries_amount,create_line_chart(inflow_timeseries_amount_chart,"DATE TYPE",title="3 - Month Outflow Time Series (Amount.)") )
		analytics_result.append(sheet7)
		
		 # frequency inflow Timeseries
		inflow_timeseries_frequency = getTimeSeriesData(analysis_data,'C','frequency' )
		inflow_timeseries_frequency_chart =getDataForTimeSeriesChart(list(filter(lambda e:e["trans_code"]=='C',analysis_data)),'frequency' )
		sheet8 = (inflow_timeseries_frequency,create_line_chart(inflow_timeseries_frequency_chart,"DATE TYPE",title="3 - Month Inflow Time Series (Freq.)") )
		analytics_result.append(sheet8)

		# frequency outflow Timeseries
		inflow_timeseries_frequency = getTimeSeriesData(analysis_data,'D','frequency' )
		inflow_timeseries_frequency_chart =getDataForTimeSeriesChart(list(filter(lambda e:e["trans_code"]=='D',analysis_data)),'frequency' )
		sheet9 = (inflow_timeseries_frequency,create_line_chart(inflow_timeseries_frequency_chart,"DATE TYPE",title="3 - Month Outflow Time Series (Freq.)") )
		analytics_result.append(sheet9)

		alertDetailsData = calculateDataForAlertDetails(gridExceptionData)
		alert1A  = getLineChartData(alertDetailsData["chart_data"], ['ricaScenarioId','ricaScenario',''],f'Alerts & Cases Analysis',type_='bar',map={'None':'Scenario'} )
		alert1B = getChart3Data(alertDetailsData["chart_data"],['ricaRiskAssessment',''],f'Alerts & Cases Risk Assessment')
		sheet10 = (alertDetailsData,alert1A,alert1B)
		analytics_result.append(sheet10)

		print("account_no:",account_no,len(analysis_data))
	# print("Analysis Result",analytics_result)

	print("analytics_result")
	excel_file = create_excel(
		scenario,branchid,account_no,
		sheet1=analytics_result[0],
		sheet2=analytics_result[1],
		sheet3=analytics_result[2],
		sheet4=analytics_result[3],
		sheet5=analytics_result[4],
		sheet6=analytics_result[5],
		sheet7=analytics_result[6],
		sheet8=analytics_result[7],
		sheet9=analytics_result[8],
		sheet10=analytics_result[9],
		pretiffy=True)
	print("excel_file=>",excel_file)

	return excel_file		

		

