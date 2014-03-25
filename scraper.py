import requests
from lxml import html
from pyquery import PyQuery as pq

url = 'http://icanhas.cheezburger.com/tag/dogs/' 
r = requests.get(url)
q = pq(r.text)

##### SOME HOW MAKE THIS SHIT INTO FUNCITONS ########
filthyDoges = q('.post-asset-wrap .event-item-lol-image')

#Make a list of doges
listOfDoges = []

#Go through the dirty file of doge picturesfor doge in filthyDoge:     
for doge in filthyDoges:
    #add the src of each doge to the list 
    listOfDoges.append(doge.get('src'))

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



### # is ID
### . is Class
### a is TagName (the tagname <a>)