from py2neo import neo4j
from py2neo import node, rel, ogm
from py2neo import cypher
from random import randint
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
    """Description: Creates and lables tag nodes if it doesn't already exist
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

def getRandomImgUrl():
    """ Description: Returns a random image
        Params: unknown
        Returns: image url """
    # randNode = graph_db.node(randint(2000, 3000))
    randNodeList = []
    for num in range(100):
        randNodeList.append(graph_db.node(randint(2000, 2300)))

    for randNode in randNodeList:
        if not randNode.exists:
            continue
        randProperties = randNode.get_properties()
        imgUrl = randProperties.get("imgSrc")
        if str(type(imgUrl)) == "<type 'unicode'>":
            nodeId = randNode._id
            return {"nodeId" : nodeId, "imgUrl": imgUrl}
    return getRandomImgUrl()
    
def findsTagsByImg(imgDict):
    """ Description: Finds all related tags for each image
        Params: imgDict, dictionary of img node id's and img urls
        Returns: list of all related tags for that image """
        
    imgNodeId = imgDict.get("nodeId") 
    imgNode = graph_db.node(imgNodeId)
    tagRelList = list(graph_db.match(start_node=imgNode))
    tagList = []
    for tagRel in tagRelList:
        tagNode = tagRel.end_node
        tagProperties = tagNode.get_properties()
        tagName = tagProperties.get("tagName")
        tagList.append(tagName)
    return tagList

#############################################################
##################### functions #############################
#############################################################


def main():
    urls = ['http://icanhas.cheezburger.com/tag/dogs/', 
        'http://icanhas.cheezburger.com/tag/cats/',
        'http://roflrazzi.cheezburger.com/history'] 

    """In case we need this for something."""
    # memeDict = scraper.listOfDictsOfMemes(urls)
    # createImgNode(memeDict)
    ImgDict = getRandomImgUrl();
    print findsTagsByImg(ImgDict)

if __name__ == "__main__":
    main()
