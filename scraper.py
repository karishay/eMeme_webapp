import requests
from lxml import html
from pyquery import PyQuery as pq

url = 'http://icanhas.cheezburger.com/tag/dogs/' 
r = requests.get(url)
q = pq(r.text)
#####################################################
##### SOME HOW MAKE THIS SHIT INTO FUNCITONS ########
#####################################################
filthyDoges = q('.post-asset-wrap .event-item-lol-image')

def dogeWash(filthyDoges):
    #Make a list of doges
    listOfDoges = []
    #Go through the dirty file of doge picturesfor doge in filthyDoge:     
    for doge in filthyDoges:
        #add the src of each doge to the list 
        listOfDoges.append(doge.get('src'))
    return listOfDoges


def findDogeTag(listOfDoges):
    dogeTags = []
    for doge in listOfDoges:
        #this is currently seeing the item in the list as a string instead of an object. transform it back into and object then traverse the tree
        dogeDaddy = doge.getparent()
        dogeAncestor = dogeDaddy.getparent().getparent().getparent().getchildren()[1]
        sisterDoge = dogeAncestor.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[0].getchildren()
        print sisterDoge

#   find the parent of the src

    #   locate the sibling tags of the src
#   extract the innerHTML of the tag links
#   happy dance
#   return the list of tags for that src
    return sisterDoge
    # grandAunt = parent.getparent().getparent().getparent().getchildren()[1]
# grandAunt.getchildren()[0].getchildren()[0].getchildren()[1].get("class")
# grandAunt.getchildren()[0].getchildren()[0].getchildren()[1].getchildren()[0].getchildren()


filthyDogeTags = q('.post-asset-wrap .unstyled')
listOfLists = []
#go through the dirty file of the list of lists
for links in filthyDogeTags:
    listOfTagsPerDoge = []
#   for each list in the list loop through that list
    for link in links:
        #extract the link from the list
        tag = link.text_content()

        #extract the inner html of the link and add to list       
        listOfTagsPerDoge.append(tag)

    #add list of tags to list of lists
    listOfLists.append(listOfTagsPerDoge)
print listOfLists


# keys = listOfDoges
# values = listOfLists

# dictOfMemes = dict(zip(keys, values))

# print dictOfMemes

### # is ID
### . is Class
### a is TagName (the tagname <a>)