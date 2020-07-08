"""
This file contains all the endpoints for the 'What next' application
"""

from flask import render_template, url_for, flash, redirect, jsonify, request, Response, session
from sqlalchemy import or_
from whatnext import app
from whatnext import db
from whatnext.models import Tags

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
            #MATCH (:May21tag { tagName: 'c#' })-->(movie) RETURN movie.tagName
            print(tech)

            tech_pair_rows = tags_object.fetch_nodes(tech)
            print(tech_pair_rows)
            """tech_pair_rows = Tagpair.query.filter(or_(Tagpair.tag1==tech, Tagpair.tag2==tech)).order_by(Tagpair.count.desc()).limit(6)"""
            for row in tech_pair_rows:
                if row.tag1 not in associated_tech_graph['nodes']:
                    associated_tech_graph['nodes'].append(row.tag1)
                if row.tag2 not in associated_tech_graph['nodes']:
                    associated_tech_graph['nodes'].append(row.tag2)
                if [row.tag1,row.tag2] not in associated_tech_graph['edges']:
                    associated_tech_graph['edges'].append([row.tag1,row.tag2])
        return jsonify({'graph':associated_tech_graph})

