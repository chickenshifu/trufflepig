#!/usr/bin/python3
'''THIS FILE IS FOR EXECUTION ONLY. 
COMBINES ALL SUBROUTINES FROM SCRIPTS IN MAIN FOLDER'''

import parser
import databaseHandling
import calculator
import mailHandler
import variables

try:

    print("Starting online job...")


    '''Refresh database with raw data, this job lasts for at least 4-5 hours and shall run once per day'''
    parser.parseCryptoUrls()
    parser.parseWatchlistEntry()
    
    print("Online job done!")
    
    print("Starting offline jobs...")
    
    calculator.calculateMeanAndDeviation()
    resultTuple = calculator.calculateOutliers()
    
    print("Offline jobs done!")
    
    print("Sending mail...")
    recipient = variables.mailhandler_recipient
    mailHandler.sendMail(recipient, "Success", resultTuple)
    print("Mail successfully sent!")
    
    
    print("Jobs finished!")
    
    
except Exception as e:

    print(f'ERROR: {e}')
