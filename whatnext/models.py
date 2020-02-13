"""
This module contains the db table models for the 'What next' application
"""
from whatnext import db
from sqlalchemy import Integer, ForeignKey, String, Column,CheckConstraint

class Raw(db.Model):
    "Add the raw table" 
    row_id = db.Column(db.String,primary_key=True)   
    answer_count = db.Column(db.String)
    last_activity_date = db.Column(db.String)
    tags = db.Column(db.String)    
    view_count = db.Column(db.String)