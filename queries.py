
def JOURNAL_VIA_ACCOUNT(account_id):
	return f"""
		             select RICATRANSID,RICABRANCHCODE,RICALCYAMOUNT, RICABRANCHNAME,
		             account_name,
		 dbms_lob.substr(details, 10000, 1) details,
		    to_char(RICAENTRYDATE,'YYYY-MM-DD') AS RICAENTRYDATE,
		    to_char(RICAPOSTINGDATE,'YYYY-MM-DD') AS RICAPOSTINGDATE,
		    to_char(RICAVALUEDATE,'YYYY-MM-DD') AS RICAVALUEDATE,
		to_char(RICAENTRYTIME,'HH:MI:SS') AS RICAENTRYTIME, 
		RICAINPUTTER,RICALCYAMOUNT,RICALCYCODE,
		RICATRANSCODE,RICATRANSTYPE
		from rica_journalentries
		where RICAACCOUNTID='{account_id}'

                            """