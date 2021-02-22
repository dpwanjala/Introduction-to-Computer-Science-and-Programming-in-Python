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
HAND_SIZE = 5

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
    # Modify the deal_hand function to support always giving one wildcard in each hand. The wildcard replaces
    # one of the vowels.
    hand = {"*": 1}

    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        # we are adding the vowel to the dictionary if it does not exist or getting it if it exists and adding 1 to
        # its value
        hand[x] = hand.get(x, 0) + 1

    # modify this so for the number of consonants because we subtracted 1 to include the * in every hand
    for i in range(num_vowels + 1, n):
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

    # we are going to populate an items_matched list if word exists in word_list or if at least one word formed
    # by replacing * in word exists in word_list

    items_matched = []

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
    # let us initialize a length to 0 and add to this the values for each letter available in the hand
    # remember the values correspond to the number of times the letter occurs in the hand
    handlen = 0

    # just add the values
    for key in hand.keys():
        handlen += hand[key]

    return handlen


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

    # initialize an int at 0 total_score to keep track of the score for each word the user plays
    total_score = 0

    # make a copy of hand so we do not mutate our hand
    new_hand = hand.copy()
    # we will use the length of the keys in the dictionary to keep track of how many letters the players
    # still has available. This works since we are removing the letters from the dictionary every time the user uses up
    # that letter in their word and its frequency reaches 0.
    num_available_letters = len(new_hand.keys())

    while num_available_letters > 0:
        # calculate the hand length
        hand_len = calculate_handlen(new_hand)

        # Display the hand
        print("Current Hand: ", end="")
        display_hand(new_hand)

        # Ask user for input
        user_input = input("Enter word, or '!!' to indicate that you are finished: ")

        if user_input == "!!":
            # If the input is two exclamation points:
            # End the game (break out of the loop)
            print("Total score for this hand: ", total_score)
            print("-----------------------------------------")
            break
        elif is_valid_word(user_input, hand, word_list):
            # Otherwise (the input is not two exclamation points) and it is valid
            # we find the points the user earn for that word they have created
            points_earned = get_word_score(user_input, hand_len)
            # and then updated total score
            total_score += points_earned
            print("'", user_input, "'", " earned ", points_earned, " points. Total: ", total_score, " points")
            # finally we update the user's hand to display only the letters they still have available to use
            new_hand = update_hand(new_hand, user_input)
            # keep track of number of letters left
            num_available_letters = len(new_hand.keys())
        else:
            # the user input is invalid
            # update the hand
            new_hand = update_hand(new_hand, user_input)
            # update the num_available_letters
            num_available_letters = len(new_hand.keys())
            if num_available_letters > 0:
                # input is invalid an user still has available letters left
                print("That is not a valid word. Please choose another word.")
            else:
                # input is invalid and user does not have any available letters left
                print("That is not a valid word.")
                print("Ran out of letters. Total score for this hand: ", total_score, " points")

    return total_score


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

    # create new_hand so we do not mutate hand
    new_hand = hand.copy()

    # let us create an list of letters that we can substitute with by first creating a list of those we can
    # not substitute with
    # unpack the keys of the new_hand dictionary into a list of the keys and append letter as we also can
    # not substitute with that

    non_viable_letters = [*new_hand, letter]

    # letters from vowels and consonants that we can substitute with letter
    viable_letters = [letter for letter in VOWELS + CONSONANTS if letter not in non_viable_letters]

    # user provide letter not in the hand, word should be the same

    if letter not in new_hand or new_hand[letter] == 0:
        # user has provided a letter not in the hand
        # hand should be the same
        return new_hand
    else:
        # letter is in the dictionary
        # replace all copies of the letter with a new letter chosen from the VOWELS and CONSONANTS at random
        # and different from chosen letter
        x = random.choice(viable_letters)
        new_hand[x] = new_hand[letter]
        del new_hand[letter]

    return new_hand


