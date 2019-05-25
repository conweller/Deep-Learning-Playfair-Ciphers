"""Contain KeyState Class"""


class KeyState:
    """The current state of the key being built

    Attributes:
        available: list of available key indexes
        used: dictionary of used characters and the key indexes they occupy
        decp_txt: deciphered text
        encp_txt: enciphered text
        loc: location in the enciphered and deciphered strings we are
            currently
    """

    # Vector representation of actions:
    ACT_ROW = [0, 0, 1]
    ACT_COL = [0, 1, 0]
    ACT_SQR = [1, 0, 0]

    def __init__(self, decp_txt, encp_txt, key):
        self.available = list(range(0, 25))
        self.used = {}
        self.decp_txt = decp_txt
        self.encp_txt = encp_txt
        self.loc = 0
        self.key = key  # Do we need to pass in the key here, I just added this -- chris

    def add_char(self, char, idx):
        """
        Adds character to given index
        Arguments:
            char: inputed character
            idx: index in the key
        """
        self.available.remove(idx)
        self.used[char] = idx

    def action_row(self):
        """
        Makes a row action

        Returns:
            Reward for the given action
        """
        print("row")

    def action_column(self):
        """
        Makes a column action

        Returns:
            Reward for the action
        """
        print("column")

    def action_square(self):
        """
        Makes a square action

        Returns:
            Reward for the given action
        """
        print("square")

    def make_action(self, act_vec):
        """
        Makes the action corresponding to the input, and returns the action's
            reward

        Arguments:
            act_vec: a vector representation of the action being made
        Returns:
            Reward for the given action
        """
        action = {
            str(KeyState.ACT_ROW): KeyState.action_row,
            str(KeyState.ACT_COL): KeyState.action_column,
            str(KeyState.ACT_SQR): KeyState.action_square
        }
        return action[str(act_vec)](self)
    
    # HYPERPAREMET SECTION

    # MODEL
    state_size = [50, 50]       # 50 plaintext pairs and 50 ciphertext pairs 
    action_size = 3             # There is three actions (currently) column, row, and square add
    learning_rate = .002        # Alpha
    
    # TRAINING
    total_episodes = 1000       # I just picked a big number, I dont know how many we want to do

    # EXPLORATION
    explore_start = 1.0         # alright all these variable names are kind of self explanatory
    explore_stop = 0.01
    decay_right = 0.0001

    # Q Learning hyper parameters
    gamma = 0.95

    # Memory HyperParemeters
    memory_size = 1000000

    # Training?
    training = True



    



