from py2neo import neo4j
from py2neo import node, rel, ogm
from py2neo import cypher
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
    tagName = StringProperty(unique_index=True, required=True)
    tagIndex = IntegerProperty(unique_index=True)

# define class for Img Nodes
class Img(StructuredNode):
    """Img node stores src for each meme img with aggregate 
    weight of all selections"""
    imgIndex = StringProperty(unique_index=True)
    imgSrc = StringProperty(required=True)
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
        #so this part is working properly as it has added images notes to the 
        imgNode = Img(imgSrc=img, aggregateImgWeight=0).save()
        imgNode.refresh()
        
        for tag in memeDict[img]:
            #check if tag exists already in the database (this part is not working)
            if not Tag.index.search(tagName=tag):
                     #created the tag 
                tagNode = Tag(tagName=tag).save()
                tagNode.refresh()
                print tagNode
                #connect it to the img with the relationship (write this one as a cypher query)
                query = "MATCH (i:'{imgNode}'), (t:'{tagNode}') CREATE (i)-[r:TAGGED]->(t) RETURN r"
                params = {'imgNode': dir(imgNode.imgIndex, 'tagNode':tagNode.tagName}
                print params
                taggedRelationship = cypher.execute(graph_db, query, params)
                print taggedRelationship

         
            else:
                query = "MATCH ()-[r:TAGGED]-() return r"
                taggedRelationship = cypher.execute(graph_db, query)
                print "This is the tagged relationship[0]", taggedRelationship[0]
                # cypher_query.append(query, params)
                #params = dictionary of parameters (properties)
                # taggedRelationship.aggregateImgTagWeight += 1
                # taggedRelationship.commit
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
