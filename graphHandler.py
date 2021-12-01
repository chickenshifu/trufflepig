#!/usr/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import databaseHandling



def simple_graph(name_for_database):

   raw_data = databaseHandling.readStatsFromCryptoTable(name_for_database)
   watchlist_list = raw_data['watchlist']
   price_list = raw_data['price']

   
   raw_data.plot()
   plt.show()





if __name__ == '__main__':

    print(f'Testing {simple_graph} autonomously...')
    n = '[/currencies/bitcoin/]'
    simple_graph(n)
    print('Finished testing')
    





