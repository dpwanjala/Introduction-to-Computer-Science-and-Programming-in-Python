# Problem Set 2, hangman.py
# Name: Davidpaul Wanjala
# Collaborators: None human. More precisely, Google and starkoverflow + quora + youtube.
# Time spent: 2 whole days. approximately 24 hours.

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

# ****************** parameters *******************

welcome_msg = "Welcome to the game Hangman."
max_warnings = 3
max_guesses = 6


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    # Strategy
    # 1. We first loop through the secret_word and check if each letter of the secret_word is in the
    #   letters_guessed list. We break at the first instance when the value is false for efficiency since we
    #   don't need to check anymore to get our answer.
    # 2. We return a boolean value that we updated with each iteration through our list of letters and now points to
    #   whether all letters have been guessed or there is a letter in the secret_word that has not been guessed.

    is_word_guessed_bool = False

    # step 1.

    # break at the first instance we find a secret_word_letter that is not guessed
    for secret_word_letter in secret_word:
        if secret_word_letter in letters_guessed:
            is_word_guessed_bool = True
        else:
            is_word_guessed_bool = False
            break

    # step 2.

    return is_word_guessed_bool


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    # Strategy
    # 1. We first create guessed_word_ls that we will populate with either the letter that has been guessed or
    #   with a "_ " depending on whether the secret_word_letter is present in the already letters_guessed.
    # 2. We are going to use letter_index to keep track of the indices of the letters as we populate our guessed_word_ls
    #   so we can ensure we insert our letter in the right position in the word.
    # 3. We finally return a string constructed from that list of letters that we just created. And this my friend, is
    #   the guessed_word filled up with letters already guessed and gaps for those not guessed.

    guessed_word_ls = []
    letter_index = 0

    for secret_word_letter in secret_word:
        if secret_word_letter in letters_guessed:
            guessed_word_ls.insert(letter_index, secret_word_letter)
            letter_index += 1
        else:
            guessed_word_ls.insert(letter_index, "_ ")
            letter_index += 1

    init_string = ""
    return init_string.join(guessed_word_ls)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    # Strategy 1. we are going to use margin to do this in one sentence. Here we go! 2. We will utilize the
    # string.ascii_lowercase property which gives us a string comprised of all lowercase letters 3. We are going to
    # loop through every letter that has been guessed and each time we will use that letter as and index to
    # "translate" or in other word to remove it from our original string by setting its value to None. Boom!

    english_letters_string = string.ascii_lowercase.translate({ord(i): None for i in letters_guessed})

    return english_letters_string


# *************************** additional helper functions *****************************

# print a welcome message

def print_welcome(welcome_msg, secret_word):
    """
     welcome_message: string, an introduction welcome message
     secret_word: string, the selected secret word the players i to guess
     returns: None, we just print out the message and secret_word plus a separator to the console for the player
    """
    print(welcome_msg)
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    # print a separator
    print("----------------")


# recursively find number of unique characters in a word

def num_unique_chars(word):
    # base case 1
    if len(word) == 0:
        return 0
    # base case 2
    elif len(word) == 1:
        return 1
    # recursive cases
    elif word[0] in word[1:]:
        return 0 + num_unique_chars(word[1:])
    else:
        return 1 + num_unique_chars(word[1:])


# calculate the score at any point in the game

def get_score(secret_word, num_guesses_left):
    """
     secret_word: string, the selected secret word the players i to guess
     num_guesses_left: int, the number of guesses the user has left before they make the next guess
     returns: string, the total score computed as a function of this two variables
    """
    # total score is num_guesses_left * number of unique letters in secret word
    return str(num_guesses_left * num_unique_chars(secret_word))


def is_input_valid(user_guess):
    """
     user_input: an input provided by a user
     returns: boolean . True if users input is valid and false otherwise
    """
    return True if user_guess in string.ascii_lowercase else False


