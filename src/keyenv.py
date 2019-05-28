"""Contain KeyState Class"""
import cipher
GOOD_SQR_REWARD = 10


class KeyState:
    """The current state of the key being built

    Attributes:
        avbl: list of available key indexes
        avbl_row: list of 5 numbers representing the number of available
            indexes in the row corresponding to the index in the list
        avbl_col: list of 5 numbers representing the number of available
            indexes in the column corresponding to the index in the list
        used: dictionary of used characters and the key indexes they occupy
        decp_txt: deciphered text
        encp_txt: enciphered text
        key: key used to encipher the deciphered text
        txt_idx: location in the enciphered and deciphered strings we are
            currently
    """

    # Vector representation of actions:
    ACT_ROW = [0, 0, 1]
    ACT_COL = [0, 1, 0]
    ACT_SQR = [1, 0, 0]

    def __init__(self, decp_txt, encp_txt, key):
        self.avbl = list(range(0, 25))
        self.avbl_row = [5]*5
        self.avbl_col = [5]*5
        self.used = {}
        self.decp_txt = decp_txt
        self.encp_txt = encp_txt
        self.key = key
        self.txt_idx = 0

    def add_char(self, char, idx):
        """
        Adds character to given index, removes the index from available lists
        Arguments:
            char: inputed character
            idx: index in the key
        """
        self.avbl.remove(idx)
        self.avbl_row[idx // 5] -= 1
        self.avbl_col[idx % 5] -= 1
        self.used[char] = idx

    def get_key(self):
        """
        Returns used dictionary as a list representation of a key, with the
            character ' ' denoting an unused spot in the key
        """
        key_arr = [' ']*25
        for char in self.used.keys():
            key_arr[self.used[char]] = char
        cipher.print_key(key_arr)
        # return key_arr

    def check_avbl(self):
        """
        Returns the number of the current set of 4 encp_txt and decp_txt
            characters that are not already in the key being built
        """
        cur_text = self.decp_txt[self.txt_idx: self.txt_idx + 2]
        cur_text += self.encp_txt[self.txt_idx: self.txt_idx + 2]
        return set(cur_text).difference(self.used.keys())

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

# The following function is kind of ridiculous, but it works and would've been
#   difficult to implement in a different manner
    def action_square(self):
        """
        Makes a square action

        Returns:
            Reward for the given action
        """
        avbl_chars = self.check_avbl()
        d1 = self.decp_txt[self.txt_idx]
        d2 = self.decp_txt[self.txt_idx+1]
        e1 = self.encp_txt[self.txt_idx]
        e2 = self.encp_txt[self.txt_idx+1]
        print(d1)
        print(d2)
        if not avbl_chars:
            print("all chars used")
            return -12242134
        rows = enumerate(self.avbl_row)
        rows = list([r for r in rows if r[1] > 1])
        rows.sort(key=lambda tup: tup[1])
        cols = enumerate(self.avbl_col)
        cols = list([c for c in cols if c[1] > 1])
        cols.sort(key=lambda tup: tup[1])
        if len(avbl_chars) == 4:
            for i in range(len(rows)-1):
                max_row1 = rows[-1-i][0]
                for j in range(len(rows)-i-1):
                    max_row2 = rows[-2-i-j][0]
                    for k in range(len(cols)-1):
                        max_col1 = cols[-1-k][0]
                        for l in range(len(cols)-k-1):
                            max_col2 = cols[-2-k-l][0]
                            we_good = (max_row1 * 5) + max_col1 in self.avbl
                            we_good &= (max_row1 * 5) + max_col2 in self.avbl
                            we_good &= (max_row2 * 5) + max_col1 in self.avbl
                            we_good &= (max_row2 * 5) + max_col2 in self.avbl
                            if we_good:
                                self.add_char(d1, (max_row1*5) + max_col1)
                                self.add_char(e1, (max_row1*5) + max_col2)
                                self.add_char(d2, (max_row2*5) + max_col2)
                                self.add_char(e2, (max_row2*5) + max_col1)
                                self.txt_idx += 2
                                return GOOD_SQR_REWARD
        if len(avbl_chars) == 3:
            if e1 not in avbl_chars:
                row_used = self.used[e1] // 5
                col_used = self.used[e1] % 5
                if self.avbl_row[row_used]==0 or self.avbl_col[col_used]==0:
                    return
                max_row1 = row_used
                max_col2 = col_used
                for i in range(len(rows)-1):
                    max_row2 = rows[-1-i][0]
                    if max_row2 != max_row1:
                        for k in range(len(cols)-1):
                            max_col1 = cols[-1-k][0]
                            if max_col2 != max_col1:
                                we_good = (max_row1 * 5) + max_col1 in self.avbl
                                # we_good &= (max_row1 * 5) + max_col2 in self.avbl
                                we_good &= (max_row2 * 5) + max_col1 in self.avbl
                                we_good &= (max_row2 * 5) + max_col2 in self.avbl
                                if we_good:
                                    self.add_char(d1, (max_row1*5) + max_col1)
                                    # self.add_char(e1, (max_row1*5) + max_col2)
                                    self.add_char(d2, (max_row2*5) + max_col2)
                                    self.add_char(e2, (max_row2*5) + max_col1)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
            if e2 not in avbl_chars:
                row_used = self.used[e2] // 5
                col_used = self.used[e2] % 5
                if self.avbl_row[row_used]==0 or self.avbl_col[col_used]==0:
                    return
                max_row2 = row_used
                max_col1 = col_used
                for i in range(len(rows)-1):
                    max_row1 = rows[-1-i][0]
                    if max_row2 != max_row1:
                        for k in range(len(cols)-1):
                            max_col2 = cols[-1-k][0]
                            if max_col2 != max_col1:
                                we_good = (max_row1 * 5) + max_col1 in self.avbl
                                we_good &= (max_row1 * 5) + max_col2 in self.avbl
                                # we_good &= (max_row2 * 5) + max_col1 in self.avbl
                                we_good &= (max_row2 * 5) + max_col2 in self.avbl
                                if we_good:
                                    self.add_char(d1, (max_row1*5) + max_col1)
                                    self.add_char(e1, (max_row1*5) + max_col2)
                                    self.add_char(d2, (max_row2*5) + max_col2)
                                    # self.add_char(e2, (max_row2*5) + max_col1)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
            if d1 not in avbl_chars:
                row_used = self.used[d1] // 5
                col_used = self.used[d1] % 5
                if self.avbl_row[row_used]==0 or self.avbl_col[col_used]==0:
                    return
                max_row1 = row_used
                max_col1 = col_used
                for i in range(len(rows)-1):
                    max_row2 = rows[-1-i][0]
                    if max_row2 != max_row1:
                        for k in range(len(cols)-1):
                            max_col2 = cols[-1-k][0]
                            if max_col2 != max_col1:
                                # we_good = (max_row1 * 5) + max_col1 in self.avbl
                                we_good = (max_row1 * 5) + max_col2 in self.avbl
                                we_good &= (max_row2 * 5) + max_col1 in self.avbl
                                we_good &= (max_row2 * 5) + max_col2 in self.avbl
                                if we_good:
                                    # self.add_char(d1, (max_row1*5) + max_col1)
                                    self.add_char(e1, (max_row1*5) + max_col2)
                                    self.add_char(d2, (max_row2*5) + max_col2)
                                    self.add_char(e2, (max_row2*5) + max_col1)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
            if d2 not in avbl_chars:
                row_used = self.used[d2] // 5
                col_used = self.used[d2] % 5
                if self.avbl_row[row_used]==0 or self.avbl_col[col_used]==0:
                    return
                max_row2 = row_used
                max_col2 = col_used
                for i in range(len(rows)-1):
                    max_row1 = rows[-1-i][0]
                    if max_row2 != max_row1:
                        for k in range(len(cols)-1):
                            max_col1 = cols[-1-k][0]
                            if max_col2 != max_col1:
                                we_good = (max_row1 * 5) + max_col1 in self.avbl
                                we_good &= (max_row1 * 5) + max_col2 in self.avbl
                                we_good &= (max_row2 * 5) + max_col1 in self.avbl
                                # we_good &= (max_row2 * 5) + max_col2 in self.avbl
                                if we_good:
                                    self.add_char(d1, (max_row1*5) + max_col1)
                                    self.add_char(e1, (max_row1*5) + max_col2)
                                    # self.add_char(d2, (max_row2*5) + max_col2)
                                    self.add_char(e2, (max_row2*5) + max_col1)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
        if len(avbl_chars) == 2:
            if e1 not in avbl_chars and e2 not in avbl_chars:
                row_used1 = self.used[e1] // 5
                col_used1 = self.used[e1] % 5
                row_used2 = self.used[e2] // 5
                col_used2 = self.used[e2] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if col_used1 == col_used2:
                    return
                if row_used1 == row_used2:
                    return
                max_row1 = row_used1
                max_col2 = col_used1
                max_row2 = row_used2
                max_col1 = col_used2
                we_good = (max_row1 * 5) + max_col1 in self.avbl
                # we_good &= (max_row1 * 5) + max_col2 in self.avbl
                # we_good &= (max_row2 * 5) + max_col1 in self.avbl
                we_good &= (max_row2 * 5) + max_col2 in self.avbl
                if we_good:
                    self.add_char(d1, (max_row1*5) + max_col1)
                    # self.add_char(e1, (max_row1*5) + max_col2)
                    self.add_char(d2, (max_row2*5) + max_col2)
                    # self.add_char(e2, (max_row2*5) + max_col1)
                    self.txt_idx += 2
                    return GOOD_SQR_REWARD
            if d1 not in avbl_chars and d2 not in avbl_chars:     # untested 5/27
                row_used1 = self.used[d1] // 5
                col_used1 = self.used[d1] % 5
                row_used2 = self.used[d2] // 5
                col_used2 = self.used[d2] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if col_used1 == col_used2:
                    return
                if row_used1 == row_used2:
                    return
                max_row1 = row_used1
                max_col2 = col_used1
                max_row2 = row_used2
                max_col1 = col_used2
                we_good = (max_row1 * 5) + max_col1 in self.avbl
                # we_good &= (max_row1 * 5) + max_col2 in self.avbl
                # we_good &= (max_row2 * 5) + max_col1 in self.avbl
                we_good &= (max_row2 * 5) + max_col2 in self.avbl
                if we_good:
                    # self.add_char(d1, (max_row1*5) + max_col1)
                    self.add_char(e1, (max_row1*5) + max_col1)
                    # self.add_char(d2, (max_row2*5) + max_col2)
                    self.add_char(e2, (max_row2*5) + max_col2)
                    self.txt_idx += 2
                    return GOOD_SQR_REWARD
            if d1 not in avbl_chars and e1 not in avbl_chars:     # untested 5/27
                row_used1 = self.used[d1] // 5
                col_used1 = self.used[d1] % 5
                row_used2 = self.used[e1] // 5
                col_used2 = self.used[e1] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if col_used1 == col_used2:
                    return
                if row_used1 == row_used2:
                    return
                if row_used1 == row_used2:
                    max_row1 = row_used1
                    max_col1 = col_used1  # d1
                    max_col2 = col_used2  # e1
                    for i in range(len(rows)-1):
                        max_row2 = rows[-1-i][0]
                        we_good = (max_row2 * 5) + max_col1 in self.avbl
                        we_good &= (max_row2 * 5) + max_col2 in self.avbl
                        if we_good:
                            # self.add_char(d1, (max_row1*5) + max_col1)
                            self.add_char(d2, (max_row2*5) + max_col2)
                            # self.add_char(d2, (max_row2*5) + max_col2)
                            self.add_char(e2, (max_row2*5) + max_col1)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD
            if d1 not in avbl_chars and e2 not in avbl_chars:  #untested 5/27
                row_used1 = self.used[d1] // 5
                col_used1 = self.used[d1] % 5
                row_used2 = self.used[e2] // 5
                col_used2 = self.used[e2] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if col_used1 == col_used2:
                    return
                if row_used1 == row_used2:
                    return
                if col_used1 == col_used2:
                    max_col1 = col_used1
                    max_row1 = row_used1  # d1
                    max_row2 = row_used2  # e2
                    for i in range(len(cols-1)):
                        max_col2 = cols[-1-i][0]
                        we_good = (max_row1 * 5) + max_col1 in self.avbl
                        we_good &= (max_row2 * 5) + max_col2 in self.avbl
                        if we_good:
                            # self.add_char(d1, (max_row1*5) + max_col1)
                            self.add_char(e1, (max_row1*5) + max_col2)
                            # self.add_char(d2, (max_row2*5) + max_col2)
                            self.add_char(d2, (max_row2*5) + max_col2)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD        

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
    # There is three actions (currently) column, row, and square add
    action_size = 3
    learning_rate = .002        # Alpha

    # TRAINING
    # I just picked a big number, I dont know how many we want to do
    total_episodes = 1000

    # EXPLORATION
    # alright all these variable names are kind of self explanatory
    explore_start = 1.0
    explore_stop = 0.01
    decay_right = 0.0001

    # Q Learning hyper parameters
    gamma = 0.95

    # Memory HyperParemeters
    memory_size = 1000000

    # Training?
    training = True
