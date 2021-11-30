#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
import databaseHandling
import re

url = 'https://coinmarketcap.com'
url_suffix = '/?page='

headers = headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12.0; rv:93.0) Gecko/20100101 Firefox/93.0'

    }

################
#SELENIUM CONFIG
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

'''LOCAL'''
#binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox-bin')
#executablePath = '/usr/local/Cellar/geckodriver/0.28.0/bin/geckodriver'

'''RASPBERRY PI'''
binary = FirefoxBinary('/usr/bin/firefox')
executablePath = '/usr/bin/geckodriver'

options = Options()
options.headless = True 
driver = webdriver.Firefox(executable_path=executablePath, firefox_binary=binary, options=options)
actions = ActionChains(driver)

initMsg = f"Initialized Browser (Geckodriver-Path: {executablePath})"
print(initMsg)


################

################################
#DEFINITION OF HTML ELEMENTS####
cmc_crypto_url = 'sc-16r8icm-0 escjiH'
###############################



def parseCryptoUrls():

    #CREATE DATABASE + TABLES####!
    databaseHandling.createCryptoURLTable()
    
    print(f"Starting to collect all Cryptocurrency URLs from {url} ...")
    
    req = requests.get(url)
    '''Loop breaks, if other than 200 HTTP response OR maximum pages parsed'''
    i = 1 
    while not (i>4): #5 Pages == 500 cryptos
    
        print(f'Parsing page: {i}')
        url_full = url + url_suffix + str(i)
        
        driver.get(url_full)
    
        time.sleep(1 + random.randrange(0,4))
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        driver.execute_script("scrollBy(0,-2000);")
        driver.execute_script("scrollBy(0,+4000);")
        time.sleep(0.5)
        driver.execute_script("scrollBy(0,-2000);")
        driver.execute_script("scrollBy(0,+4000);")
        time.sleep(0.5)
        driver.execute_script("scrollBy(0,-2000);")
        driver.execute_script("scrollBy(0,+4000);")
        time.sleep(0.5)
        driver.execute_script("scrollBy(0,-2000);")
        driver.execute_script("scrollBy(0,+4000);")
    
    
        time.sleep(3)
        html_source = driver.page_source
        i += 1
        time.sleep(1 + random.randrange(0,2))
    
    
        ########START OF COLLECTING SINGLE URLS#######
        soup = BeautifulSoup(html_source, 'html.parser')
        crypto_rows = soup.find_all('div', {'class': 'sc-16r8icm-0 escjiH'})
    
        for row in crypto_rows:
            crypto_url = row.find_all('a', {'class': 'cmc-link'})
    
            for target_url in crypto_url:
                final_url=target_url['href']
                
                ########WRITE TO DATABASE#####
                databaseHandling.appendTableWithUrls(final_url) 
    
        req = requests.get(url_full)

        if req.status_code != 200 or i>1:
            print(f"Stopped parsing from {url}. Last page parsed: {i}.")
     
def parseData():
      ########OPEN EACH URL AND SCAN 'WATCHLIST' ENTRY####
      print("Lese aus DB...")
      urls = databaseHandling.readUrls()
      a = len(urls)

      for i in range(0,a-1):
          name_for_selenium = str(urls.loc[i, "url"])
          name_for_database = f'[{urls.loc[i, "url"]}]'
          databaseHandling.createSingleCryptoTable(name_for_database)
      
          target_url = url + name_for_selenium
          print(f'Open {target_url}')
          
          ######SELENIUM ACTION#####
          driver.get(target_url)
          html_source = driver.page_source
          time.sleep(1+random.randrange(0,2))
          soup = BeautifulSoup(html_source, 'html.parser')
          watchlist_entry = soup.select('div.namePill:nth-child(3)')
          current_price = soup.select('.priceValue > span:nth-child(1)')[0].get_text()

          ####FORMAT NUMBERS####
          watchlist_entry = re.sub('[^0-9,]', "", str(watchlist_entry)).replace(",", "")
          current_price = float(current_price.replace("$","").replace(",",""))

          ######WRITE CRYPTO VALUES TO DATABASE AS NEW TABLE######
          databaseHandling.writeStatsToCryptoTable(name_for_database, watchlist_entry, current_price)
          print(f'Progess: {round(i/a*100,2)} %)' )
         
      
      driver.close()
      




if __name__ == '__main__':
    print(f'Starting {__name__} autonomously...')

    print(f'Testing parseCryptoUrls')
    parseCryptoUrls()
    
    print('Testing parseWatchlistEntry')
    parseWatchlistEntry()

    print(f'Finished testing {__name__}!')
