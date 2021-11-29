#!/usr/bin/python3

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
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                    deviation REAL,
                                    mean REAL,
                                    correlation INTEGER);'''

        cursor.execute(tableCreation)

        db.commit()
        db.close()

        return 1

    except sqlite3.Error as error:

        print("Failed to create sqlite table", error)

        db.commit()
        db.close()

        return 0

def writeDeviationToStatsTable(datatable_name, deviation):
    
    datenbankname = "database/stats_trufflepig.db"

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)
    cursor = db.cursor()

    try:

        sqlstatement = '''INSERT OR IGNORE INTO ''' + tbl_name + ''' (deviation) VALUES (?);'''
        
        cursor.execute(sqlstatement, (deviation,))

        db.commit()
        return cursor.lastrowid

    except Exception as e:

         print(f'{e}, Eintrag für {tbl_name} konnte nicht hinzugefügt werden.')

         return -1

    db.close()


def readStatsFromStatsTable(datatable_name):

    datenbankname = 'database/stats_trufflepig.db'

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)

    try:
        df = pd.read_sql_query("SELECT deviation, mean, correlation FROM " + tbl_name, db)

    except Exception as e:

        print('Failed: ' + str(e))

    db.close()

    return df


def writeMeanDeviationToStatsTable(datatable_name, mean, last_row_id):
    
    datenbankname = "database/stats_trufflepig.db"

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)
    cursor = db.cursor()

    try:

        sqlstatement = '''UPDATE ''' + tbl_name + ''' SET (mean) = (?) WHERE (id) = (?);'''
        
        cursor.execute(sqlstatement, (mean, last_row_id,))

    except Exception as e:

         print(f'{e}, Eintrag für {tbl_name} konnte nicht hinzugefügt werden.')

    db.commit()
    db.close()



def writeCorrelationToStatsTable(datatable_name, correlation, last_row_id):
    
    datenbankname = "database/stats_trufflepig.db"

    tbl_name = datatable_name

    db = sqlite3.connect(datenbankname)
    cursor = db.cursor()

    try:

        sqlstatement = '''UPDATE ''' + tbl_name + ''' SET (correlation) = (?) WHERE (id) = (?);'''
        
        cursor.execute(sqlstatement, (correlation, last_row_id,))

    except Exception as e:

         print(f'{e}, Eintrag für {tbl_name} konnte nicht hinzugefügt werden.')

    db.commit()
    db.close()
