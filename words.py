"""
This is the words module and supports all the REST actions for the
words data
"""

from flask import make_response, abort
from syllables.syllabifier import Syllabifier
from syllables.word_generator import closest_edits1
from itertools import chain
import time
from config import db
from models import Word, WordSchema
import sys
import os


def read_all():
    """
    This function responds to a request for /api/words
    with the complete lists of words

    :return:        json string of list of words
    """
    # Create the list of words from our data
    words = Word.query.order_by(Word.distance).all()

    # Serialize the data for the response
    word_schema = WordSchema(many=True)
    data = word_schema.dump(words)
    return data


def read_one(word_id):
    """
    This function responds to a request for /api/words/{word_id}
    with one matching word from words

    :param word_id:   Id of word to find
    :return:          word matching id
    """
    # Get the word requested
    word = Word.query.filter(Word.word_id == word_id).one_or_none()

    # Did we find a word?
    if word is not None:

        # Serialize the data for the response
        word_schema = WordSchema()
        data = word_schema.dump(word).data
        return data

    # Otherwise, nope, didn't find that word
    else:
        abort(
            404,
            "Word not found for Id: {word_id}".format(word_id=word_id),
        )


def create(word):
    """
    This function creates a new word in the words structure
    based on the passed in word data

    :param word:  word to create in words structure
    :returns:        201 on success, 406 on word exists
    """
    # print(f'SUCCESS{word}', file=sys.stdout)  # TODO
    word_name = word.get("word_name")

    existing_word = (
        Word.query.filter(Word.word_name == word_name)
        .one_or_none()
    )

    # Can we insert this word?
    if existing_word is None:

        # Create a word instance using the schema and the passed in word
        schema = WordSchema()
        new_word = schema.load(word, session=db.session).data

        # Add the word to the database
        db.session.add(new_word)
        db.session.commit()

        # Serialize and return the newly created word in the response
        data = schema.dump(new_word).data

        return data, 201

    # Otherwise, nope, word exists already
    else:
        abort(
            409,
            "Word {word_name} exists already".format(
                word_name=word_name
            ),
        )


def search(json_word):
    """
    This function searches for a word

    :param word:  word (json) to search in words structure
    :return:        201 on success, 406 on word exists
    """
    if os.path.exists("data/words.db"):
        os.remove("data/words.db")
    db.create_all()
    word_name = json_word.get("word_name").lower()
    print(f'Searching for similar words to {word_name}...', file=sys.stderr)
    syllab = Syllabifier()
    # Is input word defined?
    if syllab.is_valid(word_name):
        print(f'Word {word_name} is valid', file=sys.stderr)
        sylls_input = syllab.to_syllables(syllab.to_phoneme(word_name))
        schema = WordSchema()
        sim_words = []
        start = time.time()

        for phonemeword, dist in closest_edits1(word_name, sylls_input, 100).items():
            # string_sim_word = " ".join(list(chain.from_iterable(sim_word)))
            text_word = phonemeword.text_word
            phonetic_name = str(phonemeword.phoneme_word)
            valid_word = phonemeword.valid_word
            new_word = Word(word_name=text_word,
                            phonetic_name=phonetic_name,
                            distance=dist,
                            valid_word=valid_word)
            db.session.add(new_word)  # Add to words database
            sim_words.append(new_word)

        db.session.commit()

        # Serialize and return the newly created word in the response
        data = schema.dumps(sim_words, many=True)
        time_elapsed = time.time() - start
        print(f'EXECUTION_TIME: {time_elapsed // 60: .2f} mins \
             {time_elapsed % 60: .2f} seconds', file=sys.stderr)
        return data, 201

    # Otherwise, word does not exist
    else:
        abort(
            409,
            "Word {word_name} undefined".format(
                word_name=word_name
            ),
        )


def update(word_id, word):
    """
    This function updates an existing word in the words structure
    Throws an error if a word with the name we want to update to
    already exists in the database.

    :param word_id:   Id of the word to update in the words structure
    :param word:      word to update
    :return:            updated word structure
    """
    # Get the word requested from the db into session
    update_word = Word.query.filter(
        Word.word_id == word_id
    ).one_or_none()

    # Try to find an existing word with the same name as the update
    word_name = word.get("word_name")

    existing_word = (
        Word.query.filter(Word.word_name == word_name)
        .one_or_none()
    )

    # Are we trying to find a word that does not exist?
    if update_word is None:
        abort(
            404,
            "Word not found for Id: {word_id}".format(word_id=word_id),
        )

    # Would our update create a duplicate of another word already existing?
    elif (
        existing_word is not None and existing_word.word_id != word_id
    ):
        abort(
            409,
            "Word {word_name} exists already".format(
                word_name=word_name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in word into a db object
        schema = WordSchema()
        update = schema.load(word, session=db.session).data

        # Set the id to the word we want to update
        update.word_id = update_word.word_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated word in the response
        data = schema.dump(update_word).data

        return data, 200


def delete(word_id):
    """
    This function deletes a word from the words structure

    :param word_id:   Id of the word to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the word requested
    word = Word.query.filter(Word.word_id == word_id).one_or_none()

    # Did we find a word?
    if word is not None:
        db.session.delete(word)
        db.session.commit()
        return make_response(
            "Word {word_id} deleted".format(word_id=word_id), 200
        )

    # Otherwise, word not found
    else:
        abort(
            404,
            "Word not found for Id: {word_id}".format(word_id=word_id),
        )
