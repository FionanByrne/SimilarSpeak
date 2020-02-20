"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template

# local modules
import config
import os
from config import db

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/

    :return:        the rendered template "home.html"
    """
    if os.path.exists("words.db"):
        os.remove("words.db")
    db.create_all()
    return render_template("home.html")


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", debug=True)
