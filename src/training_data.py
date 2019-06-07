"""Houses method to read in and format training data"""
from string import ascii_lowercase
from cipher import encipher_text, decipher_text, generate_key

def generate_data(filename, subset_sz):
    """
    Creates list of training data tuples (each containing deciphered text,
        enciphered text, and cipher keys) from file containing plain_text

    Arguments:
        filename: string path to a text file
        subset_sz: size of each chunk of text in the returned training data
    Returns:
        list of size SUBSET_SZ of tuples of deciphered text, enciphered
        text, and cipher keys in that order
    """
    input_chars = ""

    # plain_text: List of strings containing <SUBSET_SZ> characters from
    #   INPUT_CHARS
    plain_text = []

    with open(filename) as inf:
        for line in inf:
            for char in line:
                char = char.lower()
                if char in ascii_lowercase:
                    input_chars += char

    for idx in range(0, len(input_chars), subset_sz):
        plain_text.append((input_chars[idx:idx + subset_sz]))
    del plain_text[-1]

    # training: list of size SUBSET_SZ of tuples of deciphered text, enciphered
    #   text, and cipher keys in that order
    training = []

    for text in plain_text:
        key = generate_key()
        cipher_text = encipher_text(key, text)
        training.append((decipher_text(key, cipher_text), cipher_text, key))
    return training
