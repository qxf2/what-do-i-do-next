"""
Run this file to setup your database for the first time.
"""
import time
import sys
import sqlite3
import os
import datetime
import csv

CURR_FILEPATH = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURR_FILEPATH)
DB_FILE = os.path.join(ROOT_DIR,'data','whatnext.db')

RAW_TABLE = 'raw'
COL_1 = 'id'
COL_2 = 'answer_count'
COL_3 = 'last_activity_date'
COL_4 = 'tags'
COL_5 = 'view_count'

TAG_TABLE = 'tag'
TAG_COL_1 = 'id'
TAG_COL_2 = 'name'

TAG_PAIR_TABLE = 'tag_pair'
TAG_PAIR_COL_1 = 'tag1'
TAG_PAIR_COL_2 = 'tag2'
TAG_PAIR_COL_3 = 'count'
TAG_PAIR_COL_4 = 'view_count'

def create_connection_obj():
    "Return a connection object"
    return sqlite3.connect(DB_FILE)

def setup_tag_pair_data():
    "Setup the tag pairs"
    pass

def get_csv_row_data():
    "Return csv row data in a format suitable for executemany"
    row_data = []
    with open(CSV_FILE,'rb') as fp:
        all_rows = csv.DictReader(fp)
        row_data = [(row[COL_1], row[COL_2], row[COL_3], row[COL_4], row[COL_5]) for row in all_rows]
    
    return row_data

def create_tables(db_cursor):
    "Create the tables"
    #Raw table
    db_cursor.execute("CREATE TABLE IF NOT EXISTS {}({} TEXT,{} TEXT, {} TEXT, {} TEXT, {} TEXT)".format(RAW_TABLE,COL_1,COL_2,COL_3,COL_4,COL_5))
    #Tag table
    db_cursor.execute("CREATE TABLE {}({} integer PRIMARY KEY, {} char(256))".format(TAG_TABLE,TAG_COL_1,TAG_COL_2))
    #Tag pair table
    db_cursor.execute("CREATE TABLE {}({} char(256), {} char(256), {} integer, {} integer)".format(TAG_PAIR_TABLE,TAG_PAIR_COL_1,TAG_PAIR_COL_2,TAG_PAIR_COL_3,TAG_PAIR_COL_4))

def create_db():
    "Create the database for the first time"
    conn = create_connection_obj()
    db_cursor = conn.cursor()
    create_tables(db_cursor)
    csv_row_data = get_csv_row_data()
    if len(csv_row_data):
        db_cursor.executemany("INSERT INTO {} ")
    conn.commit()
    conn.close()
    #Load DB with data until today
    setup_tag_pair_data()

def setup_database():
    "Setup the database"
    if not os.path.exists(DB_FILE):
        create_db()
    print("Done")
    

#----START OF SCRIPT
if __name__=='__main__':
    setup_database()