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


#create more routes that actually get things from the 
#graphModel and sends them back to templates

    # http://localhost:5000/oauth2callback
###some other stuff###
if __name__ == "__main__":
    app.run(debug=True)