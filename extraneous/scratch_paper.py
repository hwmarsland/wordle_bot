import pandas as pd

# Opening/reading possible words text file
with open('possible_words.txt', 'r', encoding='utf8') as rf:
    text = rf.read()

# Converting text file to a list of words
wordlist = text.split('\n')

alphabet = "abcdefghijklmnopqrstuvwxyz"
dict = {}

# for i in alphabet:
#     for j in wordlist:
#         if i in j:
#             if i in dict.keys():
#                 dict[i] += 1
#             else:
#                 dict[i] = 1

# print(dict)

# Read second words file into pandas dataframe
secondwords = pd.read_excel('optimal_second_words.xlsx')

