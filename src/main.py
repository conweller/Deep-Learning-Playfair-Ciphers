from string import ascii_letters

DATA_FILE = "../data/melville-moby_dick.txt"
SUBSET_SZ = 100

# ============ Generate plain text training data from text file ===============

# INPUT_CHARS: List of alphabetical characters in the input file
INPUT_CHARS = []

# PLAIN_TEXT: List of tuples containing <SUBSET_SZ> characters from INPUT_CHARS
PLAIN_TEXT = []

with open(DATA_FILE) as inf:
    for line in inf:
        for char in [ch.lower() for ch in line]:
            if char in ascii_letters:
                INPUT_CHARS.append(char)

for idx in range(0, len(INPUT_CHARS), SUBSET_SZ):
    PLAIN_TEXT.append(tuple(INPUT_CHARS[idx:idx + SUBSET_SZ]))
del PLAIN_TEXT[-1]
