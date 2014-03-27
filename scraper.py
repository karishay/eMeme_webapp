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
    allTags = []
    Ancestors = pq(memeBucket)
    for meme in Ancestors:
        meme = pq(meme)
        if meme("img"):
            Tags = []
            listOfTagsPerMeme = meme('.tags ul li')
            for tag in listOfTagsPerMeme:
                tagText = tag.text_content()
                Tags.append(tagText)
            allTags.append(Tags)
    return allTags


keys = findImages(allTheThings)
values = findTags(memeBucket)

dictOfMemes = dict(zip(keys, values))

print dictOfMemes

### # is ID
### . is Class
### a is TagName (the tagname <a>)