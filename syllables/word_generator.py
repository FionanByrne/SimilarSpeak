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
    replaces = [L + c + R[1:] for L, R in splits if R for c in [[i] for i in consonants]]
    inserts = [L + c + R for L, R in splits for c in [[i] for i in consonants]]
    edits = deletes + replaces + inserts
    return list(filter(lambda e: pronouncable(e, 0.01), edits))


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# TODO
def syll_difference(p1, p2):
    return 0.1


# TODO
test_word = ['M', 'EH']
#print(edits1(test_word))
sylls = [['AH', 'T'], ['M', 'EH', 'T']]
# res = []
syll = ["K", "AH", "T"]
print(edits1(syll))
#res = list(filter(lambda edit: print(pronouncable(["AH", "T"], 0.01)), edits1(syll)))
#print(res)