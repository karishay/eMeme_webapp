from py2neo import neo4j
from py2neo import node, rel, ogm
from py2neo import cypher
import scraper

graph_db = neo4j.GraphDatabaseService("http://localhost:7476/db/data/")
store = ogm.Store(graph_db)

#############################################################
####### functions to create Nodes and Relationships #########
#############################################################
#check to see if user token is in the database
def logInOrCreateUser(access_token):
    users = graph_db.get_or_create_index(neo4j.Node, "Users")
    perhapsUser = users.get("access_token", access_token)
    if len(perhapsUser) == 1:
        return access_token
    else:
        user = users.get_or_create("access_token", access_token, {
            "access_token": access_token
            })
        user.add_labels("USER")
        return access_token

def createImgNode(memeDict):
    """Description: Creates img nodes and assigns appropriated tagged 
                    relationships to tag nodes.
       Param: memeDict, dictionary, keys are urls and values are tags
       Returns: None"""

    urls = memeDict.keys()
    for url in urls:
        imgNode, = graph_db.create({"imgSrc":url, "aWeight":0})
        imgNode.add_labels("IMG")

        for tag in memeDict[url]:
            tagNode = getTagNode(tag)
            graph_db.create(rel(imgNode, ("TAGGED", {"aWeight": tagNode[1]}), tagNode[0][0]))

def getTagNode(tag):
    """Description: Creates and lables tag nodes 
       Param: tag, string, characteristic of image
       Returns: a tuple with a node in list form and a weight integer"""

    tags = graph_db.get_or_create_index(neo4j.Node, "Tags")
    aWeight = 1
    #define the tag query
    perhapsTag = tags.get("tagName", tag)
    if len(perhapsTag) == 1:
        perhapsProp = perhapsTag[0]._properties
        pTagName = perhapsProp.get("tagName")
        aWeight += 1
        t = perhapsTag
    else:
        t = tags.get_or_create("tagName", tag, {"tagName": tag})
        t.add_labels("TAG")
        t = [t]
    return (t, aWeight)


#############################################################
##################### functions #############################
#############################################################


def main():
    urls = ['http://icanhas.cheezburger.com/tag/dogs/', 
        'http://icanhas.cheezburger.com/tag/cats/',
        'http://roflrazzi.cheezburger.com/history'] 

    """In case we need this for something."""
    memeDict = scraper.listOfDictsOfMemes(urls)
    createImgNode(memeDict)

if __name__ == "__main__":
    main()
