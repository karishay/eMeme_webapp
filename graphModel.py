from py2neo import neo4j
from py2neo import node, rel, ogm
from neomodel import (StructuredNode, StructuredRel, StringProperty, FloatProperty, IntegerProperty,
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
    name = StringProperty(unique_index=True, required=True)
    #must be gmail login for google auth and session cookies
    email = StringProperty(unique_index=True, required=True)
    #maybe not needed if google auth doesn't give passwords
    password = IntegerProperty(unique_index=True)

# define class for Tag Nodes
class Tag(StructuredNode):
    """ Tag node creates new tags in Neo4j"""
    tagName = StringProperty(unique_index=True)

# define class for Img Nodes
class Img(StructuredNode):
    """Img node stores src for each meme img with aggregate 
    weight of all selections"""
   imgSrc = StringProperty(unique_index=True, required=True)
   aggregateImgWeight = FloatProperty()

# define class for Selected Rel
class SelectedRelationship(StructuredRel):
    """Selected Relationship stores the weight for each img-tag
     relationship per user."""
    specificImgTagWeight = FloatProperty()
        
# define class for Tagged Rel
class TaggedRelationship(StructuredRel):
    """Tagged relationship stores the aggregate weight of all 
    users who have tagged the tag-img realtionship."""
    aggregateImgTagWeight = FloatProperty()

# define class for Given Rel
class GivenRelationship(StructuredRel):
    """Given relationship defines the relationship between 
    images that were given to the user based on a certain tag, 
    regardless of selection."""

# define class for Searched Rel
class SearchedTagRelationship(StructuredRel):
    """Defines the relationship between users and the tags 
    they search for."""

#############################################################
##################### functions #############################
#############################################################
#call functions from scraper that return things with scraper.blah
def createGraph():
    #make a function to create graph db
    imgs = Img.create(
        #iterate through the keys of the dictionary from the scraper
        )


    pass

#define a function the recieves the assets from scraper
#and creates the nodes and relationships in db



def main():
    """In case we need this for something."""


if __name__ == "__main__":
    main()
