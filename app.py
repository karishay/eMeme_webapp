from flask import Flask, render_template, redirect, request, session, g, url_for, flash
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flask.ext.markdown import Markdown
import config
import os
#may not need the forms.... maybe?

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

###some other stuff###
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)