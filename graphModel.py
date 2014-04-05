from py2neo import neo4j
from py2neo import node, rel, ogm
from py2neo import cypher
import random
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
    """Description: Creates img nodes and assigns appropriate tagged 
                    relationships to tag nodes.
       Param: memeDict, dictionary, keys are urls and values are tags
       Returns: None"""
    urls = memeDict.keys()
    for url in urls:
        imgIndex = graph_db.get_or_create_index(neo4j.Node, "Img")

        imgNode = imgIndex.get_or_create("imgSrc", url, {"imgSrc":url, "aWeight":0})
        print "this should be an img node: ", imgNode
        imgNode.add_labels("IMG")

        for tag in memeDict[url]:
            tagNode = getTagNode(tag)
            graph_db.create(rel(imgNode, ("TAGGED", {"aWeight": tagNode[1]}), tagNode[0][0]))


def updateOrCreateTagged(memeDict):
    """ Description:
        Params: memeDict, dictionary, keys are urls and values are tags
        Returns: None """

    #check to see if the image exists
    urls = memeDict.keys()
    for url in urls:
        pImg = graph_db.get_indexed_node("Img", "imgSrc", url)
        print "This should be an indexed img node: ", pImg
        #this is working right now
        tags = memeDict[url]
        if str(type(pImg)) != "<type 'NoneType'>":
        #if so check to see if the tag exists
            
            print "This should be a list", tags
            for tag in memeDict[url]:
                tagName =  tagsExist([tag])


                if len(tagName) > 0:
                    pTagNode = graph_db.get_indexed_node("Tags", "tagName", tagName[0])                    
                    print "This should be an existing tag: ", pTagNode
                #if so check to see if there's a relationship
                    pRel = graph_db.match_one(start_node=pImg, rel_type="TAGGED", end_node=pTagNode)
                    print "This should find the relationship or return none: ", pRel
                    #if so increment rel aweight
                    if str(type(pRel)) != "<type 'NoneType'>":
                        getOldWeight = pRel.get_properties()
                        oldWeight = getOldWeight.get("aWeight")
                        newWeight = oldWeight + 1
                        relProp = pRel.update_properties({"aWeight": newWeight})
                        print "This should be the old weight: ", oldWeight
                    #else 
                    else:
                        #create a relationship 
                        newRel = graph_db.create(rel(pImg, ("TAGGED", {"aWeight": 1}), pTagNode))
                        print "Hopefully this is a relationship: ", newRel                            
                        # and add the default weight
                #else 
                else:
                    #create tag node
                    makeNewTagNode = getTagNode(tag)
                    newTagNode = graph_db.get_indexed_node("Tags", "tagName", tag)
                    #and then create a relationship
                    newRel = graph_db.create(rel(pImg, ("TAGGED", {"aWeight": 1}), newTagNode))
            #else
        else:
            #create image node
            newImgNode = createImgNode({url : tags})
            print "this should be a new img node:", newImgNode
    

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
        randNodeList.append(graph_db.node(random.randint(2000, 2300)))

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

def retrieveImages(tag):
    """ Description: Finds all images related to a specific tag and 
                    returns a dictionary of image urls with aggregate 
                    image weights.
        Params: tag, string that describes image
        Returns: dictionary, img url keys with aggregate weight values"""
    #find the tag node by tag name
    tags = graph_db.get_or_create_index(neo4j.Node, "Tags")
    tagNode = tags.get("tagName", tag)
    if tagNode != []:
        # tagNode = tags.get_indexed_node("")
        #find the TAGGED relationships
        rels = tagNode[0].match()
        imgNodeDict = {}
        #loop through the relationships 
        for rel in rels:
            #save the image urls and related weights to a dictionary
            imgNode = rel.start_node
            relWeight = rel.get_properties().get("aWeight")
            imgNodeDict[imgNode.get_properties().get("imgSrc")] = relWeight
        return imgNodeDict
        
    else:
        return False

