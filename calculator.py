#!/usr/bin/python3

'''CALCULATES THE THRESHOLD AND RETURNS POSSIBLE OUTLIERS'''

import pandas as pd
import databaseHandling


def calculateMeanAndDeviation():
   '''Read in every Crypto as Pandas dataframe, calculate deviation, mean and correlation and saves it back to database.
   This job is separated from the one above, to make the calculation run offline with raw data from job above and to allow for parallel threading in a later stage.'''
   
   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):
       name_for_database = f'[{urls.loc[i,"url"]}]'
       data = databaseHandling.readStatsFromCryptoTable(name_for_database)
       length = len(data)
   
       #Only dataframes with more than one entry
       if length > 1:
           d = data['watchlist'] - data['watchlist'].shift(1)
           print(f"Watchlist: {data['watchlist']} / WatchList_before: {data['watchlist'].shift(1)} = {d}")
           #data['deviation'].iloc[-1] = d 
   
           #m = data.deviation.mean()
           #print(f'Mean deviation: {m}')
           #data['mean'].iloc[-1] = m 

           #databaseHandling.writeStatsToCryptoTable(name_for_database, watchi, devi, meani)
           
   
       else:
           print(f'New coin detected, table: {name_for_database}. Default values stay unchanged, since only one entry is available.')
  



def calculateOutliers(): 
   '''Calculate outliers'''

   resultList = []
   trashList = []

   lower_dev = 0 #0 percentage deviation, meaning, that a deviation greater than the mean is enough
   higher_dev = 0.10 #10 percentage deviation

   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):
     name_for_database = f'[{urls.loc[i, "url"]}]'
     name_for_mail = name_for_database.split("/")[2]
     data = databaseHandling.readStatsFromCryptoTable(name_for_database)
    
     length = len(data)
    
     if length > 1:
         last_watchlist = data['watchlist'].iloc[-1]
         last_deviation = data['deviation'].iloc[-1]
         last_mean = data['mean'].iloc[-1]
    
         lower_threshold = last_mean * (1+lower_dev)
         higher_threshold = last_mean * (1+higher_dev)
         msgBig = f'{name_for_mail}: Last wachtlist entry: {last_watchlist}; Last mean: {last_mean} / Last Deviation: {last_deviation}'

         if last_deviation > higher_threshold:
             msg = f'!!! {msgBig} // Last deviation (={last_deviation}) > Higher threshold (={higher_threshold})'
             print(msg)
             resultList.append(msg)
    
         elif last_deviation < higher_threshold and last_deviation > lower_threshold:
             msg = f'Lower threshold (={lower_threshold}) > Last deviation (={last_deviation}) < Higher threshold (={higher_threshold}): {msgBig}'
             print(msg)
             resultList.append(msg)

         else:
             print(msgBig)
             trashList.append(msgBig)

     else:
         print(f'Skipped Outlier-Calculation ({name_for_mail}, only one entry)')

    
   return (resultList, trashList)


if __name__ == '__main__':

    print(f'Testing {calculateMeanAndDeviation} autonomously...')
    calculateMeanAndDeviation()
    print(f'Finished testing')


#    print(f'Testing {calculateOutliers}')
#    results = calculateOutliers()
#
#    import mailHandler
#
#    recipient = 'khlrtbs@gmail.com'
#    subject = "TEST"
#    mailHandler.sendMail(recipient,subject, results)

    print("Finished testing")
