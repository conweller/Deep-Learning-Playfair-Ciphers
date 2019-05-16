"""Contains builds system"""
from string import ascii_lowercase
from cipher import encipher_text, generate_key

DATA_FILE = '../data/melville-moby_dick.txt'

# Size of each chunk of training data, must be even
SUBSET_SZ = 100

# ============ Generate training data from text file ===============

# INPUT_CHARS: List of alphabetical characters in the input file
INPUT_CHARS = ""

# PLAIN_TEXT: List of strings containing <SUBSET_SZ> characters from
#   INPUT_CHARS
PLAIN_TEXT = []

with open(DATA_FILE) as inf:
    for line in inf:
        for char in line:
            char = char.lower()
            if char in ascii_lowercase:
                INPUT_CHARS += char

for idx in range(0, len(INPUT_CHARS), SUBSET_SZ):
    PLAIN_TEXT.append((INPUT_CHARS[idx:idx + SUBSET_SZ]))
del PLAIN_TEXT[-1]

# TRAINING: list of size SUBSET_SZ of tuples of plain text, cipher text, and
#   cipher keys in that order
TRAINING = []

for text in PLAIN_TEXT:
    key = generate_key()
    TRAINING.append((text, encipher_text(key, text), key))
