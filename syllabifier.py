import nltk
from nltk import corpus
import pathlib
import os


os.chdir('C:/Users/fiona/Desktop/College/Year 4/SimilarSpeak/SS')
wordfile = "input.txt"

supplementary = "dictionary.txt" # input("path to supplementary dictionary (optional): ")

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



# Import CMU pronunciation dictionary
arpabet = nltk.corpus.cmudict.dict() 


#Extend dictionary if required
if supplementary:
    ext_dic_bool = True
    dic_file = open(supplementary)
    for line in dic_file:
        line = line.split()
        arpabet[line[0].lower()] = line[1:]


# Generate list of phonemes for each word
phones = []
unknown_words = []
with open(wordfile, 'r') as f:
    for line in f.readlines():
        words = line.lower().split()
        for w in words:
            if w in arpabet:
                for i in range(len(arpabet[w])): # all variations of phoneme representations
                    phones_w = arpabet[w][i] 
                    new_phones = []
                    for p in phones_w:
                        new_p = p[:2] # omits the numbers from phone labels
                        new_phones.append(new_p)
                    phones.append(new_phones)
                
            else: unknown_words.append(w)



#Split phoneme lists into syllables
syllables = []
for word in phones:
    boundary = 0
    for i in range(1 , len(word)):
  
        if ((word[i] == 'K' and word[i-1]!='S' and i+1< len(word) and syl_dic[word[i+1]] >= 8)
            or (word[i] == 'T' and word[i-1]!='S' and i+1< len(word) and syl_dic[word[i+1]] >= 9)
            or (word[i] == 'P' and word[i-1]!='S' and i+1< len(word) and syl_dic[word[i+1]] >= 8 and word[i+1]!= 'W')
            or (word[i] == 'B' and i+1 < len(word) and syl_dic[word[i+1]] >= 8 and word[i+1]!= 'W')
            or (word[i] == 'G' and i+1 < len(word) and syl_dic[word[i+1]] >=8 and not(word[i+1] in ['W', 'Y']))
            or (word[i] == 'D' and i+1 < len(word) and syl_dic[word[i+1]] >= 9)
            or (word[i] in ['CH', 'JH', 'HH', 'SH', 'DH', 'ZH', 'Z'] and i+1< len(word) and syl_dic[word[i+1]] == 11)
            or (word[i] == 'TH' and i+1 < len(word) and syl_dic[word[i+1]] >= 9 and word[i+1]!='Y')
            or (word[i] in ['F', 'V'] and i+1 < len(word) and syl_dic[word[i+1]] >= 8)
            or (word[i] in ['N', 'M'] and word[i-1]!='S' and i+1< len(word) and syl_dic[word[i+1]]==11)
            or (word[i] == 'L' and not(word[i-1] in ['K', 'P', 'G', 'B', 'F', 'S', 'V']) and i+1< len(word) and syl_dic[word[i+1]] == 11)
            or (word[i] == 'R' and not(word[i-1] in ['K', 'T', 'P', 'G', 'D', 'B', 'F', 'V']) and i+1< len(word) and syl_dic[word[i+1]] == 11)
            or (word[i] == 'W' and not (word[i-1] in ['K', 'T', 'D', 'TH', 'DH']) and i+1< len(word) and syl_dic[word[i+1]] == 11)
            or (word[i] == 'Y' and not (word[i-1] in ['K', 'P', 'F', 'V', 'B']) and i+1< len(word) and syl_dic[word[i+1]] == 11)
            or (word[i] == 'S' and i+1< len(word) and syl_dic[word[i+1]] >= 7)
            or (word[i] == 'S' and i+1< len(word) and word[i+1] == 'T' and i+2 < len(word) and syl_dic[word[i+2]] >= 9)
            or (word[i] == 'S' and i+1< len(word) and (word[i+1] == 'K' or word[i+1] == 'P') and i+2 < len(word) and syl_dic[word[i+2]] >= 8)
            or (syl_dic[word[i]] == 11 and (syl_dic[word[i-1]] == 11 or word[i-1] == 'NG'   )  )):
                syllables.append(word[boundary:i])
                boundary = i
    
    syllables.append(word[boundary:])


outputfile = open("syllables." + wordfile, "w")
for i in syllables:
    outputfile.write( str(i) + "\n")
outputfile.close()


if unknown_words:
    unknown = open("unknown." + wordfile, "w")
    for i in unknown_words:
        unknown.write(i + "\n")
    unknown.close()

