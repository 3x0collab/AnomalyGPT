UPDATE_QUERY = """ 
                     UPDATE rica_rule_builders
                SET ricaLastRunDate = CONVERT(date, '{ricaLastRunDate}', 23),  
                ricaLastRunTime = CONVERT(time, '{ricaLastRunTime}', 114)
                WHERE ricaRuleId = '{ricaRuleId}'
     """

UPDATE_QUERY_NEXTRUNDATE = """ 
                     UPDATE rica_rule_builders
                SET ricaNextRunDate = CONVERT(date, '{ricaNextRunDate}', 23),  
                ricaNextRunTime = CONVERT(time, '{ricaNextRunTime}', 114)
                WHERE ricaRuleId = '{ricaRuleId}'
     """


UPDATE_ALERTSCONCAT = """  INSERT INTO rica_alertsconcat (    
                    ricaConcatId,
                       ricaAlertId,
                       ricaScenarioId,
                       ricaTransRef,
                       ricaCustomerNo,
                       ricaAccountNo,
                       ricaBranchId,
                       ricaDisposition,
                       ricaRiskAssessment, 
                       ricaAmountInvolved, 
                       ricaAvertedAmount, 
                       ricaRecoverAmount, 
                       ricaNetLossAmount, 
                       ricaAlertDate, 
                       ricaAlertTime
                    )       

                        VALUES (
                       '{journalId}',
            '{exceptionId}',
            '{ricaScenarioId}',
            '{ricaEntityId}',
            '{ricaCustomerNo}',
            '{ricaAccountNo}',
            '{branchId}',
            '{ricaNewDisposition}',
            '{ricaRiskAssessment}',
            {ricaAmount},
            {ricaAvertedAmount},
            {ricaRecoverAmount},
            {ricaNetLossAmount},
                        CONVERT(date, '{ricaCreateDate}',23),
                        CONVERT(time, '{ricaCreateTime}',114)
                 )
"""



