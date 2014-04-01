from py2neo import neo4j
from py2neo import node, rel, ogm
from py2neo import cypher
import scraper

graph_db = neo4j.GraphDatabaseService("http://localhost:7476/db/data/")
store = ogm.Store(graph_db)

#############################################################
##################### functions #############################
#############################################################

###----------------These are Relationships----------------###


###---------------------These are Nodes-------------------###
#define a function that creates a node
def createImgNode(memeDict):
    urls = memeDict.keys()
    for url in urls:
        print "url is %s" % url
        imgNode, = graph_db.create({"imgSrc":url, "aWeight":0})
        imgNode.add_labels("IMG")

        for tag in memeDict[url]:
            #if its in the db then add one to the weight
            print "tag is: %s" % tag
            tagNode = getTagNode(tag)
            #rel((imgNode, ("TAGGED", {"aWeight":1}), tagNode))
            graph_db.create(rel(imgNode, "TAGGED", tagNode))

# define a function that returns a tag node
def getTagNode(tag):
    tags = graph_db.get_or_create_index(neo4j.Node, "Tags")
    t = tags.get_or_create("tagName", tag, {"tagName": tag})
    t.add_labels("TAG")
    return t 


#############################################################
##################### functions #############################
#############################################################
#call functions from scraper that return things with scraper.blah
# def createGraph(memeDict):
    # #make a function to create graph db
    # #create a list of nodes

    # images = []
    # tags = []
    # for img in memeDict:
    #     #so this part is working properly as it has added images notes to the 
    #     imgNode = Img(imgSrc=img, aggregateImgWeight=0).save()
    #     imgNode.refresh()
        
    #     for tag in memeDict[img]:
    #         #check if tag exists already in the database (this part is not working)
    #         if not Tag.index.search(tagName=tag):
    #                  #created the tag 
    #             tagNode = Tag(tagName=tag).save()
    #             tagNode.refresh()
    #             print tagNode
    #             #connect it to the img with the relationship (write this one as a cypher query)
    #             query = "MATCH (i:'{imgNode}'), (t:'{tagNode}') CREATE (i)-[r:TAGGED]->(t) RETURN r"
    #             params = {'imgNode': dir(imgNode.imgIndex), 'tagNode':tagNode.tagName}
    #             print params
    #             taggedRelationship = cypher.execute(graph_db, query, params)
    #             print taggedRelationship

         
    #         else:
    #             query = "MATCH ()-[r:TAGGED]-() return r"
    #             taggedRelationship = cypher.execute(graph_db, query)
    #             print "This is the tagged relationship[0]", taggedRelationship[0]
    #             # cypher_query.append(query, params)
    #             #params = dictionary of parameters (properties)
    #             # taggedRelationship.aggregateImgTagWeight += 1
    #             # taggedRelationship.commit
    # return "The createGraph function ran! Check DB to see if it worked."



def main():
    urls = ['http://icanhas.cheezburger.com/tag/dogs/', 
        'http://icanhas.cheezburger.com/tag/cats/',
        'http://roflrazzi.cheezburger.com/history'] 

    """In case we need this for something."""
    memeDict = scraper.listOfDictsOfMemes(urls)
    createImgNode(memeDict)

if __name__ == "__main__":
    main()
