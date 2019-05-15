from string import ascii_letters

DATA_FILE = "../data/melville-moby_dick.txt"
SET_SIZE = 100

# Generate usible plain text training data from text file:
input_chars = []
plain_text_sets = []

with open(DATA_FILE) as inf:
    for line in inf:
        for char in [ch.lower() for ch in line]:
            if char in ascii_letters:
                input_chars.append(char)

for idx in range(0, len(input_chars), SET_SIZE):
    plain_text_sets.append(tuple(input_chars[idx:idx + SET_SIZE]))
del plain_text_sets[-1]