UPDATE_ALERTQUERY = """ 
            INSERT INTO rica_alerts (    
                    ricaAlertId,
               ricaBatchId,
               ricaTypeId,
               ricaSubTypeId,
               ricaScenarioId,
               ricaScenario,
               ricaEntityId,
               ricaEntityName,
               ricaHighlights,
               ricaAlertStatus,
               ricaFlowType,                      
               ricaAssignee,
               ricaAssignor,
               ricaRiskAssessment,
               ricaSuggestedRisk,
               ricaPriority,
               ricaBranchId,
               ricaBranchName,
               ricaCluster,
               ricaZone,
               ricaRegion,                   
               ricaRespondent,
               ricaRespondentDesignate,
               ricaInvestigator,
               ricaInvestigatorDesignate,
               ricaOwner,
               ricaOwnerDesignate,
               ricaNextOwner,
               ricaNextOwnerDesignate,
               ricaEnforcer,                    
               ricaLikelihood,
               ricaConsequence,
               ricaCreatedBy,
               ricaCreateDate,
               ricaCreateTime,
               ricaDueDate,
               ricaLastActivity,
               ricaLastActivist,
               ricaLastActivityDate,
               radporLastActivityTime,                    
               ricaCustomerNo,
               ricaAccountNo,
               ricaAccountName,
               ricaTransId,                      
               ricaStandardComment,
               ricaAlertComment,                    
               ricaRecoveryDate,
               ricaCurrency,
               ricaAmount,
               ricaTotalAmountInvolved,
               ricaAvertedAmount,
               ricaRecoverAmount,
               ricaNetLossAmount,
               ricaRecoveryComment,
               ricaLastRunDate,
               ricaLastRunTime,
               ricaNextRunDate,                      
               ricaNextRunTime,
               ricaOldRespondent,
               ricaNewRespondent,
               ricaOldInvestigator,
               ricaNewInvestigator,
               ricaOldOwner,
               ricaNewOwner,
               ricaOldNextOwner,
               ricaNewNextOwner,
               ricaNewAssignee,
               ricaNoAttachment,
               ricaRiskScoring,
               ricaReturnStatus,
               ricaReturnTo,
               ricaValidateOverride,
               ricaAutoCaseCreate,
               ricaRegReportFlag,
               ricaReportWithinDate,
               ricaReportWithinTime,
               ricaRegReportDate,
               ricaRegReportTime,
               ricaRegReportStatus,                      
               ricaNotifyBeforeDue,
               ricaRespondentOverdueTime,
               ricaInvestigatorOverdueTime,
               ricaOwnerOverdueTime,
               ricaRespondentOverdueRepeat,
               ricaInvestigatorOverdueRepeat,
               ricaOwnerOverdueRepeat, 
               ricaOverdueRiskMatrix,
               ricaOverduePriority,
               ricaExpectedRemindTime,
               ricaRemindCounter,
               ricaRemindNextDate,
               ricaRemindNextTime,
               ricaOverdueCounter,
               ricaAutoClose,
               ricaAutoStatus,
               ricaCloseAfter,
               ricaCloseRisk  ,
               ricaNewAlertStatus ,
               ricaStatusReason,
               ricaNewAssigneeRole  ,
               ricaNewAssigneeName,
               ricaReassignRole,
               ricaReassignCriteria,
               ricaReassignee,
               ricaFindings,
               ricaActions,
               ricaGeneralComment,
               ricaDecision,
               ricaNewDisposition,
               ricaDecisionReason,
               ricaFinalRiskMatrix,
               ricaFinalLikelihood,
               ricaFinalConsequence,
               ricaFinalPriority,
               ricaOverrideDate,
               ricaOverrideTime,
               ricaTransDate,
               ricaTransTime,
               ricaDueTime,
               ricaInputter,
                ricaAuthoriser,
                ricaAccountOfficer,
                ricaVerifier
                    )         

                        VALUES (
                        '{exceptionId}',
                '{ricaBatchId}',
                '{ricaTypeId}',
                '{ricaSubTypeId}',
                '{ricaScenarioId}',
                '{ricaScenario}',
                '{ricaEntityId}',
                '{ricaEntityName}',
                '{ricaHighlights}',
                '{ricaAlertStatus}',
                '{ricaFlowType}',
                '{ricaAssignee}',
                '{ricaAssignor}',
                '{ricaRiskAssessment}',
                '{ricaSuggestedRisk}',
                {ricaPriority},
                '{ricaBranchId}',
                '{branch_name}',
                '{ricaCluster}',
                '{ricaZone}',
                '{ricaRegion}',                  
                '{ricaRespondent}',
                '{ricaRespondentDesignate}',
                '{ricaInvestigator}',
                '{ricaInvestigatorDesignate}',
                '{ricaOwner}',
                '{ricaOwnerDesignate}',
                '{ricaNextOwner}',
                '{ricaNextOwnerDesignate}',
                '{ricaEnforcer}',                   
                '{ricaLikelihood}',
                '{ricaConsequence}',
                '{ricaCreatedBy}',
                        CONVERT(date, '{ricaCreateDate}',23),
                        CONVERT(time, '{ricaCreateTime}',114),
                        CONVERT(date, '{ricaDueDate}',23),
                        '{ricaLastActivity}',
                        '{ricaLastActivist}',
                        CONVERT(date, '{ricaLastActivityDate}',23),
                        CONVERT(time, '{radporLastActivityTime}',114),
                        '{ricaCustomerNo}',
                        '{ricaAccountNo}',
                        '{ricaAccountName}',
                        '{ricaTransId}',                     
                        '{ricaStandardComment}',
                        '{ricaAlertComment}',                   
                        CONVERT(date, '{ricaRecoveryDate}',23),
                       '{ricaCurrency}',
                {ricaAmount},
                {ricaTotalAmountInvolved},
                {ricaAvertedAmount},
                {ricaRecoverAmount},
                {ricaNetLossAmount},
                '{ricaRecoveryComment}',
                        CONVERT(date, '{ricaLastRunDate}',23),
                        CONVERT(time, '{ricaLastRunTime}',114),
                        CONVERT(date, '{ricaNextRunDate}',23),
                        CONVERT(time, '{ricaNextRunTime}',114),
                        '{ricaOldRespondent}',
                '{ricaNewRespondent}',
                '{ricaOldInvestigator}',
                '{ricaNewInvestigator}',
                '{ricaOldOwner}',
                '{ricaNewOwner}',
                '{ricaOldNextOwner}',
                '{ricaNewNextOwner}',
                '{ricaNewAssignee}',
                {ricaNoAttachment},
                '{ricaRiskScoring}',
                '{ricaReturnStatus}',
                '{ricaReturnTo}',
                '{ricaValidateOverride}',
                '{ricaAutoCaseCreate}',
                '{ricaRegReportFlag}',
                        CONVERT(date, '{ricaReportWithinDate}',23),
                        CONVERT(time, '{ricaReportWithinTime}',114),
                        CONVERT(date, '{ricaRegReportDate}',23),
                        CONVERT(time, '{ricaRegReportTime}',114),
                         '{ricaRegReportStatus}',                     
                {ricaNotifyBeforeDue}, 
                {ricaRespondentOverdueTime},
                {ricaInvestigatorOverdueTime},
                {ricaOwnerOverdueTime},
                {ricaRespondentOverdueRepeat},
                {ricaInvestigatorOverdueRepeat},
                {ricaOwnerOverdueRepeat},
                '{ricaOverdueRiskMatrix}',
                {ricaOverduePriority},
                        CONVERT(time, '{ricaExpectedRemindTime}',114),
                        {ricaRemindCounter},
                        CONVERT(date, '{ricaRemindNextDate}',23),
                        CONVERT(time, '{ricaRemindNextTime}',114),
                         {ricaOverdueCounter},
                '{ricaAutoClose}',
                '{ricaAutoStatus}',
                '{ricaCloseAfter}',
                '{ricaCloseRisk}',
                '{ricaNewAlertStatus}',
                '{ricaStatusReason}',
                '{ricaNewAssigneeRole}',
                '{ricaNewAssigneeName}',
                '{ricaReassignRole}',
                '{ricaReassignCriteria}',
                '{ricaReassignee}',
                '{ricaFindings}',
                '{ricaActions}',
                '{ricaGeneralComment}',
                '{ricaDecision}',
                '{ricaNewDisposition}',
                '{ricaDecisionReason}',
                '{ricaFinalRiskMatrix}',
                '{ricaFinalLikelihood}',
                '{ricaFinalConsequence}',
                {ricaFinalPriority},
                        CONVERT(date, '{ricaOverrideDate}',23),
                        CONVERT(time, '{ricaOverrideTime}',114),
                        CONVERT(date, '{ricaTransDate}',23),
                        CONVERT(time, '{ricaTransTime}',114),
                        CONVERT(time, '{ricaDueTime}',114),
                          '{ricaInputter}',
                '{ricaAuthoriser}',
                '{ricaAccountOfficer}',
                '{ricaVerifier}'
                 )
                 """


