import requests
from pyquery import PyQuery as pq

url = 'http://icanhas.cheezburger.com/tag/dogs/' 

r = requests.get(url)

q = pq(r.text)

doge = q('.post-asset-inner a')

print doge


### # is ID
### . is Class
### a is TagName (the tagname <a>)