#TODO: Make a funciton the sees if the tags are actually in the database 
#that returns a list of acceptable tags
def tagsExist(possibleTags):
    """ Description: Checks to see if the tags are actually in the database
        Params: list of tags from user input
        Returns: list of existing tags"""
    #loop through the possible tags
    existingTags = []
    for tag in possibleTags:
        strTag = str(tag)
        print "This is a strTAg", strTag
        #if the tag is in the database
        pTag = graph_db.get_indexed_node("Tags", "tagName", strTag)
        print "This is PTAG:", pTag
        if str(type(pTag)) != "<type 'NoneType'>":
            existingTags.append(tag)
            #add it to the list of existing tags
    return existingTags 

def retrievePerfectMemes(listOfTags):
    """ Description: Retrieve all urls for every image associated 
                with every tag accounting for all aggregate weights
        Params: list of tags that have been verified to exist using 
                the tagsExist function
        Returns: list of urls with repititions accounting for weights 
        of all given tags"""

    #get all the images for every tag in the list of tags- for loop
    listOfMemeDicts = []
    cleanTags = tagsExist(listOfTags)
    #loop through the tags in the list of tags
    for tag in cleanTags:
        #get the dictionary for each tag in the list
        memeDict = retrieveImages(tag)
        #add the dict to the list of dicts
        listOfMemeDicts.append(memeDict)

    allTheMemeDicts = {}
    # loop through the list of dicts
    for memeD in listOfMemeDicts:
        #iterate through that dict
        for imgUrl, imgWeight in memeD.iteritems():
            #if the image in the dict is already in allTheMemeDicts
            if imgUrl in allTheMemeDicts:
                #add the two weights together
                totalWeight = allTheMemeDicts[imgUrl] + imgWeight
                allTheMemeDicts[imgUrl] = totalWeight
            #otherwise add the img url and weight to allTheMemeDicts
            else:
                allTheMemeDicts[imgUrl]= imgWeight
    
    allTheMemeUrls = []
    #iterate over allTheMemeDicts
    for imgUrl, imgWeight in allTheMemeDicts.iteritems():
        #add one url to allTheMemeUrls for every weight
        allTheMemeUrls.extend([imgUrl] * imgWeight)
    return allTheMemeUrls


def servePerfectMemes(listOfTags):
    """ Description: Selects the perfect meme accounting 
                    for all tags and all associated weights
        Params: Takes a list of tags from user input
        Returns: list of three image urls accounting for all 
                    tags and associated tag weights"""
    allTheMemeUrls = retrievePerfectMemes(listOfTags)
    if len(allTheMemeUrls) != 0:
        threeTaggedImages = []
        #add three distinct random images accounting for weight
        img = random.choice(allTheMemeUrls)
        while len(threeTaggedImages) != 3:
            if img not in threeTaggedImages:
                threeTaggedImages.append(img)
            else:
                img = random.choice(allTheMemeUrls)
    else:
        return False
    #return list of three images
    return threeTaggedImages  



#############################################################
##################### main function #########################
#############################################################


def main():
    urls = ['http://icanhas.cheezburger.com/tag/dogs/', 
        'http://icanhas.cheezburger.com/tag/cats/',
        'http://roflrazzi.cheezburger.com/history',
        'http://icanhas.cheezburger.com/tag/cute',
        'http://failblog.cheezburger.com/tag/fail-nation',
        'http://geek.cheezburger.com/tag/funny',
        'http://geek.cheezburger.com/tag/Sad',
        'http://geek.cheezburger.com/tag/data'
        ] 

    """In case we need this for something."""
    # memeDict = scraper.listOfDictsOfMemes(urls)
    # createImgNode(memeDict)
    # ImgDict = getRandomImgUrl();
    # findsTagsByImg(ImgDict)

if __name__ == "__main__":
    main()
