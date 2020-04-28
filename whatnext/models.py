"""
This module contains the db table models for the 'What next' application
"""
from whatnext import db
#from sqlalchemy import Integer, ForeignKey, String, Column,CheckConstraint
#from py2neo import Graph,Relationship,Node
from py2neo import Graph, Node, Relationship


class Neodb:
    "Model the tags"
    print("I am coming here")
    def tags(self):
        graph = Graph("http://neo4j:TestQxf2@127.0.0.1/db/data")
        try:
            graph.run("Match () Return 1 Limit 1")
            print('ok')
        except Exception:
            print('not ok')
        tags1=Node("Table",tagName="Java")
        tags2=Node("Table",tagName="Selenium")
        tags3=Node("Table",tagName="Python")
        graph.create(tags1)
        graph.create(tags2)
        graph.create(tags3)

    """def tagpair():
        tagpair1 = Node("Tagpair",tagpair="Python,Selenium",viewpair="1000")
        tagpair2 = Node("Tagpair",tagpair="Jenkins,Selenium",viewpair="100")
        tagpair3 = Node("Tagpair",tagpair="Python,Jenkins",viewpair="5000")
        tagpair4 = Node("Tagpair",tagpair="Jenkins,Java",viewpair="13567")
        tagpair5 = Node("Tagpair",tagpair="aws,java,Selenium",viewpair="1521")
        tags= 'python|selenium|jenkins'

        tags = [x.strip() for x in tags.lower().split('|')]
        for t in set(tags):
            tag = graph.merge_one("Tag", "name", t)
            rel = Relationship(tag, "TAGGED", tagpair1)
            graph.create(rel)"""

"""class Raw(db.Model):
    "Model the raw table" 
    row_id = db.Column(db.String,primary_key=True)   
    answer_count = db.Column(db.String)
    last_activity_date = db.Column(db.String)
    tags = db.Column(db.String)    
    view_count = db.Column(db.String)

class Tagpair(db.Model):
    "Model the tag pair table"
    tag1 = db.Column(db.String,primary_key=True)
    tag2 = db.Column(db.String,primary_key=True)
    count = db.Column(db.Integer)"""
