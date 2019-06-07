"""Contains code to build the learning system"""
import training_data as td
import numpy as np
import pickle
import agent
import keyenv


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

# =========================== TRAIN OUR SYSTEM ================================
# EPISODES: The number of times we train the agent
EPISODES = 9000

# INPUT_DIM: The input data dimensions for our neural net
#   25 spaces in the key, and 4 letters of input text = 29
INPUT_DIM = 29

# OUTPUT_DIM: The output dimensions for our neural net
#   the 3 possible actions
OUTPUT_DIM = 3

# BATCH_SIZE: The number size of memory looked at during training
BATCH_SIZE = 32

# AGENT: The agent taking actions to build a key
AGENT = agent.OurAgent(INPUT_DIM, OUTPUT_DIM)

# DONE: Boolean indiating if our agent reached a terminal state
DONE = False
sum = 0
for idx in range(EPISODES):
    # ken: Key environment, i.e. the current state of the key being built
    ken = keyenv.KeyState(TRAINING[idx][0], TRAINING[idx][1])
    # ken = keyenv.KeyState(TRAINING[0][0], TRAINING[0][1])
    # state: array represntation of the current in progress key, cipher text, and decipher text
    state = np.reshape(ken.get_state(), (1, INPUT_DIM))
    while ken.txt_idx < SUBSET_SZ:
        action = AGENT.act(state)
        next_state, reward, done = ken.make_action(action)
        next_state = np.reshape(next_state, (1, INPUT_DIM))
        AGENT.store_state(state, action, reward, next_state, done)
        state = next_state
        if done:
            sum += ken.txt_idx
            AGENT.target_nnet.model.set_weights(AGENT.nnet.model.get_weights())
            if idx % 100 == 0 and idx > 0:
                print("Average = " + str(sum/100))
                sum = 0
            # print("Key:")
            # ken.print_key()
            # print("episode {} \n Key:\n{}".format(idx, ken.get_key()))
            break
        if len(AGENT.memory) > BATCH_SIZE:
            AGENT.train(BATCH_SIZE)
