"""
This file contains all the endpoints for the 'What next' application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response, session
from whatnext import app
from whatnext import db

from whatnext.models import Raw

@app.route("/",methods=["GET","POST"])
def home():
    "Return the index page"
    return render_template("index.html")
