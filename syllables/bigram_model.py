import cmudict
from nltk import ngrams
import nltk
from itertools import permutations
from syllabifier import Syllabifier


def pronouncable(syllable: str, thresh):
    """
    :param syllable: Syllable to test, eg: "AH K T"
    :param thresh: Minimum acceptable value for bigram conditional prob
    :returns: True if syllable is pronouncable
    """
    #syllable_split = nltk.word_tokenize(syllable)

    # Frequency of all phonemes (initially 0)
    accepted_phonemes = [i[0] for i in cmudict.phones()]
    unigramsDict = dict([(char, 0) for char in accepted_phonemes])

    # Count and conditional probabilties of phoneme pairs
    phoneme_pairs = list(permutations(accepted_phonemes, 2))
    bigramsDict = dict([(char, 0) for char in phoneme_pairs])
    condProbsDict = dict([(char, 0) for char in phoneme_pairs])

    # Get list of all syllables
    syllabifier = Syllabifier()
    all_syllables = syllabifier.all_syllables

    for _syll in all_syllables:
        # Count unigrams (phonemes)
        for phoneme in _syll:
            unigramsDict[phoneme] += 1

        # Count bigrams: {"AH T" : 1, "AH K" : 3, ...}
        bigrams = list(ngrams(_syll, 2))
        for bigram in bigrams:
            if bigram in bigramsDict:
                bigramsDict[bigram] += 1
            else:
                bigramsDict[bigram] = 1

    # Find conditional probability for each phoneme bigram in syllable
    for p1, p2 in bigramsDict:
        count = bigramsDict[(p1, p2)]
        if unigramsDict[p1] != 0:
            cProb = count*1.0 / unigramsDict[p1]
        else:
            cProb = 0.0
        condProbsDict[(p1, p2)] = cProb

    consonants = [i[0] for i in cmudict.phones() if not i[1] == ['vowel']]

    if len(syllable) == 0:  # Emtpy Syllable
        return True
    if all(p in consonants for p in syllable):  # No vowel sounds
        return False
    else:
        bigrams = list(ngrams(syllable, 2))
        # Compute conditional probabilities for phoneme bigrams
        cond_probs = list(map(lambda pair: condProbsDict[pair], bigrams))
        # Are all cond probs above threshold value
        return all(cond_prob > thresh for cond_prob in cond_probs)
