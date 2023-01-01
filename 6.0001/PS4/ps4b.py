import string

wordlist = []

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # inFile: file
    inFile = open(file_name, 'r')
    global wordlist
    # wordlist: list of strings
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
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
    # True
    # >>> is_word(word_list, 'asdf') returns
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

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        word_list = load_words(WORDLIST_FILENAME)
        self.text = text
        self.valid_words = []
        copy_words = list(self.text.split(" "))
        for word in copy_words:
            if is_word(word_list, word):
                self.valid_words.append(word)

    def get_message_text(self):
        return self.text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy_valid_words = self.valid_words.copy()
        return copy_valid_words

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
        shift_dict = {}

        for letter in string.ascii_lowercase:
            shifted_letter = chr((ord(letter) - ord('a') + shift) % 26 + ord('a'))
            shift_dict[letter] = shifted_letter

        for letter in string.ascii_uppercase:
            shifted_letter = chr((ord(letter) - ord('A') + shift) % 26 + ord('A'))
            shift_dict[letter] = shifted_letter

        return shift_dict

    def apply_shift(self, shift):
        shift_dict = self.build_shift_dict(shift)
        shifted_message = ""

        for letter in self.text:
            if letter == " ":
                shifted_message += " "
            else:
                shifted_letter = shift_dict.get(letter, letter)
                shifted_message += shifted_letter

        return shifted_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        super(Message, self).__init__(self, text)
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
        self.message_text = text
        self.valid_words = []
        copy_words = list(self.text.split(" "))
        word_list = load_words(WORDLIST_FILENAME)
        for word in copy_words:
            if is_word(word_list, word):
                self.valid_words.append(word)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.text.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        Returns: self.shift
        '''

        return self.shift

    def get_encryption_dict(self):
        copy_encryption_dict = self.encryption_dict.copy()
        return copy_encryption_dict

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        """
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        """
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.text.apply_shift(self, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        super().__init__(text)
        self.text = text
        self.valid_words = []
        copy_words = list(self.text.split(" "))
        word_list = load_words(WORDLIST_FILENAME)
        for word in copy_words:
            if is_word(word_list, word):
                self.valid_words.append(word)

    def decrypt_message(self):
        attempts = {}

        encrypted = Message(self.text)
        for i in range(1, 27):
            shift = i % 26
            new_encrypt = Message(encrypted.apply_shift(shift))
            attempts[shift] = new_encrypt.valid_words

        best_shift = None
        best_words = []
        for shift, words in attempts.items():
            if len(words) > len(best_words):
                best_shift, best_words = shift, words

        if not best_words:
            return None, ''
        else:
            return best_shift, best_words[0]


if __name__ == '__main__':
    print("Testing")
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Test with a message that can't be decrypted
    print("Testing with a message that can't be decrypted:")
    ciphertext = CiphertextMessage('abcdefghijklmnopqrstuvwxyz')
    print("Expected Output:", (None, ''))
    actual_output = ciphertext.decrypt_message()
    print("Actual Output:", actual_output)

    # Test with a message that contains only digits
    print("Testing with a message that contains only digits:")
    ciphertext = CiphertextMessage('0123456789')
    print("Expected Output:", (None, ''))
    actual_output = ciphertext.decrypt_message()
    print("Actual Output:", actual_output)

