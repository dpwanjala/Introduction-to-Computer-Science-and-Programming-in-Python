# Problem Set 4B
# Name: David Paul Wanjala
# Collaborators: None
# Time Spent: 3 hours

import string


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    is_word(word_list, 'bat') returns
    True
     is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


# ********************* additional helper function ****************

def shift_letters(alphabet_letters, shift):
    """
    shifts alphabet_letters by an number shift

    alphabet_letters, string

    shift, int

    returns a shift_dict, dictionary where keys are the letters and values are corresponding letters shifted to
    """
    # initialize an empty dictionary
    shift_dict = {}
    # initialize an int variable 0 to keep track of the letter index in letters string
    letter_index = 0
    for letter in alphabet_letters:
        # for each letter in the alphabet letter check if it can be shifted forwards or has to cycle around
        if letter_index + shift > 25:
            # if shifting a letter will place it beyond letter z, cycle it to earlier characters and add it to shift_dict
            shift_dict[letter] = alphabet_letters[(letter_index + shift) - 26]
            # increment the index before we move to the next letter
            letter_index += 1
        else:
            # if shifting a letter will not place it beyond z
            # add the key corresponding to the letter to shift_dict and the corresponding shift letter as value of key
            shift_dict[letter] = alphabet_letters[letter_index + shift]
            # increment the index before we move to the next letter
            letter_index += 1
    return shift_dict


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        # assign data attributes
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        # return immutable version of the message_text
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words_copy = self.valid_words.copy()
        return valid_words_copy

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        lowercase_dict = shift_letters(string.ascii_lowercase, shift)
        uppercase_dict = shift_letters(string.ascii_uppercase, shift)

        return {**lowercase_dict, **uppercase_dict}

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''

        # we create a char_lst to hold all our shifted characters and special symbols as we encrypt the message
        char_lst = []
        shift_dict = self.build_shift_dict(shift)

        # strategy is to place the special symbol as they are in char_list, shift the letters and place them in char_lst
        # as well and letter join the characters in char_lst into a string
        for char in self.message_text:
            if char in string.ascii_letters:
                shifted_char = shift_dict[char]
                char_lst.append(shifted_char)
            else:
                char_lst.append(char)

        return "".join(char_lst)


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        # Use the parent class constructor to make your code more concise
        Message.__init__(self, text)  # returns self.message_text and self.valid_words
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict_copy = self.encryption_dict.copy()
        return encryption_dict_copy

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''

        # set new self.shift to value of shift
        self.shift = shift

        # set new self.encryption_dict by invoking self.build_shift_dict(shift)
        self.encryption_dict = self.build_shift_dict(shift)

        # set new self.message_text_encrypted by invoking self.apply_shift(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        # Use the parent class constructor to make your code more concise
        Message.__init__(self, text)  # returns self.message_text and self.valid_words

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        valid_words = self.get_valid_words()

        # list to keep track of real words for shift values corresponding to index in the list
        real_words_count = {}

        # all possible shift values, note when shift_value 0, the shift position is the same as original position.
        for shift_value in range(26):

            # shift each letter shift_value and create a list of the strings - splits on whitespace and discards
            # empty strings
            shifted_message_text_lst = self.apply_shift(shift_value).split()

            # if a string in the shifted message is_word keep it, if not discard it, this will tell us how many real
            # words we get by shifting the message_text by that shift_value
            real_words = [word for word in shifted_message_text_lst if is_word(valid_words, word)]

            # how many real words do we have for this shift, and keep track of it
            real_words_count[shift_value] = len(real_words)

            if len(real_words) == len(self.message_text):
                # if we have the number of real words equal to the number of words in message_text, we have found
                # our decryption shift_value and we can break out of the loop for efficiency
                break
            else:
                pass

        # max value/s in our real_words_count list
        max_real_words = max(real_words_count.values())
        # shift values as dictionary keys that have the max_real_words as their key values
        best_shift_values = [k for k, v in real_words_count.items() if v == max_real_words]

        # select the first best_shift_value
        best_shift_value = best_shift_values[0]

        # decrypt the message
        decrypted_message = self.apply_shift(best_shift_value)

        # tuple with first instance of best_shift_values and the decrypted message
        return (best_shift_value, decrypted_message)


if __name__ == '__main__':

    # example test case 1
    plaintext = PlaintextMessage('Hello, World!', 2)
    print('Expected Output: Jgnnq Yqtnf!')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # example test case 2
    ciphertext = CiphertextMessage('Jgnnq Yqtnf!')
    print('Expected Output:', (24, 'Hello, World!'))
    print('Actual Output:', ciphertext.decrypt_message())

    # best shift value for deciphering story = 12
    ciphertext = CiphertextMessage(get_story_string())
    print('Actual Output:', ciphertext.decrypt_message())
    # Actual Output: (12, 'Jack Florey is a mythical character created on the spur of a moment to help cover an
    # insufficiently planned hack. He has been registered for classes at MIT twice before, but has reportedly never
    # passed aclass. It has been the tradition of the residents of East Campus to become Jack Florey for a few nights
    # each year to educate incoming students in the ways, means, and ethics of hacking.')
