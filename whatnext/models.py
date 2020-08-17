"""
This module contains the db table models for the 'What next' application
"""
from py2neo import Graph, Node, Relationship,NodeMatcher

class Tags:
    "Model the tags"
    def __init__(tech):
        tech_word = tech

    def fetch_nodes(self,tech_word):
        graph = Graph("http://neo4j:TestQxf2@127.0.0.1/db/data")
        matcher = NodeMatcher(graph)
        match_nodes = matcher.match(tagName=tech_word).first()
        return (list(r.end_node["tagName"] for r in graph.match(nodes=(match_nodes,)).limit(6)))

