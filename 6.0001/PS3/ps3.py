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

WORDLIST_FILENAME = "words.txt"


def deal_hand(n):
    hand = {}
    num_vowels = int(math.ceil(n / 3))

    asterisk_index = random.randrange(num_vowels)
    for i in range(num_vowels):
        if i == asterisk_index:
            x = "*"
        else:
            x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def load_words():
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
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    word = word.lower()
    word_length = len(word)
    first_part = 0

    for i in word:
        letter_score = SCRABBLE_LETTER_VALUES.get(i, 0)
        first_part += letter_score

    second_part = max(7 * word_length - 3 * (n - word_length), 1)

    score = second_part * first_part
    if len(word) == 0:
        return 0
    else:
        return score


def display_hand(hand):
    string = ""
    for letter in hand.keys():
        for j in range(hand[letter]):
            string += letter
            string += " "
    return string


def update_hand(hand, word):
    word = word.lower()
    deleted_letters = []
    updated_hand = hand.copy()
    for i in word:
        if i in updated_hand:
            if i in deleted_letters:
                continue
            else:
                deleted_letters.append(i)
                updated_hand[i] -= word.count(i)
    return updated_hand


def is_valid_word(word, hand, word_list):
    hand_copy = hand.copy()
    for letter in word:
        if letter == "*":
            replaceable = False
            for vowel in VOWELS:
                replaced = word.replace("*", vowel)
                if replaced in word_list:
                    replaceable = True
                    break
            if not replaceable:
                return False
        elif letter not in hand_copy or hand_copy[letter] == 0:
            return False
        else:
            hand_copy[letter] -= 1
    return True


def calculate_handlen(hand):
    return len(hand)


def play_hand(hand, word_list):
    total_points = 0
    playing = True
    subbed = False

    while playing:
        print("Current hand:", display_hand(hand))

        if not subbed:
            sub = input("Would you like to substitute a letter: ").lower()
            if sub == "yes":
                letter = input("Which letter would you like to replace: ")
                substitute_hand(hand, letter)
            subbed = True

        display_hand(hand)

        word = input("Enter a word or \"!!\" to indicate that you are finished: ")
        if word == "!!":
            break
        else:
            valid = is_valid_word(word, hand, word_list)
            if valid:
                score = get_word_score(word, HAND_SIZE)
                total_points += score
                print("\"" + word + "\"", "earned ", score, "points. Total:", total_points)
                hand = update_hand(hand, word)
                print()
            else:
                print("That isn't a valid word. Try again")
                print()
                continue

    print("Total score for this hand:", total_points, "points")
    print("_____________________")
    return total_points


def substitute_hand(hand, letter):
    hand_list = list(hand)
    print("Before", hand)
    if letter in hand:
        random_letter = random.choice(string.ascii_lowercase)
        while random_letter in hand:
            random_letter = random.choice(string.ascii_lowercase)
        key_to_replace = random.choice(hand_list)
        print("Random letter:", random_letter)
        print("Key to replace:", key_to_replace)

        while key_to_replace == "*":
            key_to_replace = random.choice(hand_list)
        value = hand[key_to_replace]
        hand[random_letter] = value
        del hand[key_to_replace]

    else:
        print("That letter isn't in your hand.")

    print("After:", hand)


def play_game(word_list):
    count = 0
    dictionaries = []
    total_points = 0

    hand_size = int(input("Enter total number of hands: "))
    for i in range(hand_size):
        hand = deal_hand(HAND_SIZE)
        dictionaries.append(hand)

    while True:
        current_dictionary = dictionaries[count]
        total_points += play_hand(current_dictionary, word_list)
        replay = input("Would you like to replay the hand: ").lower()

        if replay == "yes":
            play_hand(current_dictionary, word_list)
        else:
            count += 1
            if count == len(dictionaries):
                break
            else:
                continue

    print("_____________________")
    print("Total score over all hands:", total_points)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
