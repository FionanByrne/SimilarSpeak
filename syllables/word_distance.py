import pandas as pd
import numpy as np
from syllabifier import Syllabifier
import itertools

CONSONANTS_MATRIX_FILE = "bailey_consonants.csv"
VOWEL_MATRIX_FILE = "bailey_vowels.csv"


class WordDistance:
    vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH',
              'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW']

    def __init__(self, phoneme_word):
        # Import CMU pronunciation dictionary
        self.gap_penalty = 0.5
        self.cons_vowel_dist = 1
        self.phoneme1_weight = 1.5  # Weight given to first aligned phoneme
        self.target = self._syllables_to_word(phoneme_word)  # Target phoneme word
        self.phoneme_distances = self._create_distances()

    def get_phoneme_distance(self, phoneme1, phoneme2):
        return self.phoneme_distances[phoneme1][phoneme2]

    def _read_matrix(self, matrix_name):
        """
        :param matrix_name: name of csv file, eg: "consonants.csmv"
        :return: pandas.core.frame.DataFrame object
        """
        matrix_path = 'syllables/matrices/' + matrix_name
        return pd.read_csv(matrix_path, index_col=0, na_values="null").dropna()

    def _normalize_matrix(self, dataset):
        min_val = dataset.min().min()
        max_val = dataset.max().max()
        return (dataset - min_val)/(max_val - min_val)

    def _create_distances(self):
        """
        Create DataFrame matrix from files containing all phoneme distances
        """
        consonant_distances = self._read_matrix(CONSONANTS_MATRIX_FILE)
        consonant_distances = self._normalize_matrix(consonant_distances)

        vowel_distances = self._read_matrix(VOWEL_MATRIX_FILE)
        vowel_distances = self._normalize_matrix(vowel_distances)

        # Append consonant & phoneme matrices. Set empty values to max distance
        phoneme_distances = consonant_distances.append(vowel_distances,
                                                       sort=False)
        phoneme_distances = phoneme_distances.fillna(self.cons_vowel_dist)

        # Add gap penalty column and row:
        phoneme_distances['-'] = self.gap_penalty
        gap_row = [self.gap_penalty] * len(phoneme_distances.columns)
        phoneme_distances.loc['-'] = gap_row

        return phoneme_distances

    def _syllables_to_word(self, syllables):
        return list(itertools.chain.from_iterable(syllables))

    def _compute_distance(self, align1, align2, Verbose):
        align1.reverse()
        align2.reverse()
        distance = self.phoneme1_weight * self.get_phoneme_distance(align1[0], align2[0])
        for i in range(1, len(align1)):
            distance += self.get_phoneme_distance(align1[i], align2[i])
        if Verbose:
            print(align1)
            print(align2)

        return distance

    def word_dist(self, word, Verbose=False):
        """
        Using matrices, compute distance between two words.
        Words are computed in their non-syllabified form, eg:
        [["IH", "N"], ["T", "UW"]] -> ["IH", "N" ,"T", "UW"]

        params: words1, word2: list of phonemes, eg: ""
        """
        # Revert back to non syllable form
        word = self._syllables_to_word(word)

        m, n = len(self.target), len(word)
        score = np.zeros((m+1, n+1))  # Initialize scoring matrix

        # Calculate scoring matrix according to Needleman-Wunsch algorithm
        for i in range(0, m + 1):
            score[i][0] = self.gap_penalty * i
        for j in range(0, n + 1):
            score[0][j] = self.gap_penalty * j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                match = score[i - 1][j - 1] + \
                        self.get_phoneme_distance(self.target[i-1], word[j-1])
                delete = score[i - 1][j] + self.gap_penalty
                insert = score[i][j - 1] + self.gap_penalty
                score[i][j] = min(match, delete, insert)

        align1, align2 = [], []
        i, j = m, n  # Begin at the bottom right entry
        while i > 0 and j > 0:  # While not at the top left entry
            score_current = score[i][j]
            score_diag = score[i-1][j-1]
            score_up = score[i][j-1]
            score_left = score[i-1][j]

            if (score_current == score_diag
                    + self.get_phoneme_distance(self.target[i-1], word[j-1])):
                align1.append(self.target[i-1])
                align2.append(word[j-1])
                i -= 1
                j -= 1
            elif score_current == score_left + self.gap_penalty:
                align1.append(self.target[i-1])
                align2.append('-')
                i -= 1
            elif score_current == score_up + self.gap_penalty:
                align1.append('-')
                align2.append(word[j-1])
                j -= 1

        # Back trace up to the top left entry
        while i > 0:
            align1.append(self.target[i-1])
            align2.append('-')
            i -= 1
        while j > 0:
            align1.append('-')
            align2.append(word[j-1])
            j -= 1

        return self._compute_distance(align1, align2, Verbose)


# TESTS
# s = Syllabifier()
# t1 = [["T", "AA", "T"], ["ER"]]
# t2 = [["D", "AA", "T"], ["ER"]]
# t3 = [["T", "AA", "D"], ["ER"]]
# wd = WordDistance(t1)
# print(f"Distance = {wd.word_dist(t2, True)}")
# print(f"Distance = {wd.word_dist(t3, True)}")
# print("-------------")
