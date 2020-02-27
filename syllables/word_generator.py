from bigram_model import pronouncable
import cmudict
from syllabifier import Syllabifier


def generate_1edits(phoneme_sylls, thresh=0.01):
    """
    Generate pronouncable word 1 Levenshtein edit distance away

    :param phoneme_sylls: List of phonemes; e.g. [['M', 'EH'], ['N', 'IY']]
    :param thresh: Min conditional probability for accepting pronouncablity
    """
    list = []
    for syll in phoneme_sylls:
        list += filter(lambda i: pronouncable(i, thresh), edits1(syll))
    return list


def edits1(word):
    consonants = [i[0] for i in cmudict.phones() if not i[1] == ['vowel']]
    vowels = [i[0] for i in cmudict.phones() if i[1] == ['vowel']]
    # phonemes = consonants + vowels  # All phonemes in arpabet
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [L + R[1:] for L, R in splits if R and R[0] not in vowels]
    replaces = [L + c + R[1:] for L, R in splits if R
                for c in [[i] for i in consonants]]
    inserts = [L + c + R for L, R in splits
               for c in [[i] for i in consonants]]
    return (deletes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# TODO
def syll_difference(p1, p2):
    return 0.1


# TEST
word = "trains"
s = Syllabifier()
syll = s.to_syllables(s.to_phoneme(word))[0]
# syll = ['T', 'R', 'AY', 'N', 'Z']
results = edits1(syll)
for res in results:
    if pronouncable(res, 0.001, False):
        print(res)

print("--------------------------------------")

test_word = ["T"]
print(" ".join(test_word), ":")
print(pronouncable(test_word, 0.001, True))
# res = list(filter(lambda edit: pronouncable(edit, 0.01)), edits1(syll)))
