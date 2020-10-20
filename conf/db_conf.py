""" This file contains the neo4j DB URL """
import os

db_url = "http://neo4j:TestQxf2@127.0.0.1/db/data"
csv_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/stackoverflow_data.csv'))
db_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data','whatnext.db'))