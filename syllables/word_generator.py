import cmudict
import itertools
from collections import OrderedDict
from trigram_model import pronouncable
from syllabifier import Syllabifier
from word_distance import WordDistance


def generate_1edits(phoneme_sylls, thresh=0.015):
    """
    Generate pronouncable word 1 Levenshtein edit distance away

    :param phoneme_sylls: List of phonemes; e.g. [['M', 'EH'], ['N', 'IY']]
    :param thresh: Min conditional probability for accepting pronouncablity
    """
    if len(phoneme_sylls) == 1:  # 1-syllable word
        return find_edits1(phoneme_sylls[0])
    else:
        similar_syllables = []
        for syll in phoneme_sylls:
            similar_syllables.append(find_edits1(syll))

        # Return cartesian product of generated syllables (as list of lists)
        sim_words = map(list, list(itertools.product(*similar_syllables)))
        return (sim_words)


def consonant_edits(phonemes):
    cons = ['B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N',
            'NG', 'P', 'R', 'S', 'SH', 'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH']
    splits = [(phonemes[:i], phonemes[i:]) for i in range(len(phonemes) + 1)]

    inserts = [L + c + R for L, R in splits for c in [[i] for i in cons]]

    replaces = [L + c + R[1:] for L, R in splits
                if R for c in [[i] for i in cons]]

    deletes = [L + R[1:] for L, R in splits if R]
    return (deletes + replaces + inserts)


def find_edits1(syll, change_onsets=True, change_codas=True, thresh=0.015):
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
    syll_edits += list(filter(lambda syll: pronouncable(syll, thresh), vowel_edits))
    # Onset edits:
    if(change_onsets):
        onset_swaps = consonant_edits(onset)
        onset_edits = (o + vowel + coda for o in onset_swaps)
        syll_edits += list(filter(lambda syll: pronouncable(syll, thresh), onset_edits))
    # Coda edits
    if(change_codas):
        coda_swaps = consonant_edits(coda)
        coda_edits = (onset + vowel + c for c in coda_swaps)
        syll_edits += list(filter(lambda syll: pronouncable(syll, thresh), coda_edits))

    # if(change_codas and change_onsets):
    #     for o in onset_swaps:
    #         for c in coda_swaps:
    #             onset_coda_edit = o + vowel + c
    #             print(onset_coda_edit)
    #             if pronouncable(onset_coda_edit, thresh):
    #                 syll_edits += onset_coda_edit
    return syll_edits


def closest_edits(word):
    wd = WordDistance(word)
    sim_words = {}
    for pos, syll in enumerate(word):
        print(pos, syll)
        for syll_swap in find_edits1(syll):
            print(syll_swap)
            sim_word = word[:pos] + [syll_swap] + word[pos+1:]
            print(sim_word)
            word_dist = wd.word_dist(sim_word)
            print(word_dist)
            sim_words[sim_word] = word_dist
    # Order sim_words by ascending distance
    sim_words = {k: v for k, v in sorted(sim_words.items(),
                                         key=lambda item: item[1])}
    return sim_words


def find_edits2(syll):
    "All edits that are two edits away from syll"
    return [e2 for e1 in find_edits1(syll) for e2 in find_edits1(e1)]


# TEST
w1 = "cat"
w2 = "cats"
s = Syllabifier()
t1 = s.to_syllables(s.to_phoneme(w1))
t2 = s.to_syllables(s.to_phoneme(w2))

x = closest_edits([["K", "AE", "T"], ["ER"]])
for i in x:
    print(i)

# print("syll = ", t1)
# res1 = find_edits1(t1[0])
# for i in res1:
#     print(i)
# print(len(res1))
