#!/usr/bin/python3
'''THIS FILE IS FOR EXECUTION ONLY. 
COMBINES ALL SUBROUTINES FROM SCRIPTS IN MAIN FOLDER'''

import parser
import databaseHandling
import calculator
import mailHandler
import variables
import time

try:

    start = time.time()
    print("Starting online job...")

    '''Refresh database with raw data, this job lasts for at least 4-5 hours and shall run once per day'''
    parser.parseCryptoUrls()
    parser.parseData()
    
    print("Online job done!")
    
    print("Starting offline jobs...")
    
    resultTuple = calculator.calculateStats()
    
    print("Offline jobs done!")
    
    print("Sending mail...")
    mailHandler.sendMail("Success", resultTuple)
    print("Mail successfully sent!")
    end = time.time()
    elapsed_time = end-start
    print(f'Jobs finished! (Total time elapsed: {elapsed_time}')
    
except Exception as e:

    print(f'ERROR: {e}')
