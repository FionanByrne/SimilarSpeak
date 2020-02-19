"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, request, jsonify

# local modules
import config


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


@connex_app.route("/search", methods=['POST'])
def search_word():
    word = request.form['word']
    distance = "0.0"
    if word:
        print(word)
        return jsonify({word: distance})

    return jsonify({'error': 'Missing Data!'})


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", debug=True)
