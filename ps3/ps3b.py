from ps3a import *
import time
from perm import *


HAND_SIZE = 7
#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    possible_words = []
    hand_size = 0
    for k in hand.keys():
        hand_size += hand[k]

    for i in range(hand_size, 0, -1):
        total_permutations = get_perms(hand, i)
        for w in total_permutations:
            if is_valid_word(w, hand, word_list):
                return w

    return False
    #     for w in total_permutations:
    #         if is_valid_word(w, hand, word_list) and w not in possible_words:
    #             possible_words.append(w)


    # if len(possible_words) == 0:
    #     return False

    # best_word = ""
    # for w in possible_words:
    #     if get_word_score(w, hand_size) > get_word_score(best_word, hand_size):
    #         best_word = w

    # return best_word

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed,
       the remaining letters in the hand are displayed, and the computer
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...
    hand_score = 0
    n = len(hand)
    hand_in_play = True


    while hand_in_play == True:
        display_hand(hand)
        inputted_word = comp_choose_word(hand, word_list)
        if inputted_word == False:
            hand_in_play = False
            continue
        print "Chosen word: ", inputted_word
        print "Score for that word: ", get_word_score(inputted_word, n)
        hand_score += get_word_score(inputted_word, n)
        hand = update_hand(hand, inputted_word)
        if len(hand) == 0:
            hand_in_play = False

    print "Total hand score: ", hand_score


#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    while True:
        game_choice = raw_input("Enter n, r or e: ")
        if game_choice == 'e':
            print "Thanks for playing"
            break
        while game_choice not in ['n', 'r', 'e']:
            print "Lets try that again"
            if game_choice == 'r' and not hand:
                print "You can't choose "
            game_choice = raw_input("Enter n, r or e: ")

        comp_or_human = raw_input("Enter u or c: ")
        while comp_or_human not in ['u', 'c']:
            print "Try that again"
            comp_or_human = raw_input("Enter u or c: ")


        if game_choice == 'n' and comp_or_human == 'u':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand, word_list)

        if game_choice == 'n' and comp_or_human == 'c':
            hand = deal_hand(HAND_SIZE)
            comp_play_hand(hand, word_list)

        if game_choice == 'r' and comp_or_human == 'u':
            try:
                play_hand(hand, word_list)
            except:
                print "Can't replay hand, no original game was started"

        if game_choice == 'r' and comp_or_human == 'c':
            try:
                comp_play_hand(hand, word_list)
            except:
                print "Can't replay hand, no original game was started"


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


