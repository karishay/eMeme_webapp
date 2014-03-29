from py2neo import neo4j
from py2neo import node, rel, ogm
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom)
import scraper

graph_db = neo4j.GraphDatabaseService("http://localhost:7476/db/data/")
store = ogm.Store(graph_db)

#############################################################
################## Class Declarations Here ##################
#############################################################
# define class for User Nodes
class User(StructuredNode):
    """UserNode class creates a new user node in Neo4j"""
    name = StringProperty(unique_index=True)
    email = StringProperty(unique_index=True, required=True)
    password = IntegerProperty(unique_index=True, required=True)
        

# define class for Tag Nodes
class Tag(StructuredNode):
    """ Tag node creates new tags in Neo4j"""
    tagName = StringProperty()
# define class for Img Nodes

# define class for Selected Rel

# define class for Tagged Rel

# define class for Given Rel

# define class for Searched Rel

#############################################################
##################### functions #############################
#############################################################
#call functions from scraper that return things with scraper.blah
def createGraph():
    #make a function to create graph db
    pass

#define a function the recieves the assets from scraper
#and creates the nodes and relationships in db



def main():
    """In case we need this for something."""


if __name__ == "__main__":
    main()