UPDATE_EXCEPTION_OUTPUT = """ 
 INSERT INTO ricaExceptionOutput (  
            ricaExceptionId,
            ricaScenarioId,
            ricaExceptionDescription,
            ricaBranchId,
            ricaExceptionIndicator,
             ricaRespondent,
                   ricaRespondentDesignate,
                   ricaInvestigator,
                   ricaInvestigatorDesignate,
                   ricaOwner,
                   ricaOwnerDesignate,
                   ricaNextOwner,
                   ricaNextOwnerDesignate,
                   ricaEnforcer,    
            ricaOtherReceivers,
               ricaExceptionResult,
               ricaExceptionRunTime,
               ricaExceptionRunDate

               )
               VALUES (
                '{exceptionId}',
                '{ricaScenarioId}',
                '{ricaExceptionDescription}',
                '{ricaBranchs}',
                '{ricaExceptionIndicator}',
                '{ricaRespondent}',
                    '{ricaRespondentDesignate}',
                    '{ricaInvestigator}',
                    '{ricaInvestigatorDesignate}',
                    '{ricaOwner}',
                    '{ricaOwnerDesignate}',
                    '{ricaNextOwner}',
                    '{ricaNextOwnerDesignate}',
                    '{ricaEnforcer}',              
                '{ricaOtherReceivers}',
              :exceptionResult,
            CONVERT(time, '{ricaExceptionRunTime}',114),
                CONVERT(date, '{ricaExceptionRunDate}',23)

                  )
        """

GET_SPF=""" select ricaClientName,ricaStmpMailServer,ricaStmpMailPort,ricaStmpMailUser,ricaStmpMailPassword,
     ricaDefaultOwner,ricaDefaultRespondent,ricaDefaultInvestigator,ricaLicenseCode,ricaLicenseNotifyDur,
       CONVERT(varchar(10), ricaExpiryDate, 120) AS ricaExpiryDate 
     from rica_spf 
     where ricaSpfId='{lang}-SYSTEM' """

GET_ACCT_TRANSACTIONS = """
SELECT DISTINCT TOP 10
    RICATRANSID AS Transaction_ID,
    ricatranstype AS Transaction_Type,
    RICABRANCHCODE AS Transaction_Branch,  
    CAST(RICANARRATIVE AS VARCHAR(400)) AS Transaction_Narrative, 
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
WHERE CONVERT(DATETIME, RICASPECIALDATE + ' ' + RICASPECIALTIME, 112) >= '{v_lastrundate}{v_lastruntime}'  
    AND RICAACCOUNTID = '{account}' 
ORDER BY Transaction_Date DESC, Transaction_Time DESC;

"""