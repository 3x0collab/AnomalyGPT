




in exceptions, write a routine that get group first, if it's not available, then pick respondent
workon alert management to select group and respondent
Create reserve field words

add branch name to header
remove chart
expand details/narrative
add alert links to email: http://localhost:3000/#/Alerts_Management?=alert_id&&refer=true
modify exceptions to use filename as id






scenarios
control rule
callover



where A.RICASPECIALDATE  >= '{v_lastrundate}'
and A.RICASPECIALTIME > '{v_lastruntime}'  
and A.RICABRANCHCODE =  '{branch_code}'  


RESERVE FIELD WORDS:
special_date -  RICASPECIALDATE
special_time - RICASPECIALTIME
branch - RICABRANCHCODE
amount - RICALCYAMOUNT
account - RICAACCOUNTID
trans_type - RICATRANSTYPE
trans_id - RICATRANSID
ref_id - RICATRANSREFID
trans_code - RICATRANSCODE
customer_no - RICACUSTOMERNO
details - RICANARRATIVE
account_officer - RICAACCOUNTOFFICER
entry_date - RICAENTRYDATE
entry_date - RICAENTRYDATE


http://127.0.0.1:3000/#login?refer=true&link=Alerts_Management&args=SC0001-000-20230310-14280837-000MBFT223040091

handleForm({target: "Review" })


====> in the query panel, validate if the query return reserved fields
====> provide an arrangeable list that contains all output fields by the query, which  can be selected or unselected and re-arrange