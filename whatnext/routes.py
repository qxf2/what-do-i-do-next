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
        associated_tech_graph = {'nodes':[],'edges':[]}
        tech_id = 1
        edge_id = 100
        for tech in technologies:
            tech = tech.strip().lower()
            tech_pair_rows = Tagpair.query.filter(Tagpair.tag1==tech or Tagpair.tag2==tech).order_by(Tagpair.count.desc()).limit(5)
            for row in tech_pair_rows:
                if row.tag1 not in associated_tech_graph['nodes']:
                    associated_tech_graph['nodes'].append(row.tag1)
                if row.tag2 not in associated_tech_graph['nodes']:
                    associated_tech_graph['nodes'].append(row.tag2)
                if [row.tag1,row.tag2] not in associated_tech_graph['edges']:
                    associated_tech_graph['edges'].append([row.tag1,row.tag2])
        return jsonify({'graph':associated_tech_graph})