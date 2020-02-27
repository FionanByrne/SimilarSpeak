import cmudict
from nltk import ngrams
import pickle
from itertools import permutations
from syllabifier import Syllabifier


def create_model():
    """
    :param file_path: relative path to create conditional probabilities file
    """
    # syllable_split = nltk.word_tokenize(syllable)
    cond_probs_path = "syllables/data/cond_probs.p"

    # Frequency of all phonemes (initially 0)
    accepted_phonemes = [i[0] for i in cmudict.phones()]
    unigrams_dict = dict([(char, 0) for char in accepted_phonemes])

    # Count and conditional probabilties of phoneme pairs
    phoneme_pairs = list(permutations(accepted_phonemes, 2))
    bigrams_dict = dict([(char, 0) for char in phoneme_pairs])
    cond_probs_dict = dict([(char, 0) for char in phoneme_pairs])

    # Get list of all syllables
    syllabifier = Syllabifier()
    all_syllables = syllabifier.all_syllables

    for _syll in all_syllables:
        # Count unigrams (phonemes)
        for phoneme in _syll:
            unigrams_dict[phoneme] += 1

        if(len(_syll) < 2):
            continue

        # Count bigrams: {"AH T" : 1, "AH K" : 3, ...}
        bigrams = list(ngrams(_syll, 2))
        for bigram in bigrams:
            if bigram in bigrams_dict:
                bigrams_dict[bigram] += 1
            else:
                bigrams_dict[bigram] = 1

    # Phoneme followed by same phoneme has zero probability
    for _symbol in [i[0] for i in cmudict.phones()]:
        bigrams_dict[(_symbol, _symbol)] = 0

    # Find conditional probability for each phoneme bigram in syllable
    for p1, p2 in bigrams_dict:
        count = bigrams_dict[(p1, p2)]
        if unigrams_dict[p1] != 0:
            cProb = count*1.0 / unigrams_dict[p1]
        else:
            cProb = 0.0
        cond_probs_dict[(p1, p2)] = cProb

    pickle.dump(cond_probs_dict, open(cond_probs_path, "wb"))
    return


def pronouncable(syllable: str, thresh=0.001):
    """
    :param syllable: Input syabble
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
        bigrams = list(ngrams(syllable, 2))
        # Compute conditional probabilities for phoneme bigrams
        cond_probs = list(map(lambda pair: cond_probs_dict[pair], bigrams))

        # Are all cond probs above threshold value
        return all(cond_prob > thresh for cond_prob in cond_probs)


# # TEST
# create_model()
# result = pronouncable(["T", "AH", "T", "K"])
# print(result)

