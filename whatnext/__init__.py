"""
This module contains the initial Flask configuration for the 'What next' application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .models import graph


app = Flask(__name__)
db_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data','whatnext.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///%s"%db_file
db = SQLAlchemy(app)

from whatnext import routes

