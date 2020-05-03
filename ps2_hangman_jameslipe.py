# 6.00 Problem Set 3
#
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!
def check_letter(word, letter):
    word = word.lower()
    letter = letter.lower()
    for n in word:
        if n == letter:
            return True
    return False




rand_word = choose_word(wordlist)
WON_GAME = False
guesses_left = 8
avaliable_letters = "abcdefghijklmnopqurstuvwxyz"
correct_guesses = []
print "Welcome to the game"
print "I am thinking of a word ", len(rand_word), " letters long"
print "------------------"
while WON_GAME == False and guesses_left >= 0:
    if guesses_left == 0:
        print "You lost the game"
        print rand_word
        guesses_left = guesses_left - 1
        continue
    print "You have ", guesses_left, " guesses left"
    print "Avaliable letters: ", avaliable_letters
    for l in rand_word:
        if (l in correct_guesses):
            print l,
        else:
            print "_",
    guessed_letter = raw_input("\n Please guess a letter:")
    if (guessed_letter in correct_guesses):
        print "You already guessed this"
        continue
    if check_letter(rand_word, guessed_letter) == True:
        print "Good guess"
        correct_guesses += guessed_letter
        new_avl_letters = ""
        for i in avaliable_letters:
            if i != guessed_letter:
                new_avl_letters += i
        avaliable_letters = new_avl_letters
        #check if won the game
        WON_GAME = True
        for l in rand_word:
            if (l not in correct_guesses):
                WON_GAME = False
    else:
        print "Bad guess"
        guesses_left = guesses_left - 1

    if WON_GAME == True:
        print rand_word
        print "You won the game, nice!"

    print "-------------"
