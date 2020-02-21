import nltk
import os
import sys


class Syllabifier:
    def __init__(self):
        # Import CMU pronunciation dictionary
        self.arpabet = nltk.corpus.cmudict.dict()

    def expand_dict(self, dict_name):
        """
        This (optional) function exapands phoneme dictionary
        :param: supplementary: path to supplementary dict
        """
        if os.path.exists(dict_name):
            # Extend dictionary to include additional words
            dic_file = open(dict_name)
            for line in dic_file:
                line = line.split()
                self.arpabet[line[0].lower()] = line[1:]

    def is_valid(self, word):
        """
        Is word in arpbet (or supplementary dict)?
        """
        return word in self.arpabet

    def to_phoneme(self, input_word):
        """
        This function responds to a request for /api/words
        with the complete lists of words

        :param: input_word: word to convert to arpabet
        :returns:        string of translated word
        """

        # Generate list of phonemes for the word
        phones = []

        # All variations of phoneme representations
        for i in range(len(self.arpabet[input_word])):
            phones_w = self.arpabet[input_word][i]
            new_phones = []
            for p in phones_w:
                # omits the numbers from phone labels
                new_p = p[:2]
                new_phones.append(new_p)
            phones.append(new_phones)

        print(f'WORD{i}', file=sys.stdout)

        # Phoneme sonority values
        syl_dic = {
            'AA': 11,
            'AE': 11,
            'AH': 11,
            'AO': 11,
            'AW': 11,
            'AY': 11,
            'EH': 11,
            'ER': 11,
            'EY': 11,
            'IH': 11,
            'IY': 11,
            'OW': 11,
            'OY': 11,
            'UH': 11,
            'UW': 11,
            'Y': 10,
            'W': 10,
            'R': 9,
            'L': 8,
            'M': 7,
            'N': 7,
            'NG': 7,
            'Z': 6,
            'ZH': 6,
            'V': 6,
            'DH': 6,
            'S': 5,
            'SH': 5,
            'F': 5,
            'TH': 5,
            'HH': 5,
            'JH': 4,
            'CH': 3,
            'B': 2,
            'D': 2,
            'G': 2,
            'P': 1,
            'T': 1,
            'K': 1
        }

        # Split phoneme lists into syllables
        syllables = []
        for word in phones:
            boundary = 0
            for i in range(1, len(word)):
                if ((word[i] == 'K'
                        and word[i-1] != 'S'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 8)
                    or (word[i] == 'T'
                        and word[i-1] != 'S'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 9)
                    or (word[i] == 'P'
                        and word[i-1] != 'S'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 8
                        and word[i+1] != 'W')
                    or (word[i] == 'B'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 8
                        and word[i+1] != 'W')
                    or (word[i] == 'G'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 8
                        and not(word[i+1] in ['W', 'Y']))
                    or (word[i] == 'D'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 9)
                    or (word[i] in ['CH', 'JH', 'HH', 'SH', 'DH', 'ZH', 'Z']
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] == 11)
                    or (word[i] == 'TH'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 9
                        and word[i+1] != 'Y')
                    or (word[i] in ['F', 'V']
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 8)
                    or (word[i] in ['N', 'M']
                        and word[i-1] != 'S'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] == 11)
                    or (word[i] == 'L'
                        and not(word[i-1]
                        in ['K', 'P', 'G', 'B', 'F', 'S', 'V'])
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] == 11)
                    or (word[i] == 'R'
                        and not(word[i-1]
                        in ['K', 'T', 'P', 'G', 'D', 'B', 'F', 'V'])
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] == 11)
                    or (word[i] == 'W'
                        and not (word[i-1] in ['K', 'T', 'D', 'TH', 'DH'])
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] == 11)
                    or (word[i] == 'Y'
                        and not (word[i-1] in ['K', 'P', 'F', 'V', 'B'])
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] == 11)
                    or (word[i] == 'S'
                        and i+1 < len(word)
                        and syl_dic[word[i+1]] >= 7)
                    or (word[i] == 'S'
                        and i+1 < len(word)
                        and word[i+1] == 'T'
                        and i+2 < len(word)
                        and syl_dic[word[i+2]] >= 9)
                    or (word[i] == 'S'
                        and i+1 < len(word)
                        and (word[i+1] == 'K' or word[i+1] == 'P')
                        and i+2 < len(word) and syl_dic[word[i+2]] >= 8)
                    or (syl_dic[word[i]] == 11
                        and (syl_dic[word[i-1]] == 11 or word[i-1] == 'NG'))):
                    syllables.append(word[boundary:i])
                    boundary = i

            syllables.append(word[boundary:])
            return syllables  # Take first translation
