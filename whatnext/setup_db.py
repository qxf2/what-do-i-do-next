"""
Run this file to setup your database for the first time.

insert into tag(name) select 'python' where not exists(select name from tag where name='python');
INSERT INTO tag(name) SELECT 'python' WHERE NOT exists(SELECT name from tag where name='python')
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

def setup_raw_data(db_cursor,csv_file):
    "Setup raw data"
    csv_row_data = get_csv_row_data(csv_file)
    db_cursor.executemany("INSERT INTO {} VALUES (?,?,?,?,?)".format(RAW_TABLE),csv_row_data)
        
    return db_cursor

def setup_tag_pair_data(db_cursor):
    "Setup the tag pairs"
    all_raw_rows = db_cursor.execute("SELECT * FROM {}".format(RAW_TABLE)).fetchall()
    tag_query = "INSERT INTO {} ({}) SELECT '{}' WHERE NOT exists(SELECT {} from {} where {}='{}')"
    tag_pair_query_select = "SELECT * FROM {} where {} = '{}' and {} = '{}'"
    tag_pair_query_insert = "INSERT OR REPLACE INTO {} VALUES (?,?,?,?)"
    for row in all_raw_rows:
        tag_data = row[3].split('|')
        tag_data = [x.lower() for x in tag_data]
        tag_data.sort()
        view_count = int(row[4])
        for tag in tag_data:
            db_cursor.execute(tag_query.format(TAG_TABLE,TAG_COL_2,tag,TAG_COL_2,TAG_TABLE,TAG_COL_2,tag))
        for i,first_tag in enumerate(tag_data[:-1]):
            for second_tag in tag_data[i+1:]:
                result = db_cursor.execute(tag_pair_query_select.format(TAG_PAIR_TABLE,TAG_PAIR_COL_1,first_tag,TAG_PAIR_COL_2,second_tag)).fetchone()
                if result is None:
                    count = 1
                else:
                    count = result[2] + 1
                    view_count += int(result[3])
                db_cursor.execute(tag_pair_query_insert.format(TAG_PAIR_TABLE),(first_tag,second_tag,1,view_count))

    return db_cursor

def get_csv_row_data(csv_file):
    "Return csv row data in a format suitable for executemany"
    row_data = []
    with open(csv_file,'r') as fp:
        all_rows = csv.DictReader(fp)
        row_data = [(row[COL_1], row[COL_2], row[COL_3], row[COL_4], row[COL_5]) for row in all_rows]
    
    return row_data

def create_tables(db_cursor):
    "Create the tables"
    #Raw table
    db_cursor.execute("CREATE TABLE IF NOT EXISTS {}({} TEXT,{} TEXT, {} TEXT, {} TEXT, {} TEXT)".format(RAW_TABLE,COL_1,COL_2,COL_3,COL_4,COL_5))
    #Tag table
    db_cursor.execute("CREATE TABLE IF NOT EXISTS {}({} integer PRIMARY KEY, {} char(256))".format(TAG_TABLE,TAG_COL_1,TAG_COL_2))
    #Tag pair table
    db_cursor.execute("CREATE TABLE IF NOT EXISTS {}({} char(256), {} char(256), {} integer, {} integer, PRIMARY KEY ({}, {}))".format(TAG_PAIR_TABLE,TAG_PAIR_COL_1,TAG_PAIR_COL_2,TAG_PAIR_COL_3,TAG_PAIR_COL_4,TAG_PAIR_COL_1,TAG_PAIR_COL_2))

def create_db(csv_file):
    "Create the database for the first time"
    conn = create_connection_obj()
    db_cursor = conn.cursor()
    create_tables(db_cursor)
    db_cursor = setup_raw_data(db_cursor,csv_file)
    conn.commit()
    db_cursor = setup_tag_pair_data(db_cursor)
    conn.commit()
    conn.close()
    #Load DB with data until today
    

def setup_database(csv_file):
    "Setup the database"
    if not os.path.exists(DB_FILE):
        create_db(csv_file)
    print("Done")
    

#----START OF SCRIPT
if __name__=='__main__':
    csv_file = os.path.join(ROOT_DIR,'data','stackoverflow_data.csv')
    usage = "USAGE:\npython {} <optional: path to stackoverflow csv data>\npython {} ../data/stackoverflow_data.csv".format(__file__,__file__)
    if len(sys.argv)>1:
        if not os.path.exists(sys.argv[1]):
            print("Could not locate the csv file {}".format(sys.argv[1]))
            print(usage)
        elif not sys.argv[1][-4:]=='.csv':
            print("Please provide a valid CSV file as input")
            print(usage)
        else:
            csv_file = os.path.abspath(sys.argv[1])

    setup_database(csv_file)