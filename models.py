from config import db, ma


class Word(db.Model):
    __tablename__ = "word"
    person_id = db.Column(db.Integer, primary_key=True)
    word_name = db.Column(db.String(32))
    distance = db.Column(db.Float)


class WordSchema(ma.ModelSchema):
    class Meta:
        model = Word
        sqla_session = db.session
