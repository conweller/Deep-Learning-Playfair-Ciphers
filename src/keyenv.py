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

    def __init__(self, decp_txt, encp_txt):
        self.available = list(range(0, 25))
        self.used = {}
        self.decp_txt = decp_txt
        self.encp_txt = encp_txt
        self.loc = 0

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
            Reward for the given action
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
