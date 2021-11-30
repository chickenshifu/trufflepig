#!/usr/bin/python3

import pandas as pd
import databaseHandling

def calculateStats():

   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):

       #1. CALCULATING DEVIATION
       name_for_database = f'[{urls.loc[i,"url"]}]'
       print(f'Calculating for {name_for_database}')
       data = databaseHandling.readStatsFromCryptoTable(name_for_database)
       length = len(data)
   
       #Only dataframes with more than one entry
       if length > 1:
           databaseHandling.createStatsTable(name_for_database)
           d = data['watchlist'] - data['watchlist'].shift(1)
           d_last = d.iloc[-1]

           last_row_id = databaseHandling.writeDeviationToStatsTable(name_for_database, d_last)
           print(f'Deviation={d_last} written into {name_for_database}. Last row id: {last_row_id}')


           #2. CALCULATING MEAN DEIVATION
           data = databaseHandling.readStatsFromStatsTable(name_for_database)
           m = data['deviation'].mean()
           databaseHandling.writeMeanDeviationToStatsTable(name_for_database, m, last_row_id)
           print(f'{name_for_database} updated in last row id={last_row_id} with mean deviation={m}')

           #3. CALCULATING CORRELATION
           data = databaseHandling.readStatsFromCryptoTable(name_for_database)
           c = data['watchlist'].corr(data['price'])
           databaseHandling.writeCorrelationToStatsTable(name_for_database, c, last_row_id)
           print(f'{name_for_database} updated in last row id={last_row_id} with correlation={c}')

       else:
          print(f'New coin detected, table: {name_for_database}. Default values stay unchanged, since only one entry is available.')




def calculateOutliers(): 
   '''Calculate outliers'''

   resultList = []
   trashList = []

   lower_dev = 0.25 #percentage deviation, meaning, that a deviation greater than the mean is enough
   higher_dev = 0.50 #percentage deviation

   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):
     name_for_database = f'[{urls.loc[i, "url"]}]'
     name_for_mail = name_for_database.split("/")[2]
     data = databaseHandling.readStatsFromCryptoTable(name_for_database)
     data_stats = databaseHandling.readStatsFromStatsTable(name_for_database)
    
     length = len(data)
    
     if length > 1:
         last_watchlist = data['watchlist'].iloc[-1]
         last_deviation = data_stats['deviation'].iloc[-1]
         last_mean = data_stats['mean'].iloc[-1]
    
         lower_threshold = last_mean * (1+lower_dev)
         higher_threshold = last_mean * (1+higher_dev)
         msgBig = f'{name_for_mail}: Last mean: {last_mean} / Last Deviation: {last_deviation}'

         if last_deviation > higher_threshold:
             msg = f'!!! {msgBig} // Last deviation (={last_deviation}) > Higher threshold (={higher_threshold})'
             print(msg)
             resultList.append(msg)
    
         elif last_deviation < higher_threshold and last_deviation > lower_threshold:
             msg = f'{msgBig}: Lower threshold (={lower_threshold}) > Last deviation (={last_deviation}) < Higher threshold (={higher_threshold})'
             print(msg)
             resultList.append(msg)

         else:
             print(msgBig)
             trashList.append(msgBig)

     else:
         print(f'Skipped Outlier-Calculation ({name_for_mail}, only one entry)')

    
   return (resultList, trashList)


if __name__ == '__main__':


     print('Testing {calculateStats()} autonomously...')
     calculateStats()
     print('Finished testing!')
#      print(f'Testing {calculateDeviation} autonomously...')
#      last_row_id = calculateDeviation()
#      print('Finished testing')
# 
#      print(f'Testing {calculateMeanDeviation} autonomously...')
#      calculateMeanDeviation(last_row_id)
#      print('Finished testing')
# 
#      print(f'Testing {calculateCorrelation} autonomously...')
#      calculateCorrelation()
#      print('Finished testing')
# 
     print(f'Testing {calculateOutliers}')
     results = calculateOutliers()

     import mailHandler

     subject = "TEST"
     mailHandler.sendMail(subject, results)

     print("Finished testing")
