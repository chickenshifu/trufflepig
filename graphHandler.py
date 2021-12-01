#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import databaseHandling
import datetime
import os 


def simple_graph(name_for_database):

   name_for_mail = name_for_database.split("/")[2]
   now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
   current_directory_path = os.getcwd()
   file_name = f'charts/{name_for_mail}_{now}.png'
   file_path = os.path.join(current_directory_path, file_name)
   print(file_path)

   raw_data = databaseHandling.readStatsFromCryptoTable(name_for_database)
   raw_stats = databaseHandling.readStatsFromStatsTable(name_for_database)
   
   deviation_list = raw_stats['deviation']
   length = len(deviation_list)
   print(length)
   mean_list = raw_stats['mean']
   corr_list = raw_stats['correlation']

   watchlist_list = raw_data['watchlist'][:length]
   price_list = raw_data['price'][:length]


   # create figure and axis objects with subplots()
   fig,ax = plt.subplots()
   # make a plot
   ax.plot(price_list, color="red", marker="o", markersize=0.8, linewidth=0.5)
   # set x-axis label
   ax.set_xlabel("time",fontsize=10)
   # set y-axis label
   ax.set_ylabel("price(usd)",color="red",fontsize=10)
   ax.set_title(f'wtchlst(delta) vs. prc(usd) - {name_for_mail}')

   # twin object for two different y-axis on the sample plot
   ax2=ax.twinx()
   # make a plot with different y-axis using second axis object
   ax2.plot(mean_list,color="blue",marker="x", markersize=0.8, linewidth=0.5)
   ax2.set_ylabel("mean deviation(watchlist)",color="blue", fontsize=10)
   plt.show()
   # save the plot as a file
   fig.savefig(file_path,
               dpi=100,
               bbox_inches='tight')
      
   


if __name__ == '__main__':

    print(f'Testing {simple_graph} autonomously...')
    n = '[/currencies/ethereum/]'
    simple_graph(n)
    print('Finished testing')
    





