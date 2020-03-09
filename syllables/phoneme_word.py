from itertools import chain


class PhonemeWord:
    def __init__(self, sylls_word):
        self.sylls_word = sylls_word
        self.phones = " ".join(list(chain.from_iterable(self.sylls_word)))
        self.valid = False

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.phoneme_word == other.phoneme_word
        )

    def __hash__(self):
        return 0

    def __repr__(self):
        return f"{self.phoneme_word}"
