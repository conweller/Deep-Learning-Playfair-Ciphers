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


def generate_cipher_text(key, plain_text):
    """
    Generates the cipher text for given key and plain_text

    Arguments:
        key: 5 x 5 array of unique letters not including 'j'
        plain_text: String of characters to be ciphered
    Returns:
        String of the ciphered plain_text using the inputted key
    """
    # TODO: actually cipher the text
    return plain_text
