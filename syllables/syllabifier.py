import nltk
import os

ADDITIONAL_WORDS_PATH = "syllables/data/dictionary.txt"


class Syllabifier:

    def __init__(self):
        # Import CMU pronunciation dictionary
        self.arpabet = self._expand_arpabet()

    def _expand_arpabet(self):
        """
        Expand arpabet dictionary with text file
        :param: supplementary: path to supplementary dict
        """
        init_dict = nltk.corpus.cmudict.dict()
        if os.path.exists(ADDITIONAL_WORDS_PATH):
            dic_file = open(ADDITIONAL_WORDS_PATH)
            for line in dic_file:
                line = line.split()
                if line[0] == "-":
                    # Remove entry from initial dict
                    init_dict.pop(line[1].lower())
                else:
                    # Add additional word to dict
                    init_dict[line[0].lower()] = [line[1:]]

        return init_dict

    def arpabet(self):
        """
        Return a word->phonemes arpabet dictionary
        """
        return self.arpabet

    def all_syllables(self):
        """
        Return tokenzied list of all syllables from cmu + additional dictionary
        """
        all_syllables = []
        for word in self.arpabet:
            phoneme_word = self.to_phoneme(word)
            sylls = self.to_syllables(phoneme_word)
            for syll in sylls:
                all_syllables.append(['<s>'] + syll + ['</s>'])

        # Remove duplicate syllables (reducing processing time with less data)
        # unique_sylls = set(tuple(i) for i in all_syllables)
        # Flatten list of lists into single lists of ordered phonemes
        return [i for syll in all_syllables for i in syll]

    def is_valid(self, word):
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

        # Take first variation of phoneme representations
        phones_w = self.arpabet[input_word.lower()][0]
        for p in phones_w:
            # omits the numbers from phone labels
            new_p = p[:2]
            phones.append(new_p)

        return phones

    def to_syllables(self, input_phoneme):
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
        phones = []
        phones.append(input_phoneme)
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
                    # If syllable will contain 1 vowel sound
                    if (len(list(filter(lambda x:
                            syl_dic[x] == 11, word[boundary:i]))) == 1):
                        syllables.append(word[boundary:i])
                        boundary = i

            syllables.append(word[boundary:])
            return syllables


# # TESTS
# from collections import Counter
# import cmudict
# Test if every syllable in arpabet dictionary has one vowel sound
# def num_vowels(syll):
#     vowels = [i[0] for i in cmudict.phones() if i[1] == ['vowel']]
#     return len(list((Counter(syll) & Counter(vowels)).elements()))


# s = Syllabifier()
# for word in s.arpabet:
#     syllables_list = s.to_syllables(s.to_phoneme(word))
#     for syll in syllables_list:
#         if num_vowels(syll) != 1:
#             print(word, ": ", syllables_list)

# # Test on word
# print(s.to_syllables(s.to_phoneme("humblest")))
# print(s.to_syllables(s.to_phoneme("unbalanced")))
