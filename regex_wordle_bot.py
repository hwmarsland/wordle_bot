'''
The purpose of this program is to create a "bot" that interacts with the user through the command line to solve the wordle as quickly as possible.
(mostly so it will beat my dad)

Uses the starting word "slate", which I am using due to the wordle recommendation. Then I use the pandas library to read from the optimal 
second words xlsx file, which is a slimmed down version of a file from Charles Zaiontz's article on the optimal second word to guess (following slate). 
The program then uses regexes to slim down the potential remaining words until one is found and returned to the user.

Hopefully it works.
'''
# Imports
import pandas as pd
import re

# Read second words file into pandas dataframe
secondwords = pd.read_excel('optimal_second_words.xlsx')

# Opening/reading possible words text file
with open('possible_words.txt', 'r', encoding='utf8') as rf:
    text = rf.read()

# Converting text file to a list of words
wordlist = text.split('\n')

# Lists of letters known to be/not be in the word
knownletters = []
removedletters = []


# Cutting down word list
def cut_down(pattern, guess, words):

    basepattern = '.....'

    # First search to collect any green letters
    for i in range(len(pattern)):

        searchpattern = list(basepattern)

        # If letter is a match in that location
        if pattern[i].upper() == 'G':
            knownletters.append(guess[i])
            # Set regex
            searchpattern[i] = guess[i].lower()
            regex = re.compile("".join(searchpattern))
            # Filter wordlist to match all words with that letter in that position
            words = list(filter(regex.match, words))

    # Second search to find any yellow letters
    for j in range(len(pattern)):

        searchpattern = list(basepattern)

        # If letter is a match but not in that location
        if pattern[j].upper() == 'Y':
            knownletters.append(guess[j])
            # Set regex
            searchpattern[j] = guess[j].lower()
            searchpattern = "?!("+ "".join(searchpattern) + ")"
            regex = re.compile(searchpattern)
            # Filter wordlist to remove all words with that letter in that position
            words = list(filter(regex.match, words))
            # Set regex
            searchpattern = ".*" + guess[j].lower() + ".*"
            regex = re.compile(searchpattern)
            # Filter wordlist to match all words that contain that letter at all
            words = list(filter(regex.match, words))

    # Third search to find any letters not in the word
    for k in range(len(pattern)):

        # Letter not in word
        if pattern[k] == '.' and guess[k] not in knownletters:
            removedletters.append(guess[k])
            # Set regex
            searchpattern = "?!("+ guess[k] + ")"
            regex = re.compile(searchpattern)
            # Filter wordlist to remove all words that contain the letter
            words = list(filter(regex.match, words))
    
    return words


wordlist = cut_down('...G.','renew', wordlist)

print(wordlist)