from flask import Flask, render_template, redirect, request, session, g, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flask.ext.markdown import Markdown
import config
#may not need the forms.... maybe?
# import forms
import model

app = Flask(__name__)
app.config.from_object(config)

#adding markdown capability
Markdown(app)

### Routes live here: ###
@app.route("/")
def index():
    #query the db for the shiiiiiiit you need for this page
    #load the landing page
    return render_template("index.html")


# @app.route("/", methods=["POST"])
# def process_login():
#     email = request.form.get("email")
#     password = hash(request.form.get("password"))

#     user = model.authenticate(email, password)
#     if user:
#         session['user_id'] = user.id
# #        sessionUserId = model.Session.query(model.User).get(id)
#         return redirect(url_for("getMyRatings"))
#     else:
#         flash("Email or Password incorrect, grab your shit umbrella!")
#         return redirect(url_for("index"))

# @app.route("/register", methods=["GET"])
# def registerPage():
#     return render_template("register.html")

# @app.route("/register", methods=["POST"])
# def register():
#     #get all the things from the forms
#     email = request.form.get("email")
#     password = hash(request.form.get("password"))
#     passwordCheck = hash(request.form.get("password_verify"))
#     age = request.form.get("age")
#     zipcode = request.form.get("zipcode")
#     gender = request.form.get("gender")

#     #check if the passwords match
#     if password != passwordCheck:
#         flash("Learn how to type better, el suck!")
#         return redirect(url_for("registerPage"))

#     else:
#         if model.checkEmail(email):
#             flash("Biotch, you already gots an account.")
#             return redirect(url_for("registerPage"))
#         else:
#             newUser = model.User(email = email, 
#                            password = password, 
#                            age = age, 
#                            zipcode = zipcode, 
#                            gender = gender)
#             model.Session.add(newUser)
#             model.Session.commit()
#             return redirect(url_for("index"))
###some other stuff###
if __name__ == "__main__":
    app.run(debug=True)