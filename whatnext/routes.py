"""
This file contains all the endpoints for the 'What next' application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response, session
from sqlalchemy import or_
from whatnext import app
from whatnext import db
from whatnext.models import Tags
import itertools

@app.route("/",methods=["GET","POST"])
def home():
    "Return the index page"
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        tags_object = Tags()
        query_string = request.form.get('terms')
        technologies = query_string.split(',')
        associated_tech_graph = {'nodes':[],'edges':[]}
        tech_id = 1
        edge_id = 100
        for tech in technologies:
            tech = tech.strip().lower()
            tech_pair_rows = tags_object.fetch_nodes(tech)
            if tech not in associated_tech_graph['nodes']:
                associated_tech_graph['nodes'].append(tech)
            for row in tech_pair_rows:
                if row not in associated_tech_graph['nodes']:
                    associated_tech_graph['nodes'].append(row)
                if [row,tech] not in associated_tech_graph['edges']:
                    associated_tech_graph['edges'].append([row,tech])

        return jsonify({'graph':associated_tech_graph})