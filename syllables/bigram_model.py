import cmudict
from nltk import ngrams, TrigramCollocationFinder, BigramCollocationFinder
import pickle
import itertools
from syllabifier import Syllabifier


def create_model():
    """
    :param file_path: relative path to create conditional probabilities file
    """
    # syllable_split = nltk.word_tokenize(syllable)
    cond_probs_path = "syllables/data/cond_probs.p"

    # Frequency of all phonemes (initially 0)
    accepted_phonemes = [i[0] for i in cmudict.phones()]
    accepted_phonemes.append('<s>')
    accepted_phonemes.append('</s>')
    # unigrams_dict = dict([(char, 0) for char in accepted_phonemes])

    # Get list of all syllables
    syllabifier = Syllabifier()
    all_syllables = syllabifier.all_syllables()

    # Count and conditional probabilties of phoneme pairs
    # phoneme_pairs = list(permutations(accepted_phonemes, 2))
    # phoneme_pairs = [p for p in itertools.product(accepted_phonemes, repeat=2)]
    phoneme_tups = [p for p in itertools.product(accepted_phonemes, repeat=3)]
    # bigrams_dict = dict([(char, 0) for char in phoneme_pairs])
    # trigrams_dict = dict([(char, 0) for char in phoneme_tuples])
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

    pickle.dump(cond_probs_dict, open(cond_probs_path, "wb"))
    return


def pronouncable(syllable: str, thresh=0.001, verbose=False):
    """
    :param syllable: Input syllable
    :param file_path: relative path to create conditional probabilities file
    """
    # Load dictionary
    cond_probs_path = "syllables/data/cond_probs.p"
    cond_probs_dict = pickle.load(open(cond_probs_path, "rb"))
    consonants = [i[0] for i in cmudict.phones() if not i[1] == ['vowel']]
    if len(syllable) == 0:  # Emtpy Syllable
        return True
    if all(p in consonants for p in syllable):  # No vowel sounds
        return False
    else:
        syllable = ['<s>'] + syllable + ['</s>']
        trigrams = list(ngrams(syllable, 3))
        # Compute conditional probabilities for phoneme bigrams
        cond_probs = list(map(lambda tuple: cond_probs_dict[tuple], trigrams))

        if verbose:
            print(dict(zip(trigrams, cond_probs)))

        # Are all cond probs above threshold value
        return all(cond_prob > thresh for cond_prob in cond_probs)


# # TEST
create_model()
test_word = ['T', 'EY', 'S', 'T']
print(pronouncable(test_word, 0.01, True))
