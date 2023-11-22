'''
WORDLE BOT

The purpose of this program is to create a "bot" that interacts with the user through the command line to solve the wordle.
(mostly to see if I can make one that beats my dad)

Uses the starting word "slate", which I am using due to the wordle recommendation. Then I use the pandas library to read from the optimal 
second words xlsx file, which is a slimmed down version of a file from Charles Zaiontz's article on the optimal second word to guess (following slate). 
The program then uses looping list comprehension to slim down the potential remaining words until the one is found.

Hopefully it works.

Harris Marsland
'''


# === SETUP ===

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


# === REDUCING WORD LIST ===

# Cutting down word list
def cut_down(pattern, guess, words):

    basepattern = '.....'

    # First search to collect any green letters
    for i in range(len(pattern)):

        # If letter is a match in that location
        if pattern[i].upper() == 'G':
            knownletters.append(guess[i])
            words = [x for x in words if x[i] == guess[i]]

    # Second search to find any yellow letters
    for j in range(len(pattern)):

        # If letter is a match but not in that location
        if pattern[j].upper() == 'Y':
            knownletters.append(guess[j])
            words = [x for x in words if x[j] != guess[j]]
            words = [x for x in words if guess[j] in x]

    # Third search to find any letters not in the word
    for k in range(len(pattern)):

        # Letter not in word
        if pattern[k] == '*' :
            if guess[k] not in knownletters:
                removedletters.append(guess[k])
                words = [x for x in words if guess[k] not in x]
            else:
                words = [x for x in words if x[k] != guess[k]]
    
    # print(words)
    # print(removedletters)
    # print(knownletters)
    return words


# Guess loop used for testing the process of cutting down the word list
def testing_guess_loop():
    flag = True
    words = wordlist

    while flag:
        guess = input("What is the word you're guessing?\n")
        pattern = input("What is the pattern that was returned?\n")
        if pattern == "GGGGG":
            print("Good Stuff.")
            return
        words = cut_down(pattern, guess, words)
        print(words)


# === SOLVING THE WORDLE ===

# Function that determines what the second guess should be
def second_guess(pattern):
    counter = 0
    pattern = pattern.upper()
    for i in secondwords["SLATE return val"]:
        if i == pattern:
            return secondwords["optimal guess"][counter]
        counter += 1


# Function for readablilty and stats
def words_left(words):
    print("There are now " + str(len(words)) + " possible words.")
    if len(words) <= 5:
        print(words)
    print("\n")


# Wordle solver
def solve():
    words = wordlist
    count = 0
    pattern = ''
    next_guess = ''

    while True:
        # First guess is always SLATE
        if count == 0:
            # First guess
            print("\nThe word you should guess is:\nSLATE")
            # Get pattern returned from user
            pattern = input("What is the pattern that was returned?\n(Use G to indicate green letters, Y to indicate yellow letters and * to indicate black letters)\n")
            # End condition
            if pattern == "GGGGG":
                print("Good stuff.\n")
                break
            # Cut down list
            words = cut_down(pattern, 'slate', words)
            # User visuals
            words_left(words)

        # Second guess is based on pattern returned from first guess
        elif count == 1:
            # Get second guess
            next_guess = second_guess(pattern)
            # Get pattern returned from user
            print("The word you should guess is:\n" + next_guess.upper())
            pattern = input("What is the pattern that was returned?\n")
            # End condition
            if pattern == "GGGGG":
                print("Good stuff.\n")
                break
            # Cut down list
            words = cut_down(pattern, next_guess, words)
            # User visuals
            words_left(words)

        # Subsequent guesses are based on the first word in the remaining words list
        else:
            # First word of possible words list
            next_guess = words[0]
            print("The word you should guess is:\n" + next_guess.upper())
            # Get pattern returned from user
            pattern = input("What is the pattern that was returned?\n")
            # End condition
            if pattern == "GGGGG":
                print("Good stuff.\n")
                break
            # Cut down list
            words = cut_down(pattern, next_guess, words)
            # User visuals
            words_left(words)

        count += 1


# === START ===

solve()