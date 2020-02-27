import cmudict
from nltk import ngrams, TrigramCollocationFinder, BigramCollocationFinder
import pickle
import itertools
from syllabifier import Syllabifier

COND_PROBS_PATH = "syllables/data/cond_probs.p"


def create_model():
    """
    :param file_path: relative path to create conditional probabilities file
    """
    # syllable_split = nltk.word_tokenize(syllable)

    # Frequency of all phonemes (initially 0)
    accepted_phonemes = [i[0] for i in cmudict.phones()]
    accepted_phonemes.append('<s>')
    accepted_phonemes.append('</s>')

    # Get list of all syllables: ["<s>", "AH", "</s>", "<s>", "T", ...]
    syllabifier = Syllabifier()
    all_syllables = syllabifier.all_syllables()

    # Count conditional probabilties of phoneme tuples
    phoneme_tups = [p for p in itertools.product(accepted_phonemes, repeat=3)]
    tcf = TrigramCollocationFinder.from_words(all_syllables)
    bcf = BigramCollocationFinder.from_words(all_syllables)
    tri_dict = dict(sorted(tcf.ngram_fd.items(), key=lambda t: (-t[1], t[0])))
    bi_dict = dict(sorted(bcf.ngram_fd.items(), key=lambda t: (-t[1], t[0])))

    cond_probs_dict = dict([(char, 0) for char in phoneme_tups])

    for t in tri_dict:
        p1, p2, p3 = t[0], t[1], t[2]
        tri_count = tri_dict[t]
        bi_count = bi_dict[(p1, p2)]
        if bi_count != 0:
            cond_prob = tri_count * 1.0 / bi_count
        else:
            cond_prob = 0.0
        cond_probs_dict[(p1, p2, p3)] = cond_prob

    pickle.dump(cond_probs_dict, open(COND_PROBS_PATH, "wb"))
    return


def pronouncable(syllable: str, thresh=0.001, verbose=False):
    """
    :param syllable: Input syllable, eg: ['T', 'EH', 'S', 'T']
    :param thresh: minimum conditional prob for all tuples in syllable
    """
    cond_probs_dict = pickle.load(open(COND_PROBS_PATH, "rb"))
    consonants = [i[0] for i in cmudict.phones() if not i[1] == ['vowel']]
    if len(syllable) == 0:  # Emtpy Syllable
        return True
    if all(p in consonants for p in syllable):  # No vowel sounds
        return False
    else:
        syllable = ['<s>'] + syllable + ['</s>']
        trigrams = list(ngrams(syllable, 3))
        # Get conditional probabilities for phoneme trigram
        cond_probs = list(map(lambda tuple: cond_probs_dict[tuple], trigrams))

        if verbose:
            print(dict(zip(trigrams, cond_probs)))

        # Are all cond probs above threshold value
        return all(cond_prob > thresh for cond_prob in cond_probs)


# # TEST
# create_model()
# t1 = ['T', 'EY', 'S', 'T']
# t2 = ['T', 'S', 'T']
# t3 = ['T', 'EY']
# t4 = ['OW']
# print(pronouncable(t1, 0.01, True))
# print(pronouncable(t2, 0.01, True))
# print(pronouncable(t3, 0.01, True))
# print(pronouncable(t4, 0.01, True))
