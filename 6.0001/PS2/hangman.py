import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    common_letters = []

    for i in secret_word:
        if i in letters_guessed:
            common_letters.append(i)

    print(common_letters)
    print(len(common_letters), len(secret_word))
    return len(common_letters) >= len(secret_word)


def get_guessed_word(secret_word, letters_guessed):

    word_arr = []
    for x in secret_word:
        guessed = False
        for y in letters_guessed:
            if x == y:
                guessed = True
                continue
        if guessed:
            word_arr.append(x)
        else:
            word_arr.append('_')

    return " ".join(word_arr)


def get_available_letters(letters_guessed):
    lowercase = string.ascii_lowercase

    for i in lowercase:
        if i in letters_guessed:
            lowercase = lowercase.replace(i, "")

    return lowercase
    

def hangman(secret_word):
    letters = string.ascii_lowercase + string.ascii_uppercase
    vowels = "aeiou"
    guesses = 6
    count = 0
    warnings = 0
    letters_guessed = []
    guessing = True
    print("I am thinking of a word that is", len(secret_word), "letters long")

    while guessing and guesses > 0:
        if guesses == 1:
            print('You have 1 guess left')
        else:
            print("You have", guesses, "guesses left.")

        print("Available letters: ", get_available_letters(letters_guessed))
        guess = input("Enter a letter: ").lower()

        if guess in letters_guessed:
            warnings += 1
            print("You guessed this letter already. This is warning", warnings, "out of 3.")
            if warnings >= 3:
                print("You are out of warnings. You have lost a guess")
                guesses -= 1
            continue

        if guess not in letters:
            print("You can only enter letters. Try again")
            continue
        else:
            letters_guessed.insert(count, guess)

        if guess in secret_word:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                print("____________")
                print("You got it!")
                guessing = False
        else:
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            if guess in vowels:
                guesses -= 2
            else:
                guesses -= 1

        count += 1

    if guesses == 0:
        print("Sorry, you ran out of guesses. The word was:", secret_word)


def match_with_gaps(my_word, other_word):
    my_word = my_word.replace(' ', '')
    same = None
    combined = zip(my_word, other_word)
    for (a, b) in combined:
        if len(my_word) != len(other_word):
            same = False
        else:
            if a != '_' and a != b:
                same = False
            elif a == '_' and b in my_word:
                same = False
            else:
                continue
    if same is None:
        return True
    else:
        return False


def show_possible_matches(my_word):
    my_word = my_word.replace(' ', '')
    words = ""

    for word in wordlist:
        if match_with_gaps(my_word, word):
            words += word + " "

    print(words)


def hangman_with_hints(secret_word):
    letters = string.ascii_lowercase + string.ascii_uppercase
    vowels = "aeiou"
    guesses = 6
    count = 0
    warnings = 0
    letters_guessed = []
    player_word = ""
    guessing = True

    print("I am thinking of a word that is", len(secret_word), "letters long")

    while guessing and guesses > 0:
        if guesses == 1:
            print('You have 1 guess left')
        else:
            print("You have", guesses, "guesses left.")

        print("Available letters: ", get_available_letters(letters_guessed))
        guess = input("Enter a letter: ").lower()

        if guess in letters_guessed:
            warnings += 1
            print("You guessed this letter already. This is warning", warnings, "out of 3.")
            if warnings >= 3:
                print("You are out of warnings. You have lost a guess")
                guesses -= 1
            continue

        if guess not in letters:
            if guess == "*":
                print("Possible word matches are: ")
                player_word = get_guessed_word(secret_word, letters_guessed).replace(' ', '')
                print(player_word)
                show_possible_matches(player_word)
                print("__________________")
            else:
                print("You can only enter letters. Try again")
            continue
        else:
            letters_guessed.insert(count, guess)

        if guess in secret_word:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            if is_word_guessed(secret_word, letters_guessed):
                print("____________")
                print("You got it!")
                guessing = False
        else:
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            if guess in vowels:
                guesses -= 2
            else:
                guesses -= 1

        count += 1

    if guesses == 0:
        print("Sorry, you ran out of guesses. The word was:", secret_word)


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word)
    # hangman_with_hints(secret_word)

