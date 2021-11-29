#!/usr/bin/python3

###     zentrales Modul zum Austausch der Daten aus der SQLite Datenbank


import sqlite3
import pandas as pd
from datetime import datetime
dbDatum = datetime.today().strftime('%Y%m')

def createCryptoURLTable():
    datenbankname = 'database/trufflepig.db'

    tbl_name = 'crypto_urls'

    db = sqlite3.connect(datenbankname)

    cursor = db.cursor()

    try:

        tableCreation = '''CREATE TABLE IF NOT EXISTS ''' + tbl_name + ''' (
                                    url TEXT PRIMARY KEY UNIQUE);'''

        cursor.execute(tableCreation)

        db.commit()
        db.close()

        return 1

    except sqlite3.Error as error:

        print("Failed to create sqlite table", error)

        db.commit()
        db.close()

        return 0


def createSingleCryptoTable(tablename):
    datenbankname = 'database/trufflepig.db'

    tbl_name = tablename

    db = sqlite3.connect(datenbankname)

    cursor = db.cursor()

    try:

        tableCreation = '''CREATE TABLE IF NOT EXISTS ''' + tbl_name + ''' (
                                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    watchlist REAL,
                                    price REAL);'''

        cursor.execute(tableCreation)

        db.commit()
        db.close()

        return 1

    except sqlite3.Error as error:

        print("Failed to create sqlite table", error)

        db.commit()
        db.close()

        return 0


def appendTableWithUrls(crypto_url, suffix=None):
    datenbankname = 'database/trufflepig.db'

    tbl_name = 'crypto_urls'

    db = sqlite3.connect(datenbankname)
    cursor = db.cursor()

    try:
     
         sqlstatement = ''' INSERT OR IGNORE INTO ''' + tbl_name + ''' (url) VALUES (?);'''
     
         cursor.execute(sqlstatement, (crypto_url,))
     
         #print(f'Eintrag für {crypto_url} zur Datenbank hinzugefügt bzw. ignoriert, da bereits vorhanden.')
     
    except Exception as e:

         print(f'{e}, Eintrag für {crypto_url} konnte nicht hinzugefügt werden.')

    db.commit()
    db.close()



def readUrls():

    datenbankname = 'database/trufflepig.db'

    tbl_name = 'crypto_urls'

    db = sqlite3.connect(datenbankname)

    try:

        df = pd.read_sql_query("SELECT url FROM " + tbl_name, db)

    except Exception as e:

        print('Failed: ' + str(e))

    db.close()

    return df


def writeStatsToCryptoTable(datatable_name, watchlist, current_price):
    
    datenbankname = "database/trufflepig.db"

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)
    cursor = db.cursor()

    try:

        sqlstatement = '''INSERT OR IGNORE INTO ''' + tbl_name + ''' (watchlist, price) VALUES (?, ?);'''
        
        cursor.execute(sqlstatement, (watchlist, current_price))

    except Exception as e:

         print(f'{e}, Eintrag für {tbl_name} konnte nicht hinzugefügt werden.')

    db.commit()
    db.close()



def readStatsFromCryptoTable(datatable_name):

    datenbankname = 'database/trufflepig.db'

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)

    try:
        df = pd.read_sql_query("SELECT watchlist, price FROM " + tbl_name, db)

    except Exception as e:

        print('Failed: ' + str(e))

    db.close()

    return df



def createStatsTable(tablename):
    datenbankname = 'database/stats_trufflepig.db'

    tbl_name = tablename

    db = sqlite3.connect(datenbankname)

    cursor = db.cursor()

    try:

        tableCreation = '''CREATE TABLE IF NOT EXISTS ''' + tbl_name + ''' (
                                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    deviation REAL,
                                    mean REAL,
                                    correlation REAL);'''

        cursor.execute(tableCreation)

        db.commit()
        db.close()

        return 1

    except sqlite3.Error as error:

        print("Failed to create sqlite table", error)

        db.commit()
        db.close()

        return 0

def writeStatsToStatsTable(datatable_name, deviation, mean, correlation):
    
    datenbankname = "database/trufflepig.db"

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)
    cursor = db.cursor()

    try:

        sqlstatement = '''INSERT OR IGNORE INTO ''' + tbl_name + ''' (deviation, mean, correlation) VALUES (?, ?);'''
        
        cursor.execute(sqlstatement, (deviation, mean, correlation))

    except Exception as e:

         print(f'{e}, Eintrag für {tbl_name} konnte nicht hinzugefügt werden.')

    db.commit()
    db.close()





