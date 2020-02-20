import os
from config import db
from models import Word


def build_database():
    # Data to initialize database with
    WORDS = [
        {"word_name": "word1", "distance": 0.5},
        {"word_name": "word2", "distance": 0.5},
        {"word_name": "word3", "distance": 0.5}
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
