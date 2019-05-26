"""Contains code to build the learning system"""
import pickle
import training_data as td


# =========================== READ IN TRAING DATA ============================
# Default datafile
DATA_FILE = '../data/melville-moby_dick.txt' 
# Size of each chunk of training data, must be even
SUBSET_SZ = 100

# TRAINING: list of size SUBSET_SZ of tuples of deciphered text, enciphered
#   text, and cipher keys in that order
TRAINING = []

# SERIALIZE_NAME: serialized training data
SERIALIZE_NAME = 'training.pickle'

# If serialized file exists, use that, otherwise read in the training data
#   from the DATA_FILE and serialize the result
try:
    with open(SERIALIZE_NAME, 'rb') as inf:
        TRAINING = pickle.load(inf)
except IOError:
    TRAINING = td.generate_data(DATA_FILE, SUBSET_SZ)
    with open(SERIALIZE_NAME, 'wb') as outf:
        pickle.dump(TRAINING, outf)
        outf.close()
