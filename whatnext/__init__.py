"""
This module contains the initial Flask configuration for the 'What next' application
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import conf.db_conf as url

app = Flask(__name__)
db_file = url.db_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s"%db_file
db = SQLAlchemy(app)

from whatnext import routes
