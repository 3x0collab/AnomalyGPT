
GET_SCENARIO="""
        select ricaRuleId,
    ricaRule,
    ricaTypeId,
    ricaSubTypeId,
    ricaRequestor,
    ricaPurpose,
    ricaIntervalOf,
    ricaRunMode,
    ricaWeekly,
    ricaMonthly,
    ricaQuarterly,
    ricaYearly,
    ricaLastRunDate,
    ricaLastRunTime,
    ricaNextRunDate,
    ricaNextRunTime,
    ricaImplications,
    ricaGroupBy,
    ricaRespondent,
    ricaInvestigator,
    ricaOwner,
    ricaNextOwner,
    ricaEnforcer,
    ricaModality,
    ricaTotalPerBatch,
    ricaSuggestedRisk,
    ricaLikelihood,
    ricaConsequence,
    ricaPriority,
    ricaDescription,
    ricaNotifyBeforeDue,
 
    ricaRespondentOverdueTime,
    ricaInvestigatorOverdueTime,
    ricaOwnerOverdueTime,
    ricaRespondentOverdueRepeat,
    ricaInvestigatorOverdueRepeat,
    ricaOwnerOverdueRepeat, 
    
    ricaOverdueRiskMatrix,
    ricaOverduePriority,
    ricaAutoClose,
    ricaAutoStatus,
    ricaCloseAfter,
    ricaCloseRisk,
    ricaCreateAlert,
    ricaRunStatus,
    ricaStatusReason,
    ricaStatusDate,
    ricaStatusTime,
     ricaQueryPanel,
     ricaMapper,
    ricaStatusInitiator from rica_prompt_builders
        Where ricaRuleId = '{scenario}'
        """

GET_BRANCH_1 =""" 
        select DISTINCT RICABRANCHCODE,RICABRANCHNAME from rica_journalentries 
               where CONCAT(RICASPECIALDATE,RICASPECIALTIME) >= '{v_lastrundate}{v_lastruntime}' 
            """

GET_BRANCH_1KEYSTONE =""" 
SELECT DISTINCT 
(CASE WHEN (SELECT RICACOMPANYCODE FROM RICA.RICA_T24_USER WHERE RICARECORDID = A.RICAINPUTTER) IN ('NG0010001', 'ALL') 
THEN (SELECT DISTINCT TO_CHAR(H.RICADEPTCODE) FROM RICA.RICA_T24HEAD_OFFICE_USERS H WHERE TO_CHAR(H.RICAPHBUSERGROUP) IN (SELECT DISTINCT TO_CHAR(U.RICAPHBUSERGROUP) FROM RICA.RICA_T24_USER U WHERE U.RICARECORDID = A.RICAINPUTTER)) 
ELSE TO_CHAR(A.RICABRANCHCODE) END) AS RICABRANCHCODE,

(select ricaBranchName from RICA.rica_branch where TO_CHAR(ricaBranchId) = (CASE WHEN (SELECT RICACOMPANYCODE FROM RICA.RICA_T24_USER WHERE RICARECORDID = A.RICAINPUTTER) IN ('NG0010001', 'ALL') 
THEN (SELECT DISTINCT TO_CHAR(H.RICADEPTCODE) FROM RICA.RICA_T24HEAD_OFFICE_USERS H WHERE TO_CHAR(H.RICAPHBUSERGROUP) IN (SELECT DISTINCT TO_CHAR(U.RICAPHBUSERGROUP) FROM RICA.RICA_T24_USER U WHERE U.RICARECORDID = A.RICAINPUTTER)) 
ELSE TO_CHAR(A.RICABRANCHCODE) END) ) AS RICABRANCHNAME 
FROM rica_journalentries A
               WHERE CONCAT(A.RICASPECIALDATE,A.RICASPECIALTIME) >= '{v_lastrundate}{v_lastruntime}' 
            """

GET_BRANCH_2 = """ 
            select DISTINCT RICA{group_field.upper()} as {group_field} from rica_journalentries 
              WHERE CONCAT(A.RICASPECIALDATE,A.RICASPECIALTIME) >= '{v_lastrundate}{v_lastruntime}' 
        """




GET_DIS_ACCOUNT_1 =""" 
           select DISTINCT RICAACCOUNTID from rica_journalentries 
               where CONCAT(RICASPECIALDATE,RICASPECIALTIME) >= '{v_lastrundate}{v_lastruntime}' 
            """

