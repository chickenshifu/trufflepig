#!/usr/bin/python3
'''THIS FILE IS FOR EXECUTION ONLY. 
COMBINES ALL SUBROUTINES FROM SCRIPTS IN MAIN FOLDER'''

import parser
import databaseHandling
import calculator
import mailHandler
import variables
import time
import traceback

try:

    start = time.time()
    print("Starting online job...")

    '''Refresh database with raw data, this job lasts for at least 4-5 hours and shall run once per day'''
    parser.parseCryptoUrls()
    parser.parseData()
    
    print("Online job done!")
    
    print("Starting offline jobs...")
    
    calculator.calculateStats()
    results = calculator.calculateOutliers()
    
    print("Offline jobs done!")
    
    print("Sending mail...")
    mailHandler.sendMail("Success", results)
    print("Mail successfully sent!")
    end = time.time()
    elapsed_time = (end-start)/60
    print(f'Jobs finished! (Total time elapsed (mins): {elapsed_time}')
    
except Exception as e:

    print(f'ERROR: {e}')
    e = str(e)
    full_traceback=str(traceback.format_exc())
    print(full_traceback)
    e_tuple = ([e], [full_traceback])
    mailHandler.sendMail("ERROR", e_tuple)

