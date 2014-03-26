import requests
from lxml import html
from pyquery import PyQuery as pq

url = 'http://icanhas.cheezburger.com/tag/dogs/' 
r = requests.get(url)
allTheThings = pq(r.text)

#####################################################
##### SOME HOW MAKE THIS SHIT INTO FUNCITONS ########
#####################################################

memeBucket = allTheThings('.post-asset-wrap')

def findImages(allTheThings):
    """This function returns all the memes on the page"""

    lolImages = allTheThings('.event-item-lol-image')
    listOfImages = []
    for image in lolImages:
        listOfImages.append(image.get('src'))
    return listOfImages


def findTags(memeBucket):
    """This function returns a list of """
    allDogTags = []
    Ancestors = pq(memeBucket)
    for doge in Ancestors:
        doge = pq(doge)
        if doge("img"):
            dogeTags = []
            listOfTagsPerDoge = doge('.tags ul li')
            for tag in listOfTagsPerDoge:
                tagText = tag.text_content()
                dogeTags.append(tagText)
            allDogTags.append(dogeTags)
    return allDogTags
 


# listOfLists = []
# #go through the dirty file of the list of lists
# for links in filthyDogeTags:
#     listOfTagsPerDoge = []
# #   for each list in the list loop through that list
#     for link in links:
#         #extract the link from the list
#         tag = link.text_content()

#         #extract the inner html of the link and add to list       
#         listOfTagsPerDoge.append(tag)

#     #add list of tags to list of lists
#     listOfLists.append(listOfTagsPerDoge)
# print listOfLists


keys = findImages(allTheThings)
values = findTags(memeBucket)

dictOfMemes = dict(zip(keys, values))

print dictOfMemes

### # is ID
### . is Class
### a is TagName (the tagname <a>)