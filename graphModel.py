from py2neo import neo4j
from py2neo import node, rel, ogm
from neomodel import (StructuredNode, StructuredRel, StringProperty, FloatProperty, IntegerProperty,
    Relationship, RelationshipTo, RelationshipFrom)
import scraper

graph_db = neo4j.GraphDatabaseService("http://localhost:7476/db/data/")
store = ogm.Store(graph_db)

#############################################################
################## Class Declarations Here ##################
#############################################################

###----------------These are Relationships----------------###

# define class for Selected Rel
class SelectedRelationship(StructuredRel):
    """Selected Relationship stores the weight for each img-tag
     relationship per user."""
    specificImgTagWeight = FloatProperty()
        
# define class for Tagged Rel
class TaggedRelationship(StructuredRel):
    """Tagged relationship stores the aggregate weight of all 
    users who have tagged the tag-img realtionship."""
    aggregateImgTagWeight = FloatProperty(default=1)

# define class for Given Rel
class GivenRelationship(StructuredRel):
    """Given relationship defines the relationship between 
    images that were given to the user based on a certain tag, 
    regardless of selection."""
    #count number of times given (gievn weight)

# define class for Searched Rel
class SearchedTagRelationship(StructuredRel):
    """Defines the relationship between users and the tags 
    they search for."""
    #count number of times given (gievn weight)

###------------------These are Nodes-------------------###

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
    imgTags = Relationship('Tag', 'TAGGED', model=TaggedRelationship)

#############################################################
##################### functions #############################
#############################################################
#call functions from scraper that return things with scraper.blah
def createGraph(memeDict):
    #make a function to create graph db
    #create a list of nodes

    images = []
    tags = []
    for img in memeDict:
        imgNode = Img(imgSrc=img, aggregateImgWeight=0).save()
        
        for tag in memeDict[img]:
            #check if tag exists already
            if Tag.index.get(tagName=tag):
                #increment
                taggedRelationship.aggregateImgTagWeight += 1 
            #or create new tag
            else:
                #created the tag 
                tagNode = Tag(tagName=tag).save()
                #connect it to the img with the relationship
                taggedRelationship = imgNode.tagged.connect(tagNode)
                #and set the aggregate weight = 1
                taggedRelationship.aggregateImgTagWeight = 1 
            return "The createGraph function ran! Check DB to see if it worked."



def main():
    urls = ['http://icanhas.cheezburger.com/tag/dogs/', 
        'http://icanhas.cheezburger.com/tag/cats/',
        'http://roflrazzi.cheezburger.com/history'] 

    """In case we need this for something."""
    memeDict = scraper.listOfDictsOfMemes(urls)
    createGraph(memeDict)

if __name__ == "__main__":
    main()
