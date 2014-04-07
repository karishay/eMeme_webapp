eMeme - Meme Recommendation Engine
====================================

eMeme is a web app and chrome extension internet meme recommendation engine that 
uses machine learning and to find the best meme for any situation. The machine 
learning algorithm is powered by a Neo4j graph database using Py2neo to communicate 
with the Python microframework, Flask. The front end of the web app is built with 
Gumby, styled with Sass, and powered by javaScript and Jquery.
To populate the database, I created a webscraper using PyQuery. 

Demo gif of the eMeme chrome extension:
-------------------------------------------------

The eMeme chrome extension uses context menus to send a selection of text to be 
processed by the algorithm and returns an image in the reply box.

![eMeme Chrome Extension Demo](https://raw.githubusercontent.com/karishay/eMeme_webapp/master/eMemeExtensionDemo.gif)



Demo gif of the eMeme web app:
----------------------------------------

The eMeme web app uses google plus authentication for logging in and registration.


![eMeme Web App Demo](https://raw.githubusercontent.com/karishay/eMeme_webapp/master/eMemeWebAppDemo.gif)



Technologies Used:
-----------------
Back End:
* Neo4j/Cypher
* Python
* Flask/Jinja
* PyQuery
* Py2Neo


Front End:
* Sass/CSS
* HTML
* javaScript/jQuery
* Gumby
