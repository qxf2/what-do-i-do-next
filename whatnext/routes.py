"""
This file contains all the endpoints for the 'What next' application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response, session
from whatnext import app
from whatnext import db
from whatnext.models import Raw, Tagpair

@app.route("/",methods=["GET","POST"])
def home():
    "Return the index page"
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        query_string = request.form.get('terms')
        technologies = query_string.split(',')
        associated_tech = []
        for tech in technologies:
            tech_pair_rows = Tagpair.query.filter(Tagpair.tag1==tech or Tagpair.tag2==tech).order_by(Tagpair.count.desc()).limit(5)
            for row in tech_pair_rows:
                associated_tech.append(row.tag1)
                associated_tech.append(row.tag2)
        associated_tech = list(set(associated_tech))
        return jsonify({'answer':associated_tech})
