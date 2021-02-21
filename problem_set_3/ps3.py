# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Davidpaul Wanjala
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
# -----------additional helper -----------

def get_letters_score(word, letter_values_dict):
    """
    Returns the total score for the letters in the word according to the scoring values for each letter
    from SCRABBLE_LETTER_VALUES
    """
    # strategy 1 considered but not implemented.
    # set an initial letters_score int variable to 0 and increment it by the value of the letter for every
    # iteration through the letters of word

    # strategy 2 implemented.
    # create a list of integer values, by accessing the value for each letter in word that has
    # been defined in the SCRABBLE_LETTER_VALUES dictionary Use sum(list) to calculate the sum of these values

    letters_values_lst = [letter_values_dict.get(letter, 0) for letter in word]

    return sum(letters_values_lst)


def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    # convert to lowercase
    word_lower = word.lower()
    # find word_length = number of letters used in the word
    word_length = len(word_lower)

    # get sum of the points for letters in the word
    letters_score = get_letters_score(word_lower, SCRABBLE_LETTER_VALUES)

    # letters available in current hand
    hand_size = n

    # find the first conditional score of second_component_score
    magic_calc = 7 * word_length - 3 * (hand_size - word_length)

    if magic_calc > 1:
        second_component_score = magic_calc
    else:
        second_component_score = 1

    return letters_score * second_component_score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    # Modify the deal_hand function to support always giving one wildcard in each hand. The wildward replaces
    # one of the vowels.
    hand = {"*": 1}

    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        # we are adding the vowel to the dictionary if it does not exist or getting it if it exists and adding 1 to its value
        # indexing with x here accomplishes 2 things, getting us the value or inserting the key into the dictionary with a value
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    # ensure we convert user word into all lowercase
    word = word.lower()

    # let us copy the hand so we don't modify the origianl hand. This will happen if we use the assignment operator =
    # since this will just create a new references to the original dictionary.

    new_hand = hand.copy()

    # loop through every letter in the word and decrement the value associated with that letter in our new_hand dict
    for letter in word:
        # the word is
        if new_hand.get(letter, 0) > 0:
            # letter is in dictionary and player has used it in word, decrease the value of the letter by -1
            new_hand[letter] = new_hand.get(letter) - 1
            # remove the letter if the value of the letter has reached 0 after subtraction
            if new_hand.get(letter, 0) == 0:
                # use None as second argument to ensure I don't get a KeyError
                new_hand.pop(letter, None)
            else:
                pass
        else:
            # player has guessed a letter not in hand, letter has no effect on hand
            pass

    return new_hand


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    # ensure we convert user word into all lowercase
    word = word.lower()

    # let us make a copy so we don't mutate the original hand dict
    new_hand = hand.copy()

    # loop through every letter in word and update check the value for that letter in hand, if does not exist in
    # hand, i.e its value is zero, return false, otherwise, subtract one from the hand.

    for letter in word:
        if new_hand.get(letter, 0) == 0:
            # letter does not exist in hand or has been used up already
            return False
        else:
            new_hand[letter] = new_hand.get(letter) - 1

    # if first condition has been met, we then check if the word is in word_list efficiently, we progressively filter
    # our word_list, first with the first letter of word and so on, at every step our search space shrinks to exclude
    # words that do not meet the conditions that came before

    # modify to check for words with * in it by replacing the * with vowels

    # to check it word with an * is valid, we first construct a list of words where the * has been replaced
    # by a vowel since * can only replace vowels.

    if "*" in word:
        words_with_vowel = [word.replace("*", vowel) for vowel in VOWELS]

        for each_word in words_with_vowel:
            items_matched = [item for item in word_list if item == each_word]
            if len(items_matched) > 0:
                break
            else:
                pass
    else:
        items_matched = [item for item in word_list if item == word]


    # if the word is not in the list the item_match list will be empty and we can return False, otherwise True.
    return True if len(items_matched) > 0 else False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """

    pass  # TO DO... Remove this line when you implement this function


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score

    # As long as there are still letters left in the hand:

    # Display the hand

    # Ask user for input

    # If the input is two exclamation points:

    # End the game (break out of the loop)

    # Otherwise (the input is not two exclamation points):

    # If the word is valid:

    # Tell the user how many points the word earned,
    # and the updated total score

    # Otherwise (the word is not valid):
    # Reject invalid word (print a message)

    # update the user's hand by removing the letters of their inputted word

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    pass  # TO DO... Remove this line when you implement this function


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    print("play_game not implemented.")  # TO DO... Remove this line when you implement this function


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
