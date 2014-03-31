import requests
from lxml import html
from pyquery import PyQuery as pq

urls = ['http://icanhas.cheezburger.com/tag/dogs/', 
        'http://icanhas.cheezburger.com/tag/cats/',
        'http://roflrazzi.cheezburger.com/history'] 

#####################################################
##### SOME HOW MAKE THIS SHIT INTO FUNCITONS ########
#####################################################

def findImages(pageBody):
    """This function returns all the memes on the page"""

    lolImages = pageBody('.event-item-lol-image')
    listOfImages = []
    for image in lolImages:
        listOfImages.append(image.get('src'))
    return listOfImages


def findTags(pageBody):
    """This function returns a list of tags"""
    memeBucket = pageBody('.post-asset-wrap')
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


#create a function that scrapes 
def listOfDictsOfMemes(urls):
    """This funciton returns a list of dictionaries 
    with meme img keys and associated tag values."""
    keys = []
    values = []
    for url in urls:        
        r = requests.get(url)
        pageBody = pq(r.text)
        keys.extend(findImages(pageBody))
        values.extend(findTags(pageBody))  
        
    dictOfMemes = dict(zip(keys, values))
    

    return dictOfMemes

### # is ID
### . is Class
### a is TagName (the tagname <a>)