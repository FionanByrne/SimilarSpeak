"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template

# local modules
import config
import os
import syllables.trigram_model
from config import db
import models
# import sys

# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")

# create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    Respond to browser url localhost:5000/

    :return:        the rendered template "home.html"
    """
    build_databases()
    return render_template("home.html")


def build_databases():
    if os.path.exists("data/words.db"):
        os.remove("data/words.db")
    db.create_all()
    syllables.trigram_model.create_model()


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", debug=True)
