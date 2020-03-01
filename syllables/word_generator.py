from trigram_model import pronouncable
import cmudict
import itertools
from syllabifier import Syllabifier


def generate_1edits(phoneme_sylls, thresh=0.02):
    """
    Generate pronouncable word 1 Levenshtein edit distance away

    :param phoneme_sylls: List of phonemes; e.g. [['M', 'EH'], ['N', 'IY']]
    :param thresh: Min conditional probability for accepting pronouncablity
    """
    if len(phoneme_sylls) == 1:  # 1-syllable word
        return find_1edits(phoneme_sylls)
    else:
        similar_words = []
        for i, syll in enumerate(phoneme_sylls):
            similar_words += phoneme_sylls[i]
            similar_words.append(find_1edits(syll))

        # Return cartesian product of generated syllables (as list of lists)
        return map(list, list(itertools.product(*similar_words)))


def edits1(syll, is_vowel):
    consonants = [i[0] for i in cmudict.phones() if not i[1] == ['vowel']]
    vowels = [i[0] for i in cmudict.phones() if i[1] == ['vowel']]
    splits = [(syll[:i], syll[i:]) for i in range(len(syll) + 1)]

    if(is_vowel):
        replaces = [[i] for i in vowels if [i] != syll]
        return (replaces)
    else:  # consonants
        inserts = [L + c + R for L, R in splits
                   for c in [[i] for i in consonants]]

        replaces = [L + c + R[1:] for L, R in splits
                    if R for c in [[i] for i in consonants]]

        deletes = [L + R[1:] for L, R in splits if R]

        return (deletes + replaces + inserts)


def find_1edits(syll, change_onset=True, change_coda=True, thresh=0.02):
    # Split syllable into (oneset, nucleus, coda)
    vowels = [i[0] for i in cmudict.phones() if i[1] == ['vowel']]
    vowel_i = list(map(lambda i: i in vowels, syll)).index(True)
    onset, nucleus, coda = syll[:vowel_i], [syll[vowel_i]], syll[vowel_i+1:]

    edits = []

    # Generate words by swapping out vowel
    nucleus_swaps = [onset + i + coda for i in edits1(nucleus, True)]
    edits += list(filter(lambda syll:
                         pronouncable(syll, thresh), nucleus_swaps))
    if(change_onset):
        onset_swaps = [i + nucleus + coda for i in edits1(onset, False)]
        edits += list(filter(lambda syll:
                      pronouncable(syll, thresh), onset_swaps))
    if(change_coda):
        coda_swaps = [onset + nucleus + i for i in edits1(coda, False)]
        edits += list(filter(lambda syll:
                      pronouncable(syll, thresh), coda_swaps))
    return ([syll] + edits)


def edits2(syll):
    "All edits that are two edits away from `syll`."
    return (e2 for e1 in edits1(syll) for e2 in edits1(e1))


# TODO
def syll_difference(p1, p2):
    return 0.1


# TEST
word = "rocket"
s = Syllabifier()
t1 = s.to_syllables(s.to_phoneme(word))

print("word = ", t1)
words = generate_1edits(t1)
for i in words:
    print(i)
