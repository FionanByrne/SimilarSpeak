"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, request, jsonify


# local modules
import config
import sys

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
    return render_template("home.html")


# @connex_app.route("/search", methods=['POST'])
# def search():
#     name = request.form['name']
#     # distance = "0.0"
#     if name:
#         newName = name[::-1]
#         print('SUCCESS', file=sys.stdout)
#         return jsonify({'name': newName})

#     return jsonify({'error': 'Missing Data!'})


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", debug=True)