def is_substitute():
    """
    prints the player a prompt to decide whether they want to substitute or not and return a bool value depending
    on their response.
    """
    # include try blocks here to catch user input excepts
    response = str(input("Would you like to substitute a letter? yes/no ").lower())
    return True if response == "yes" or response == "y" else False


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

    # allow user to determine and int total_num_hands they want to play
    total_num_hands = int(input("Enter total number of hands: "))

    # initialize an empty list of hand_scores to keep track of individual current_hand_score
    hand_scores = []

    # initialize a int substitute_options to 0 to keep track of how many times player has substituted a letter in the
    # game
    substitute_options = 1

    # initialize an int replay_option to 0 to keep track of how many times player has replayed a hand in the game
    replay_options = 1

    # initialize an empty dict of hand to keep track of which hand to play
    hand = {}

    # initialize an int num_hands to total_num_hands the user provided to keep track of how many hands the user has
    # played
    num_hands = total_num_hands

    while num_hands > 0:
        # while players still has num_hands to play, keep the game going

        if num_hands == total_num_hands:
            # check if user is playing game for the very first time, if so,
            # deal a new hand
            hand = deal_hand(HAND_SIZE)
            # let player know the hand they have been dealt
            print("Current hand: ", end="")
            display_hand(hand)
            # give the user the option to substitute a letter in the dealt hand
            if is_substitute():
                # player wants to substitute a letter
                # prompt player to provide the letter they want to substitute
                substitute_letter_val = str(input("Which letter would you like to replace? ").lower())
                # substitute letter and update hand
                hand = substitute_hand(hand, substitute_letter_val)
                # decrease substitute_options by 1
                substitute_options -= 1
            else:
                # player doesn't want to substitute a letter, pass
                pass
            # play the hand then and keep track of current_hand_score return value
            current_hand_score = play_hand(hand, word_list)
            # append current_hand_score to hand_scores
            hand_scores.append(current_hand_score)
            # reduce the num_hands by 1
            num_hands -= 1
        elif replay_options >= 1 and substitute_options >= 1:
            # user can replay and they can also substitute,
            # ask if they want to replay a hand
            replay_response = str(input("Would you like to replay the hand? yes/no "))
            if replay_response == "yes" or replay_response == "y":
                # if replay_response is yes, leave hand unchanged,
                # decrease replay_options by 1
                replay_options -= 1
            else:
                # deal a new hand
                hand = deal_hand(HAND_SIZE)

            # give the user the option to substitute a letter in the dealt hand
            if is_substitute():
                # player wants to substitute a letter
                # prompt player to provide the letter they want to substitute
                substitute_letter_val = str(input("Which letter would you like to replace? ").lower())
                # substitute letter and update hand
                hand = substitute_hand(hand, substitute_letter_val)
                # decrease substitute_options by 1
                substitute_options -= 1
            else:
                # player doesn't want to substitute a letter, pass
                pass

            # play the hand and keep track of the current_hand_score for this hand.
            current_hand_score = play_hand(hand, word_list)
            # append current_hand_score to hand_scores
            hand_scores.append(current_hand_score)
            # reduce the num_hands by 1
            num_hands -= 1
        elif replay_options >= 1 and substitute_options < 1:
            # user can replay but not substitute,
            # ask if they want to replay a hand
            replay_response = str(input("Would you like to replay the hand? yes/no "))

            if replay_response == "yes" or replay_response == "y":
                # if replay_response is yes, leave hand unchanged,
                # decrease replay_options by 1
                replay_options -= 1
            else:
                # deal a new hand
                hand = deal_hand(HAND_SIZE)

            # play the hand and keep track of the current_hand_score for this hand.
            current_hand_score = play_hand(hand, word_list)
            # append current_hand_score to hand_scores
            hand_scores.append(current_hand_score)
            # reduce the num_hands by 1
            num_hands -= 1
        elif replay_options < 1 and substitute_options >= 1:
            # user can not replay but they can substitute
            # deal a new hand
            hand = deal_hand(HAND_SIZE)

            # give the user the option to substitute a letter in the dealt hand
            if is_substitute():
                # player wants to substitute a letter
                # prompt player to provide the letter they want to substitute
                substitute_letter_val = str(input("Which letter would you like to replace? ").lower())
                # substitute letter and update hand
                hand = substitute_hand(hand, substitute_letter_val)
                # decrease substitute_options by 1
                substitute_options -= 1
            else:
                # player doesn't want to substitute a letter, pass
                pass
            # play the hand and keep track of the current_hand_score for this hand.
            current_hand_score = play_hand(hand, word_list)
            # append current_hand_score to hand_scores
            hand_scores.append(current_hand_score)
            # reduce the num_hands by 1
            num_hands -= 1
        else:
            # player can not substitute and can not replay but they still have num_hands left to play
            # deal a new hand
            hand = deal_hand(HAND_SIZE)
            # play the hand and keep track of the current_hand_score for this hand.
            current_hand_score = play_hand(hand, word_list)
            # append current_hand_score to hand_scores
            hand_scores.append(current_hand_score)
            # reduce the num_hands by 1
            num_hands -= 1

    # Provide aggregate feedback to the player on their performance at the end of the game.
    print("Total score over all hands: ", sum(hand_scores))
    print("Max score over all hands:", max(hand_scores))
    print("Min score over all hands:", min(hand_scores))


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
