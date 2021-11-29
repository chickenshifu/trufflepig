#!/usr/bin/python3

import pandas as pd
import databaseHandling


def calculateDeviation():
   '''Calculates deviation between watchlist entries'''

   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):
       name_for_database = f'[{urls.loc[i,"url"]}]'
       print(f'Calculating for {name_for_database}')
       data = databaseHandling.readStatsFromCryptoTable(name_for_database)
       length = len(data)
   
       #Only dataframes with more than one entry
       if length > 1:
           databaseHandling.createStatsTable(name_for_database)
           d = data['watchlist'] - data['watchlist'].shift(1)
           d_last = d.iloc[-1]
           print(f"Deviation: {d_last}")

           last_row_id = databaseHandling.writeDeviationToStatsTable(name_for_database, d_last)
           print(f'Last row id (initially from calculateDeviation()): {last_row_id}')
           return last_row_id
   
       else:
           print(f'New coin detected, table: {name_for_database}. Default values stay unchanged, since only one entry is available.')
 

def calculateMeanDeviation(last_row_id):
   '''Calculates mean of deviation of watchlist entries'''

   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):
       name_for_database = f'[{urls.loc[i,"url"]}]'
       print(f'Calculating for {name_for_database}')
       data = databaseHandling.readStatsFromStatsTable(name_for_database)
   
       m = data['deviation'].mean()
       print(f"Mean (deviation): {m}")

       databaseHandling.writeMeanDeviationToStatsTable(name_for_database, m, last_row_id)
   

def calculateCorrelation():
   '''Calculates correlation between deviation and price'''

   urls = databaseHandling.readUrls()
   a = len(urls)
   
   for i in range(0,a-1):
       name_for_database = f'[{urls.loc[i,"url"]}]'
       print(f'Calculating for {name_for_database}')
       data = databaseHandling.readStatsFromCryptoTable(name_for_database)
   
       c = data['watchlist'].corr(data['price'])
       print(f"Correlation (watchlist deviation vs. price): {c}")

       databaseHandling.writeCorrelationToStatsTable(name_for_database, c)


def calculateOutliers(): 
   '''Calculate outliers'''

   resultList = []
   trashList = []

   lower_dev = 0.10 #10 percentage deviation, meaning, that a deviation greater than the mean is enough
   higher_dev = 0.25 #25 percentage deviation

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

     print(f'Testing {calculateDeviation} autonomously...')
     last_row_id = calculateDeviation()
     print('Finished testing')

     print(f'Testing {calculateMeanDeviation} autonomously...')
     calculateMeanDeviation(last_row_id)
     print('Finished testing')

     print(f'Testing {calculateCorrelation} autonomously...')
     calculateCorrelation()
     print('Finished testing')

     print(f'Testing {calculateOutliers}')
     results = calculateOutliers()

     import mailHandler

     subject = "TEST"
     mailHandler.sendMail(recipient,subject, results)

     print("Finished testing")
