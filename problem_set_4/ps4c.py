# Problem Set 4C
# Name: David Paul Wanjala
# Collaborators: None
# Time Spent: 2 hours

import string
from ps4a import get_permutations


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
    # >>> is_word(word_list, 'bat') returns
    True
    # >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


def maintain_letters_dict(alphabet_letters):
    """
    create a dictionary mapping in which the keys and the values are the same
    alphabet_letters, string
    returns dictionary

    """
    # initialize an empty placeholder dictionary
    letters_dict = {}
    # initialize an int variable 0 to keep track of the letter index alphabet_letters
    letter_index = 0

    for letter in alphabet_letters:
        # for each letter in alphabet_letters append a key value pair in letters_dict where the key is
        # alphabet letter and the value is also the same alphabet letter
        letters_dict[letter] = alphabet_letters[letter_index]
        letter_index += 1
    return letters_dict


def shuffle_vowels(vowels, vowels_permutation):
    """
    shuffle vowels
        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"
    """
    # initialize an empty placeholder dictionary
    vowels_dict = {}
    # initialize an int variable 0 to keep track of the vowel index in vowels collection
    vowel_index = 0

    for vowel in vowels:
        # for each letter in vowels append a key value pair in vowels_dict where the key is the vowel in and the
        # value is corresponding positional vowel in vowels_permutation
        vowels_dict[vowel] = vowels_permutation[vowel_index]
        vowel_index += 1
    return vowels_dict


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
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

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lowercase_vowel_dict = shuffle_vowels(VOWELS_LOWER, vowels_permutation)
        uppercase_vowel_dict = shuffle_vowels(VOWELS_UPPER, vowels_permutation)
        lowercase_consonant_dict = maintain_letters_dict(CONSONANTS_LOWER)
        uppercase_consonant_dict = maintain_letters_dict(CONSONANTS_UPPER)

        return {**lowercase_vowel_dict, **lowercase_consonant_dict, **uppercase_vowel_dict, **uppercase_consonant_dict}

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''

        char_lst = []

        for char in self.message_text:
            if char in string.ascii_letters:
                # if the character is a letter append to the char_lst the transposed char value from transpose_dict
                transposed_char = transpose_dict[char]
                char_lst.append(transposed_char)
            else:
                char_lst.append(char)

        return "".join(char_lst)


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)  # returns self.message_text and self.valid_words

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        # generate all permutations of vowels
        vowel_lower_permutations = get_permutations(VOWELS_LOWER)
        vowel_upper_permutations = get_permutations(VOWELS_UPPER)
        vowel_permutations = vowel_lower_permutations + vowel_upper_permutations

        # use each permutation to substitute for vowels and check how many resulting real words I get
        # get valid words
        valid_words = self.get_valid_words()

        # list to keep track of real words for each vowel permutation
        real_words_count = {}

        # all possible possible vowel permutations
        for vowel_permutation in vowel_permutations:
            # build a transpose dict
            transpose_dict = self.build_transpose_dict(vowel_permutation)
            # apply the transpose using the constructed transpose_dict and create a list with each word of the
            # resulting transposed message text
            transposed_message_text_lst = self.apply_transpose(transpose_dict).split()
            # create a list with real words we have in the transposed_message_text_lst
            real_words = [word for word in transposed_message_text_lst if is_word(valid_words, word)]
            # how many real words do we have for this permutation transpose, append that to the dict real_words_count
            real_words_count[vowel_permutation] = len(real_words)

        # max value/s in our real_words_count list
        max_real_words = max(real_words_count.values())
        # vowel_permutation dictionary keys that have the max_real_words as their key values
        best_vowel_permutations = [k for k, v in real_words_count.items() if v == max_real_words]

        # select the first best_vowel_permutation
        best_vowel_permutation = best_vowel_permutations[0]

        # decrypt the message
        best_transpose_dict = self.build_transpose_dict(best_vowel_permutation)
        decrypted_message = self.apply_transpose(best_transpose_dict)

        return decrypted_message


if __name__ == '__main__':
    # example test case 1
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict)) # Output:  "Hallu Wurld!"
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Encoded message: ", enc_message.get_message_text())
    print("Decrypted message:", enc_message.decrypt_message()) # Output: "Hello World!"

    # example test case 2
    message_2 = SubMessage("Brave Lion!")
    permutation_2 = "uiaeo"
    enc_dict_2 = message_2.build_transpose_dict(permutation_2)
    print("Original message:", message_2.get_message_text(), "Permutation:", permutation_2)
    print("Expected encryption:", "Bruvi Laen!")
    print("Actual encryption:", message_2.apply_transpose(enc_dict_2)) # Output: Bruvi Laen!
    enc_message_2 = EncryptedSubMessage(message_2.apply_transpose(enc_dict_2))
    print("Encoded message: ", enc_message_2.get_message_text())
    print("Decrypted message:", enc_message_2.decrypt_message()) #will vary with different runs as there as code bring
    # different permutation that has a max number of real words.
