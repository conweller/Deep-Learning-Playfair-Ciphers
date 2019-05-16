"""Contains methods for the generation of cipher text and cipher keys"""
from random import shuffle
from string import ascii_lowercase


def generate_key():
    """
    Creates a key table to encipher and decipher plain text
    Returns:
        The 5 x 5 array of unique letters (not containing 'j'), stored in a 1
        dimensional array
    """
    arr = list(ascii_lowercase)
    shuffle(arr)
    arr.remove('j')
    return arr


def encipher_text(key, plain_text):
    """
    Generates the cipher text for given key and plain_text

    Arguments:
        key: 5 x 5 array of unique letters not including 'j'
        plain_text: String of characters to be enciphered
    Returns:
        String of the enciphered plain_text using the inputted key
    """
    cipher_text = ""
    for i in range(0, len(plain_text), 2):
        # get current char pair, change j's to i's
        ch1 = plain_text[i] if plain_text[i] != 'j' else 'i'
        ch2 = plain_text[i+1] if plain_text[i+1] != 'j' else 'i'

        # 1. If both letters are the same, make second 'x' and continue
        if ch1 == ch2:
            ch2 = 'x'
        idx1 = key.index(ch1)
        idx2 = key.index(ch2)

        # 2. If letters are on same row replace each with letter to the right
        #   on row, wrapping around the left side if necessary
        if idx1 // 5 == idx2 // 5:
            for idx in (idx1, idx2):
                cipher_text += key[idx // 5 * 5 + ((idx + 1) % 5)]

        # 3. Else if letters are in the same column replace with the letters
        #   below wrapping to top if necessary
        elif idx1 % 5 == idx2 % 5:
            for idx in (idx1, idx2):
                cipher_text += key[idx % 5 + 5 * (((idx // 5) + 1) % 5)]

        # 4. If letters are not in the same row or column, replace each using
        #   the rectangle defined by their positions, replace each letter using
        #   with the letter in the same row but the opposite corner to that
        #   letter
        else:
            cipher_text += key[
                idx1 % 5 + (idx2 % 5 - idx1 % 5) + (idx1 // 5 * 5)
            ]
            cipher_text += key[
                idx2 % 5 + (idx1 % 5 - idx2 % 5) + (idx2 // 5 * 5)
            ]
    return cipher_text