def guess_is_invalid(guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed):
    """
     guess: string, the letter player has guessed
     secret_word: string, the selected secret word the players i to guess
     num_guesses_left: int, the number of guesses the user has left before they make the next guess
     num_warnings_left: int, the number of warnings the user has left before they make the next guess
     letters_guessed: list, the letters the user has already guessed
     returns: list, containing updated [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    """
    if num_warnings_left > 0:
        # players inputs a non alphabet symbol and has warnings left.
        # player loses 1 warning of the num_warnings_left and
        num_warnings_left -= 1
        # player is informed to only guess alphabet symbols and then the updated number of warnings they have left.
        print("Oops! " + guess + " is an not a valid symbol. Only alphabets are valid. You have " + str(
            num_warnings_left) + " warnings left.")
        # Tell player which letters are available for them to select from
        print("Available letters: " + get_available_letters(letters_guessed))
        # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
        print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
        # player is informed of their progress so far by showing them guessed_word
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print("Guess: " + str(guessed_word))
        return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    elif num_warnings_left == 0 and num_guesses_left > 0:
        # players inputs a non alphabet symbol and has no warnings left but has guesses left.
        # player loses 1 guess of the num_guesses_left and
        num_guesses_left -= 1
        # player is informed to only guess alphabet symbols and then the updated number of warnings they have left.
        print("Oops! " + guess + " is an not a valid symbol. Only alphabets are valid. You have no warnings left. "
                                 "So you lose one guess. You have " + str(num_guesses_left) + " guesses left.")
        # Tell player which letters are available for them to select from
        print("Available letters: " + get_available_letters(letters_guessed))
        # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
        print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
        # player is informed of their progress so far by showing them guessed_word
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print("Guess: " + str(guessed_word))
        return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    else:
        print("number of guesses less than 0")


def guess_is_in_letters_guessed(guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed):
    """
     guess: string, the letter player has guessed
     secret_word: string, the selected secret word the players i to guess
     num_guesses_left: int, the number of guesses the user has left before they make the next guess
     num_warnings_left: int, the number of warnings the user has left before they make the next guess
     letters_guessed: list, the letters the user has already guessed
     returns: list, containing updated [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    """
    # player inputs a valid guess but the letter has already been guessed, i.e it is in letters_guessed
    if num_warnings_left > 0:
        # player has warnings left
        # player loses 1 of the num_warnings_left and
        num_warnings_left -= 1
        # player is informed the letter has already been guessed and then the updated number of warnings they have left.
        print("Oops! You have already guessed " + guess + ". You have " + str(num_warnings_left) + " warnings left")
        # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
        # Tell player which letters are available for them to select from
        print("Available letters: " + get_available_letters(letters_guessed))
        print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
        # player is informed of their progress so far by showing them guessed_word
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print("Guess: " + str(guessed_word))
        return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    elif num_guesses_left > 0 and num_warnings_left <= 0:
        # player has guesses left
        # player loses 1 of the num_guesses_left and
        num_guesses_left -= 1
        # player is informed the letter has already been guessed and then the updated number of guesses they have left.
        print("Oops! You have already guessed " + guess + ". You have no warnings left. So you lose one guess. "
                                                          "You have " + str(num_guesses_left) + " guesses left")
        # Tell player which letters are available for them to select from
        print("Available letters: " + get_available_letters(letters_guessed))
        # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
        print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
        # player is informed of their progress so far by showing them guessed_word
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print("Guess: " + str(guessed_word))
        return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]


