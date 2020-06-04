"""
This module contains the db table models for the 'What next' application
"""
#from whatnext import db
#from sqlalchemy import Integer, ForeignKey, String, Column,CheckConstraint
#from py2neo import Graph,Relationship,Node
from py2neo import Graph, Node, Relationship,NodeMatcher
import pandas as pd


class Neodb:
    "Model the tags"
    print("I am coming here")
    graph = Graph("http://neo4j:TestQxf2@127.0.0.1/db/data")
    all_tag_list = []
    final_list = []
    try:
        graph.run("Match () Return 1 Limit 1")
        df=pd.read_csv("C:/Users/annap/code/what-do-i-do-next/data/stackoverflow_data.csv")

        graph.delete_all()

        matcher = NodeMatcher(graph)
        row_count = len(df)
        for each_tags in df['tags']:
            each_tag = each_tags.split('|')
            tag_data = [x.lower() for x in each_tag]
            for each_tag_data in tag_data:
                all_tag_list.append(each_tag_data)

        final_list=list(set(all_tag_list))
        final_list.sort()

        for i,tags in enumerate(final_list):
            vartag = "tag"+str(i)
            var_tag = Node("May21tag",tagName=tags)

            graph.create(var_tag)

        for i in range(row_count):
            answer_count = df['answer_count'][i]
            view_count = df['view_count'][i]
            tags = df['tags'][i]
            each_tag = tags.split('|')
            tag_data = [x.lower() for x in each_tag]
            for j,first_tag in enumerate(tag_data[:-1]):
                match_first_tag = matcher.match("May21tag",tagName=first_tag).first()
                #Adding the answer count and view count to the nodes
                match_first_tag['answer_count']=answer_count.item()
                match_first_tag['view_count']=view_count.item()
                graph.push(match_first_tag)
                for second_tag in tag_data[j+1:]:
                    my_tag = second_tag
                    second_tag = matcher.match("May21tag",tagName=second_tag).first()
                    #Adding the answer count and view count to the nodes
                    second_tag['answer_count']=answer_count.item()
                    second_tag['view_count']=view_count.item()
                    graph.push(second_tag)
                    create_relationship = Relationship(match_first_tag ,"tagged",second_tag)
                    graph.merge(create_relationship)
                    #Check how many relations are there between the nodes

                    check_exists =len(graph.match(nodes=[match_first_tag,second_tag],r_type="tagged"))

    except Exception as e:
        print('not ok',e)
