import nltk
import os
import re
from syllables.syllabifier import Syllabifier


def _remove_digits(phonemes):
    """
    Remove stress markers from phoneme translation
    :param phonemes: input list of phonemes (strings)
    """
    return [re.sub('[0-9]', '', i) for i in phonemes]


def phoneme_to_text(phonemes):
    """
    Find first phoneme-text translation in arpabet that map to phoneme input,
    and determine if word is valid
    """
    syllab = Syllabifier()
    arpabet = syllab.arpabet.items()
    valid_word = "N"
    # Look up word in cmudict
    for word, translations in arpabet:
        translations = list(map(_remove_digits, translations))
        if phonemes in translations:
            valid_word = "Y"
            return word, valid_word  # valid word

    return nonsense_to_text(phonemes), valid_word  # nonsense word


def nonsense_to_text(phonemes):
    phoneme_to_letter = {
        'AA': 'o',
        'AE': 'a',
        'AH': 'u',
        'AO': 'aw',
        'AW': 'ow',
        'AY': 'y',
        'EH': 'e',
        'ER': 'er',
        'EY': 'a',
        'IH': 'i',
        'IY': 'ee',
        'OW': 'ow',
        'OY': 'oy',
        'UH': 'uh',
        'UW': 'oo',
        'Y': 'y',
        'W': 'w',
        'R': 'r',
        'L': 'l',
        'M': 'l',
        'N': 'n',
        'NG': 'ng',
        'Z': 'z',
        'ZH': 'sh',
        'V': 'v',
        'DH': 'th',
        'S': 's',
        'SH': 'sh',
        'F': 'f',
        'TH': 'th',
        'HH': 'h',
        'JH': 'j',
        'CH': 'ch',
        'B': 'b',
        'D': 'd',
        'G': 'g',
        'P': 'p',
        'T': 't',
        'K': 'k'
        }

    letters = [phoneme_to_letter[p] for p in phonemes]
    return "".join(letters)