def guess_is_not_in_letters_guessed(guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed):
    """
     guess: string, the letter player has guessed
     secret_word: string, the selected secret word the players i to guess
     num_guesses_left: int, the number of guesses the user has left before they make the next guess
     num_warnings_left: int, the number of warnings the user has left before they make the next guess
     letters_guessed: list, the letters the user has already guessed
     returns: list, containing updated [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    """
    # player inputs a valid guess and the letter has not been guessed before, i.e it is not in letters_guessed
    # first add the guess to the letters_guessed because it in not in it. we are adding every guess and not only
    # the ones in secret_word so we can use this to later check how many guesses the player made using its length
    letters_guessed.append(guess)
    # then we run another conditional using the new list of letters_guessed
    if guess not in secret_word:
        # player has still not made the final letter guess and the guess is not in the secret_word
        if guess not in "aeiou":
            # player has guessed a consonant player inputs a consonant that has not been guessed and the consonant is
            # not in the secret word, the user loses 1 guess
            num_guesses_left -= 1
            # player is informed their guess is incorrect and the then the number of guesses they have left
            print(
                "Oops! " + guess + " is not in my word. You guessed a consonant. So you lose 1 guess. You have " + str(
                    num_guesses_left) + " guesses left")
            # Tell player which letters are available for them to select from
            print("Available letters: " + get_available_letters(letters_guessed))
            # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
            print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print("Guess: " + str(guessed_word))
            return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
        else:
            # player inputs a vowel that has not been guessed and the vowel is not in the secret word, the user loses
            # 2 guesses
            num_guesses_left -= 2
            # player is informed their guess is incorrect and the then the number of guesses they have left
            print("Oops! " + guess + " is not in my word. You guessed a vowel. So you lose 2 guesses. You have " + str(
                num_guesses_left) + " guesses left")
            # Tell player which letters are available for them to select from
            print("Available letters: " + get_available_letters(letters_guessed))
            # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
            print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            print("Guess: " + str(guessed_word))
            return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    elif guess in secret_word:
        # player has still not made the final letter guess and the guess is in the secret_word
        # already added the guess to letters_guessed above
        # player is informed they made a good guess
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print(guess + " is a good guess: " + str(guessed_word))
        # available guesses left
        print("You have " + str(num_guesses_left) + " guesses left")
        # Tell player which letters are available for them to select from
        print("Available letters: " + get_available_letters(letters_guessed))
        # player is informed of their current score
        print("Your current score for this game is: " + get_score(secret_word, num_guesses_left))
        return [guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed]


def game_is_won(secret_word, num_guesses_left, num_warnings_left, letters_guessed):
    """
     secret_word: string, the selected secret word the players i to guess
     num_guesses_left: int, the number of guesses the user has left before they make the next guess
     num_warnings_left: int, the number of warnings the user has left before they make the next guess
     letters_guessed: list, the letters the user has already guessed
     returns: list, containing updated [secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    """
    # player just guessed a valid last guess, so they win the game.
    # player loses no guesses or warnings
    # first we inform the player they made a good guess, show them the secret_word and
    print(
        "Good guess: " + secret_word)  # initially, i was using get_guessed_word here, and realized we can avoid that computation
    print("Congratulations, you won!")
    # inform the player of their total score
    print("Your total score for this game is: " + get_score(secret_word, num_guesses_left))
    return [secret_word, num_guesses_left, num_warnings_left, letters_guessed]


def game_is_lost(secret_word, num_guesses_left, num_warnings_left, letters_guessed):
    """
     secret_word: string, the selected secret word the players i to guess
     num_guesses_left: int, the number of guesses the user has left before they make the next guess
     num_warnings_left: int, the number of warnings the user has left before they make the next guess
     letters_guessed: list, the letters the user has already guessed
     returns: list, containing updated [secret_word, num_guesses_left, num_warnings_left, letters_guessed]
    """
    # player has no guesses left, and they haven't guessed the word, end the game and reveal secret word
    # player is informed of their current score which will keep decreasing as their num_guesses_left decrease
    print("Your total score for this game is: " + get_score(secret_word, num_guesses_left))
    print("Sorry, you ran out of guesses. The word was " + secret_word)
    return [secret_word, num_guesses_left, num_warnings_left, letters_guessed]


# ****************  MAIN GAME CONTROL FLOW ***************

