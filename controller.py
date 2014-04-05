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
    return render_template("login.html", name=name)

@app.route("/improveSuggestions", methods=["GET"])
def improveSuggestions():
    tag = request.form.get("tag")
    imgDictOne = graphModel.getRandomImgUrl()
    urlOne = imgDictOne.get("imgUrl")
    imgDictTwo = graphModel.getRandomImgUrl()
    urlTwo = imgDictTwo.get("imgUrl")
    tagListOne = graphModel.findsTagsByImg(imgDictOne)
    tagListTwo = graphModel.findsTagsByImg(imgDictTwo)

    return render_template('improveSuggestions.html', urlOne=urlOne, 
                                                    urlTwo=urlTwo, 
                                                    tagListOne=tagListOne, 
                                                    tagListTwo=tagListTwo)

#TODO: Make new route that handle added or clicked tags (send to db)
@app.route("/improveSuggestions", methods=["POST"])
def improveSuggestionsSave():
    tag = request.form.get("tagName")
    img = request.form.get("imgSrc")
    aWeight = 1
    graphModel.updateOrCreateTagged({img: [tag]})
    #get the tags from the previous page
    #change the weight of the tagged relationship

    #make an ajax call that removes the tag and tells the user they've added it
    return tag, img
#user request.form.get("tag") from ajax to send to DB 

@app.route("/findPerfectMeme", methods=["GET"])
def findPerfectMeme():
    name = "Shannon"
    userInput = request.args.get("tag")
    dirtyTags = userInput.split(" ") 
    tags = [tag.strip(" ,.!?'\"@#$%^&*()_-123456789~`{}[]").lower() for tag in dirtyTags]
    memeList = graphModel.servePerfectMemes(tags)
    if memeList == False:
        errorHandler = "Sorry, no memes match your input. Please try again!"
        return render_template('findPerfectMeme.html', name=name, memeList=memeList, errorHandler=errorHandler or "")
    return render_template('findPerfectMeme.html', name=name, memeList=memeList)

###some other stuff###
if __name__ == "__main__":
    app.run(debug=True)







