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
def logInOrCreateUser(userProfileData):
    """ Description: Logs in user if existing, creates new user if not.
        Params:userProfileData is a list of data from google 
        plus to populate the user nodes
        Returns: user id string"""
        
    users = graph_db.get_or_create_index(neo4j.Node, "Users")
    perhapsUser = users.get("userId", userProfileData[0])
    print perhapsUser
    print len(perhapsUser)
    if len(perhapsUser) > 1:
        perhapsProp = perhapsUser[0]._properties
        pToken = perhapsProp.get("userId")
        return userProfileData
    else:
        user = users.get_or_create("userId", userProfileData[0], {
            "userId": userProfileData[0],
            "name": userProfileData[1],
            "gender": userProfileData[2],
            "language": userProfileData[3],
            "profileImg": userProfileData[4]
            })
        user.add_labels("USER")
        return userProfileData

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
