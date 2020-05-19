PRONOUNCIATION_THRESH = 0.03

from syllables.trigram_model import pronouncable
from syllables.word_distance import WordDistance
from syllables.phoneme_word import PhonemeWord
# from syllables.syllabifier import Syllabifier
from syllables.text_mapper import phoneme_to_text, nonsense_to_text
from itertools import chain
import operator
import sys


def consonant_edits(phonemes):
    cons = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N',
            'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
    splits = [(phonemes[:i], phonemes[i:]) for i in range(len(phonemes) + 1)]

    swaps = [L + c + R[1:] for L, R in splits if R for c in [[i] for i in cons]]

    deletes = [L + R[1:] for L, R in splits if R]

    inserts_pre = [[c] + phonemes for c in cons]
    inserts_post = [phonemes + [c] for c in cons]

    #print(f'x:{phonemes}', file=sys.stderr)

    return swaps, deletes, inserts_pre, inserts_post


def find_edits1(syll, change_onsets=True, change_codas=True, thresh=PRONOUNCIATION_THRESH):
    '''
    Find all possible pronouncable edits for given syllable
    Params:
    syll: input syllable, e.g. ["T", "EH", "S", "T"]
    change_onsets: determines if sound before vowel is kept
    change_codas: determines if sound after vowel is kept
    thresh: minimum threshold value
    '''
    # Split syllable into (oneset, vowel, coda)
    vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH',
              'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']

    vowel_i = list(map(lambda i: i in vowels, syll)).index(True)
    onset, vowel, coda = syll[:vowel_i], [syll[vowel_i]], syll[vowel_i+1:]
    vowels.remove(vowel[0])  # Remove original vowel from possible alternatives
    syll_edits = []

    # Vowel edits:
    vowel_swaps = [[i] for i in vowels if [i] != vowel[0]]
    vowel_edits = (onset + v + coda for v in vowel_swaps)

    syll_edits += list(filter(lambda syll:
                       pronouncable(syll, thresh), vowel_edits))

    onset_swaps, onset_deletes, onset_pre_inserts, onset_post_inserts = consonant_edits(onset)
    coda_swaps, coda_deletes, coda_pre_inserts, coda_post_inserts = consonant_edits(coda)

    # Onset edits:
    if(change_onsets):
        onset_edits = (onset_swaps + onset_deletes + onset_pre_inserts + onset_post_inserts)
        onset_combos = (o + vowel + coda for o in onset_edits)
        syll_edits += list(filter(lambda syll:
                           pronouncable(syll, thresh), onset_combos))
    # Coda edits
    if(change_codas):
        coda_edits = (coda_swaps + coda_deletes + coda_pre_inserts + coda_post_inserts)
        coda_combos = (onset + vowel + c for c in coda_edits)
        # for i in coda_combos:
        #     print(f'i:{i}', file=sys.stderr)
        syll_edits += list(filter(lambda syll:
                           pronouncable(syll, thresh), coda_combos))

    # if(change_codas and change_onsets):
    #     onset_edits = (onset_swaps + onset_deletes)
    #     coda_edits = (coda_swaps + coda_deletes)
    #     for o in onset_edits:
    #         for c in coda_edits:
    #             onset_coda_combo = o + vowel + c
    #             if pronouncable(onset_coda_combo, 0.05):
    #                 syll_edits.append(onset_coda_combo)

    print(f'Words:{syll_edits}', file=sys.stderr)
    return syll_edits


def join_syllables(sylls_word):
    return list(chain.from_iterable(sylls_word))


def closest_edits1(word_name, word_syllabified, n=100):
    """
    Params:
    word_name: input word in plain text, e.g. "into"
    word_syllabified: Syllabified word, e.g.: [["IH", "N"], ["T", "UW"]]
    n: max number of entires to search
    :return: Dictionary of n generated nonsense words
    """
    word_joined = join_syllables(word_syllabified)
    wd = WordDistance(word_joined)
    iteration = 0
    sim_words = {}
    for pos, syll in enumerate(word_syllabified):
        syll_edits = find_edits1(syll, thresh=PRONOUNCIATION_THRESH)
        for syll_swap in syll_edits:
            iteration += 1
            sim_sylls_word = word_syllabified[:pos] + [syll_swap] + word_syllabified[pos+1:]
            sim_phoneme_word = join_syllables(sim_sylls_word)
            print(f'Calculating word dist for {sim_phoneme_word} ({iteration}/{len(syll_edits)})', file=sys.stderr)
            word_dist = wd.word_dist(sim_phoneme_word)
            sim_word, valid_word = phoneme_to_text(sim_phoneme_word)
            # print(f'FION5:{sim_phoneme_word}', file=sys.stderr)
            if (sim_word != word_name):
                pw = PhonemeWord(sim_phoneme_word, sim_word, valid_word)
                sim_words[pw] = word_dist

    return sim_words


# TEST
# from syllabifier import Syllabifier
# x = closest_edits1([["D", "AW", "G"], ["ER"]], n=100)
# for k, v in x.items():
#     print(k, "==", v)
# print(f"Number of words generated = {len(x)}")