def hangman(secret_word, welcome_msg, max_warnings, max_guesses):  # added additional parameters
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # Strategy.
    # step 0. welcome message and let the user know if they can play the game and the length of the secret_word
    if max_guesses > 0:
        print_welcome(welcome_msg, secret_word)
    elif max_guesses == 0:
        print("You can't play the game since you don't have any guesses available for you.")
    else:
        print("We can't have a negative number of maximum allowed guesses")

    # 1. first we initialize our num_guesses_left to max_guesses. users of this function can decide maximum number of
    #   guesses players will be allowed. we do the same for num_warnings_left and an empty initial letters_guessed.
    num_guesses_left = max_guesses
    num_warnings_left = max_warnings
    letters_guessed = []

    # 2. we start our game loop that will run as long as there are available guesses to the user. we will eventually
    #   decrease this at some point to get out of the loop or break out of the loop if user wins the game

    while num_guesses_left > 0:
        # 3. every time through the loop we ask the user to enter their selection of letter input and convert then we
        # convert that input into a lowercase for sanity purposes!. we only do this if the user has not won the game.
        # we deliberately break out of the loop if the game is won.
        if is_word_guessed(secret_word, letters_guessed):
            game_is_won(secret_word, num_guesses_left, num_warnings_left, letters_guessed)
            break
        else:
            guess = input("Please guess a letter: ").lower()

        # we check the following condition and run appropriate blocks of code every time through the loop

        # 1. first we check the validity of the user input, if it is not valid, we do not proceed.
        if not is_input_valid(guess):
            # if players input is not valid, we call guess_is_invalid helper which will run appropriate block of code.
            # guess_is_invalid has the logic for the game for when this is the condition. it takes in the following
            # variables and returns a list of the same variable, so of which will have been update so we can access it
            # in this while loop scope for the next iterations.
            guess_invalid = guess_is_invalid(guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed)
            num_guesses_left = guess_invalid[2]
            num_warnings_left = guess_invalid[3]
            letters_guessed = guess_invalid[4]
        elif guess in letters_guessed:
            # the second condition we check is when player input is valid but they have already guessed that letter
            #  before. similarly the logic is abstracted in the function guess_in_letters_guessed which will return us
            #  updated variables that we can use in the next loop
            guess_in_letters_guessed = guess_is_in_letters_guessed(guess, secret_word, num_guesses_left,
                                                                   num_warnings_left, letters_guessed)
            num_guesses_left = guess_in_letters_guessed[2]
            num_warnings_left = guess_in_letters_guessed[3]
            letters_guessed = guess_in_letters_guessed[4]
        elif guess not in letters_guessed and num_guesses_left > 0:
            # the last condition whe check is when player input is valid and they have not guessed that letter before
            # the guess_not_in_letters_guessed will handle this condition for us.
            guess_not_in_letters_guessed = guess_is_not_in_letters_guessed(guess, secret_word, num_guesses_left,
                                                                           num_warnings_left, letters_guessed)
            num_guesses_left = guess_not_in_letters_guessed[2]
            num_warnings_left = guess_not_in_letters_guessed[3]
            letters_guessed = guess_not_in_letters_guessed[4]
        else:
            print("Huh?")

    # player loses game
    # player will lose the game if they have no guesses left and they have not guessed the word correctly yet.
    if num_guesses_left == 0 and not is_word_guessed(secret_word, letters_guessed):
        game_is_lost(secret_word, num_guesses_left, num_warnings_left, letters_guessed)
    else:
        pass


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word_whitespace, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    # strategy is to keep track of a boolean value and change it to false at the first instance we don't find a match
    # and break out of the loops
    my_word = my_word_whitespace.replace(" ", "")

    if len(my_word) == len(other_word):
        matches_or_gap = False
        word_len = len(my_word)
        index = 0
        while word_len > 0:
            for letter in my_word:
                if letter == other_word[index] or letter == "_":
                    matches_or_gap = True
                    word_len -= 1
                    index += 1
                else:
                    matches_or_gap = False
                    break
            break
    else:
        return False
    return matches_or_gap

def all_unique_letters(word):
    if len(word) == num_unique_chars(word):
        return True
    return False

