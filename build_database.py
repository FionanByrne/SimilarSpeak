import os
from config import db
from models import Word

# Data to initialize database with
WORDS = [
    {"word_name": "ant"},
    {"word_name": "bat"},
    {"word_name": "cat"}
]


# Delete database file if it exists currently
if os.path.exists("words.db"):
    os.remove("words.db")

# Create the database
db.create_all()

# iterate over the WORDS structure and populate the database
for word in WORDS:
    w = Word(word_name=word.get("word_name"))
    db.session.add(w)

db.session.commit()
