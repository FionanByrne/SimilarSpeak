from syllables.trigram_model import pronouncable
from syllables.word_distance import WordDistance
from syllables.phoneme_word import PhonemeWord
from syllables.syllabifier import Syllabifier
from syllables.text_mapper import phoneme_to_text, nonsense_to_text
from itertools import chain, product
import operator
import sys


# def generate_1edits(phoneme_sylls, thresh=0.05):
#     if len(phoneme_sylls) == 1:  # 1-syllable word
#         return find_edits1(phoneme_sylls[0])
#     else:
#         similar_syllables = []
#         for syll in phoneme_sylls:
#             similar_syllables.append(find_edits1(syll))

#         sim_words = map(list, list(product(*similar_syllables)))
#         return (sim_words)


def consonant_edits(phonemes):
    cons = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N',
            'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
    splits = [(phonemes[:i], phonemes[i:]) for i in range(len(phonemes) + 1)]

    inserts = [L + c + R for L, R in splits for c in [[i] for i in cons]]

    replaces = [L + c + R[1:] for L, R in splits
                if R for c in [[i] for i in cons]]

    deletes = [L + R[1:] for L, R in splits if R]
    return (deletes + replaces + inserts)


def find_edits1(syll, change_onsets=True, change_codas=True, thresh=0.05):
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
    # Onset edits:
    if(change_onsets):
        onset_swaps = consonant_edits(onset)
        onset_edits = (o + vowel + coda for o in onset_swaps)
        syll_edits += list(filter(lambda syll:
                           pronouncable(syll, thresh), onset_edits))
    # Coda edits
    if(change_codas):
        coda_swaps = consonant_edits(coda)
        coda_edits = (onset + vowel + c for c in coda_swaps)
        syll_edits += list(filter(lambda syll:
                           pronouncable(syll, thresh), coda_edits))

    # if(change_codas and change_onsets):
    #     for o in onset_swaps:
    #         for c in coda_swaps:
    #             onset_coda_edit = o + vowel + c
    #             print(onset_coda_edit)
    #             if pronouncable(onset_coda_edit, thresh):
    #                 syll_edits += onset_coda_edit
    return syll_edits


def join_syllables(sylls_word):
    return list(chain.from_iterable(sylls_word))


def closest_edits1(word, n=100):
    """
    :param word: Syllabified phoneme word, e.g. : [["IH", "N"], ["T", "UW"]]
    :return: Dictionary of n generated nonsense words
    """
    word_joined = join_syllables(word)
    wd = WordDistance(word_joined)
    # print(f'FION4":{word}', file=sys.stderr)
    # sim_words = {}
    for pos, syll in enumerate(word):
        for syll_swap in find_edits1(syll):
            sim_sylls_word = word[:pos] + [syll_swap] + word[pos+1:]
            sim_phoneme_word = join_syllables(sim_sylls_word)
            word_dist = wd.word_dist(sim_phoneme_word)
            sim_word = phoneme_to_text(sim_phoneme_word)
            # print(f'FION2":{sim_sylls_word}', file=sys.stderr)
            if sim_word:
                valid_word = True
            else:
                valid_word = False
                sim_word = nonsense_to_text(sim_phoneme_word)

            # pw = PhonemeWord(sim_word)
            # sim_words[pw] = word_dist
            if word_joined != sim_phoneme_word:
                yield sim_word, str(sim_phoneme_word), word_dist, valid_word

    # return sim_words
    # Order sim_words by ascending distance
    # return dict(sorted(sim_words.items(), key=operator.itemgetter(1))[:n])


# TEST
# from syllabifier import Syllabifier
# x = closest_edits1([["D", "AW", "G"], ["ER"]], n=100)
# for k, v in x.items():
#     print(k, "==", v)
# print(f"Number of words generated = {len(x)}")