def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    # Strategy
    # 1. call match_with_gaps on wordlist and return word if match_with_gaps resolves to true and put it in a list
    #   possible_matches and otherwise skip the word in wordlist that does not match. I use a list expression
    #   to help me do this efficiently and in one line. I love this.
    # 2. return that new list of possible_matches

    possible_matches = [word for word in wordlist if match_with_gaps(my_word, word) and all_unique_letters(word)]

    return possible_matches


def hangman_with_hints(secret_word, welcome_msg, max_warnings, max_guesses):  # added additional parameters
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # step 0. welcome message and let the user know if they can play the game and the length of the secret_word
    if max_guesses > 0:
        print_welcome(welcome_msg, secret_word)
    elif max_guesses == 0:
        print("You can't play the game since you don't have any guesses available for you.")
    else:
        print("We can't have a negative number of maximum allowed guesses")

    # 1. first we initialize our num_guesses_left to max_guesses. users of this function can decide maximum number of
    #   guesses players will be allowed. we do the same for num_warnings_left and an empty initial letters_guessed.
    num_guesses_left = max_guesses
    num_warnings_left = max_warnings
    letters_guessed = []

    # 2. we start our game loop that will run as long as there are available guesses to the user. we will eventually
    #   decrease this at some point to get out of the loop or break out of the loop if user wins the game

    while num_guesses_left > 0:
        # 3. every time through the loop we ask the user to enter their selection of letter input and convert then we
        # convert that input into a lowercase for sanity purposes!. we only do this if the user has not won the game.
        # we deliberately break out of the loop if the game is won.
        if is_word_guessed(secret_word, letters_guessed):
            game_is_won(secret_word, num_guesses_left, num_warnings_left, letters_guessed)
            break
        else:
            guess = input("Please guess a letter: ").lower()

        # we check the following condition and run appropriate blocks of code every time through the loop

        if guess == "*":
            possible_matches = show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print("Possible matches are: " + str(possible_matches))
            print("--------------------")
        elif not is_input_valid(guess) and guess is not "*":
            # if players input is not valid, we call guess_is_invalid helper which will run appropriate block of code.
            # guess_is_invalid has the logic for the game for when this is the condition. it takes in the following
            # variables and returns a list of the same variable, so of which will have been update so we can access it
            # in this while loop scope for the next iterations.
            guess_invalid = guess_is_invalid(guess, secret_word, num_guesses_left, num_warnings_left, letters_guessed)
            num_guesses_left = guess_invalid[2]
            num_warnings_left = guess_invalid[3]
            letters_guessed = guess_invalid[4]
        elif guess in letters_guessed:
            # the second condition we check is when player input is valid but they have already guessed that letter
            #  before. similarly the logic is abstracted in the function guess_in_letters_guessed which will return us
            #  updated variables that we can use in the next loop
            guess_in_letters_guessed = guess_is_in_letters_guessed(guess, secret_word, num_guesses_left,
                                                                   num_warnings_left, letters_guessed)
            num_guesses_left = guess_in_letters_guessed[2]
            num_warnings_left = guess_in_letters_guessed[3]
            letters_guessed = guess_in_letters_guessed[4]
        elif guess not in letters_guessed and num_guesses_left > 0:
            # the last condition whe check is when player input is valid and they have not guessed that letter before
            # the guess_not_in_letters_guessed will handle this condition for us.
            guess_not_in_letters_guessed = guess_is_not_in_letters_guessed(guess, secret_word, num_guesses_left,
                                                                           num_warnings_left, letters_guessed)
            num_guesses_left = guess_not_in_letters_guessed[2]
            num_warnings_left = guess_not_in_letters_guessed[3]
            letters_guessed = guess_not_in_letters_guessed[4]
        else:
            print("Huh?")

    # player loses game
    # player will lose the game if they have no guesses left and they have not guessed the word correctly yet.
    if num_guesses_left == 0 and not is_word_guessed(secret_word, letters_guessed):
        game_is_lost(secret_word, num_guesses_left, num_warnings_left, letters_guessed)
    else:
        pass


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word, welcome_msg, max_warnings, max_guesses)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word, welcome_msg, max_warnings, max_guesses)  # added additional parameters
