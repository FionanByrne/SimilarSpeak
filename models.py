from config import db, ma
# from flask_wtf import FlaskForm


class Word(db.Model):
    __tablename__ = "word"
    word_id = db.Column(db.Integer, primary_key=True)
    word_name = db.Column(db.String(32))
    phonetic_name = db.Column(db.String(32))
    distance = db.Column(db.Float, default=0.5)
    valid_word = db.Column(db.String(32), nullable=False)


class WordSchema(ma.ModelSchema):
    class Meta:
        model = Word
        sqla_session = db.session
