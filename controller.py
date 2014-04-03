from flask import Flask, render_template, redirect, request, session, g, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flask.ext.markdown import Markdown
import config
import graphModel

app = Flask(__name__)
app.config.from_object(config)

#adding markdown capability
Markdown(app)

### Routes live here: ###

#this is my landing page
@app.route("/")
def index():
    #query the db for the shiiiiiiit you need for this page
    #load the landing page
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    userId = request.form.get("userId")
    name = request.form.get("name")
    gender = request.form.get("gender")
    language = request.form.get("language")
    profileImg = request.form.get("profileImg")
    userProfileData = [userId, name, gender, language, profileImg]
    graphModel.logInOrCreateUser(userProfileData)
    #if they are logged in put their user id in the session
#get a token to print here by posting
#then talk to liz about assigning to a user and keeping in a session
    return render_template("login.html")

#TODO: make two different routes that return pertinent data to contstruct related pages
@app.route("/improveSuggestions", methods=["GET"])
def improveSuggestions():
    #TODO: get images at random from database and their associated tags
    tag = request.form.get("tag")
    imgDictOne = graphModel.getRandomImgUrl()
    urlOne = imgDictOne.get("imgUrl")
    imgDictTwo = graphModel.getRandomImgUrl()
    urlTwo = imgDictTwo.get("imgUrl")
    tagListOne = graphModel.findsTagsByImg(imgDictOne)
    tagListTwo = graphModel.findsTagsByImg(imgDictTwo)

    #TODO: build out the improveSuggestions.html jinja ajax insertion template
    return render_template('improveSuggestions.html', urlOne=urlOne, 
                                                    urlTwo=urlTwo, 
                                                    tagListOne=tagListOne, 
                                                    tagListTwo=tagListTwo)

#TODO: Make new route that handle added or clicked tags (send to db)
# @app.route()
#user request.form.get("tag") from ajax to send to DB 

@app.route("/findPerfectMeme", methods=["GET", "POST"])
def findPerfectMeme():
    #TODO: add functionality to return meme with db calls.
    #TODO: build out the findPerfectMeme.html jinja ajax insertion template
    return render_template('findPerfectMeme.html')

###some other stuff###
if __name__ == "__main__":
    app.run(debug=True)