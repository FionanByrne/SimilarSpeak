class PhonemeWord:
    def __init__(self, phoneme_word, text_word, valid_word):
        self.phoneme_word = phoneme_word
        self.text_word = text_word
        self.valid_word = valid_word

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.phoneme_word == other.phoneme_word
        )

    def __hash__(self):
        return 0

    def __repr__(self):
        return f"{self.phoneme_word}"

    def phoneme_word(self):
        return self.phoneme_word

    def text_word(self):
        return self.text_word

    def valid_word(self):
        return self.valid
