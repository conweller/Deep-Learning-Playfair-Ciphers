"""Contain KeyState Class"""
import cipher
import random
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
        avbl_chars = self.check_avbl()
        d1 = self.decp_txt[self.txt_idx]
        d2 = self.decp_txt[self.txt_idx+1]
        e1 = self.encp_txt[self.txt_idx]
        e2 = self.encp_txt[self.txt_idx+1]
        if not avbl_chars:
            print("all chars used")
            return -12242134
        cols = enumerate(self.avbl_col)
        if len(avbl_chars) == 4:
            # in this case columns are only usisble if they have > 3 open spots
            cols = list([c for c in cols if c[1] > 3])
            cols.sort(key=lambda tup: tup[1])
            for i in range(len(cols)):
                max_col = cols[-1-i][0]
                cur_col = list([s for s in self.avbl if s % 5 == max_col])
                valid_placements = []
                # check what spot (if any) is being used in max col, then
                # randomize where we place things
                if len(cur_col) == 5:
                    for idx in range(0, 5):
                        valid_placements.append((idx, (idx+2) % 5))
                        valid_placements.append((idx, (idx+3) % 5))
                else:
                    for j in range(0, 5):
                        if max_col + (j*5) not in cur_col:
                            valid_placements.append(((j+1)%5, (j+3)%5))
                            valid_placements.append(((j+3)%5, (j+1)%5))
                placement = random.choice(valid_placements)
                self.add_char(d1, placement[0] * 5 + max_col)
                self.add_char(e1, ((placement[0] + 1) % 5) * 5 + max_col)
                self.add_char(d2, placement[1] * 5 + max_col)
                self.add_char(e2, ((placement[1] + 1) % 5) * 5 + max_col)
                self.txt_idx += 2
                return GOOD_SQR_REWARD
        if len(avbl_chars) == 3:
            cols = list([c for c in cols if c[1] > 2])
            cols.sort(key=lambda tup: tup[1])
            if len(set([d1, d2, e1, e2])) == 3:
                # e1 cant possibly equal e2 and d1 cant equal d2 because of how
                #   the cipher works
                if d1 == e1:
                    return -123412341
                elif d2 == e2:
                    return -123412341
                elif d1 == e2:
                    for i in range(len(cols)):
                        max_col = cols[-1-i][0]
                        cur_col = list([s for s in self.avbl if s % 5 == max_col])
                        valid_placements = []
                        # check what spot (if any) is being used in max col, then
                        # randomize where we place things
                        if len(cur_col) == 5:
                            for idx in range(0, 5):
                                valid_placements.append((idx, (idx+4) % 5))
                        if len(cur_col) == 4:
                            for j in range(0, 5):
                                if max_col + (j*5) not in cur_col:
                                    valid_placements.append((j+2) % 5, (j+1) % 5)
                                    valid_placements.append((j+3) % 5, (j+2) % 5)
                        if len(cur_col) == 3:
                            for j in range(0, 5):
                                if max_col + (j*5) not in cur_col:
                                    if max_col + (((j+1)%5)*5) not in cur_col:
                                        valid_placements.append((j+3) % 5, (j+2) % 5)
                                    if max_col + (((j+4)%5)*5) not in cur_col:
                                        valid_placements.append((j+2) % 5, (j+1) % 5)
                        if valid_placements != []:
                            placement = random.choice(valid_placements)
                            self.add_char(d1, placement[0] * 5 + max_col)
                            self.add_char(e1, ((placement[0] + 1) % 5) * 5 + max_col)
                            self.add_char(d2, placement[1] * 5 + max_col)
                            # self.add_char(e2, ((placement[1] + 1) % 5) * 5 + max_col)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD
                        # if len(cur_col) == 4:
                elif d2 == e1:
                    for i in range(len(cols)):
                        max_col = cols[-1-i][0]
                        cur_col = list([s for s in self.avbl if s % 5 == max_col])
                        valid_placements = []
                        # check what spot (if any) is being used in max col, then
                        # randomize where we place things
                        if len(cur_col) == 5:
                            for idx in range(0, 5):
                                valid_placements.append((idx, (idx+1) % 5))
                        if len(cur_col) == 4:
                            if max_col not in cur_col:  # first in col
                                valid_placements.append((1, 2))
                                valid_placements.append((2, 3))
                            if max_col + 5 not in cur_col:  # Second in col
                                valid_placements.append((2, 3))
                                valid_placements.append((3, 4))
                            if max_col + 10 not in cur_col:  # third in col
                                valid_placements.append((3, 4))
                                valid_placements.append((4, 0))
                            if max_col + 15 not in cur_col:  # fourth in col
                                valid_placements.append((4, 0))
                                valid_placements.append((0, 1))
                            if max_col + 20 not in cur_col:  # fifth in col
                                valid_placements.append((0, 1))
                                valid_placements.append((1, 2))
                        if len(cur_col) == 3:
                            if max_col not in cur_col:  # first in col
                                if max_col + 5 not in cur_col:
                                    valid_placements.append((2, 3))
                                elif max_col + 20 not in cur_col:
                                    valid_placements.append((1, 2))
                            if max_col + 5 not in cur_col:  # Second in col
                                if max_col not in cur_col:
                                    valid_placements.append((2, 3))
                                if max_col + 10 not in cur_col:
                                    valid_placements.append((3, 4))
                            if max_col + 10 not in cur_col:  # third in col
                                if max_col + 15 not in cur_col:
                                    valid_placements.append((4, 0))
                                if max_col + 5 not in cur_col:
                                    valid_placements.append((3, 4))
                            if max_col + 15 not in cur_col:  # fourth in col
                                if max_col + 10 not in cur_col:
                                    valid_placements.append((4, 0))
                                if max_col + 20 not in cur_col:
                                    valid_placements.append((0, 1))
                            if max_col + 20 not in cur_col:  # fifth in col
                                if max_col + 15 not in cur_col:
                                    valid_placements.append((0, 1))
                                if max_col not in cur_col:
                                    valid_placements.append((1, 2))
                        if valid_placements != []:
                            placement = random.choice(valid_placements)
                            self.add_char(d1, placement[0] * 5 + max_col)
                            # self.add_char(e1, ((placement[0] + 1) % 5) * 5 + max_col)
                            self.add_char(d2, placement[1] * 5 + max_col)
                            self.add_char(e2, ((placement[1] + 1) % 5) * 5 + max_col)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD
            else:
                if d1 in self.used:
                    d1_idx = self.used[d1] % 5
                    d1_idx_in_col = self.used[d1] // 5
                    cur_col = list([s for s in self.avbl if s % 5 == d1_idx])
                    valid_placements = []
                    if len(cur_col) == 4:
                        for i in range(0, 5):
                            if d1_idx_in_col == i:
                                valid_placements.append((i, (i+2) % 5))
                                valid_placements.append((i, (i+3) % 5))
                    elif len(cur_col) == 3:
                        for i in range(0,5):
                            if d1_idx_in_col == i:
                                if ((i + 2)%5)*5 not in cur_col:
                                    valid_placements.append((i, (i+3) % 5))
                                if ((i + 4)%5)*5 not in cur_col:
                                    valid_placements.append((i, (i+2) % 5))
                    if valid_placements != []:
                        placement = random.choice(valid_placements)
                        # self.add_char(d1, placement[0] * 5 + d1_idx)
                        self.add_char(e1, ((placement[0] + 1) % 5) * 5 + d1_idx)
                        self.add_char(d2, placement[1] * 5 + d1_idx)
                        self.add_char(e2, ((placement[1] + 1) % 5) * 5 + d1_idx)
                        self.txt_idx += 2
                        return GOOD_SQR_REWARD
                elif d2 in self.used:
                    d2_idx = self.used[d2] % 5
                    d2_idx_in_col = self.used[d2] // 5
                    cur_col = list([s for s in self.avbl if s % 5 == d2_idx])
                    valid_placements = []
                    if len(cur_col) == 4:
                        for i in range(0, 5):
                            if d2_idx_in_col == i:
                                valid_placements.append(((i+2) % 5, i))
                                valid_placements.append(((i+3) % 5, i))
                    elif len(cur_col) == 3:
                        for i in range(0,5):
                            if d2_idx_in_col == i:
                                if ((i + 2)%5)*5 not in cur_col:
                                    valid_placements.append(((i+3) % 5, i))
                                if ((i + 4)%5)*5 not in cur_col:
                                    valid_placements.append(((i+2) % 5, i))
                    if valid_placements != []:
                        placement = random.choice(valid_placements)
                        self.add_char(d1, placement[0] * 5 + d2_idx)
                        self.add_char(e1, ((placement[0] + 1) % 5) * 5 + d2_idx)
                        # self.add_char(d2, placement[1] * 5 + d2_idx)
                        self.add_char(e2, ((placement[1] + 1) % 5) * 5 + d2_idx)
                        self.txt_idx += 2
                        return GOOD_SQR_REWARD
                elif e1 in self.used:
                    e1_idx = self.used[e1] % 5
                    e1_idx_in_col = self.used[e1] // 5
                    cur_col = list([s for s in self.avbl if s % 5 == e1_idx])
                    valid_placements = []
                    if len(cur_col) == 4:
                        for i in range(0, 5):
                            if e1_idx_in_col == i:
                                valid_placements.append(((i+4) % 5, (i+1) % 5))
                                valid_placements.append(((i+4) % 5, (i+2) % 5))
                    elif len(cur_col) == 3:
                        for i in range(0,5):
                            if e1_idx_in_col == i:
                                if ((i + 1)%5)*5 not in cur_col:
                                    valid_placements.append(((i+4) % 5, (i+2) % 5))
                                if ((i + 3)%5)*5 not in cur_col:
                                    valid_placements.append(((i+4) % 5, (i+1) % 5))
                    if valid_placements != []:
                        placement = random.choice(valid_placements)
                        self.add_char(d1, placement[0] * 5 + e1_idx)
                        # self.add_char(e1, ((placement[0] + 1) % 5) * 5 + e1_idx)
                        self.add_char(d2, placement[1] * 5 + e1_idx)
                        self.add_char(e2, ((placement[1] + 1) % 5) * 5 + e1_idx)
                        self.txt_idx += 2
                        return GOOD_SQR_REWARD
                elif e2 in self.used:
                    e2_idx = self.used[e2] % 5
                    e2_idx_in_col = self.used[e2] // 5
                    cur_col = list([s for s in self.avbl if s % 5 == e2_idx])
                    valid_placements = []
                    print(cur_col)
                    if len(cur_col) == 4:
                        for i in range(0, 5):
                            if e2_idx_in_col == i:
                                valid_placements.append(((i+1) % 5, (i+4) % 5))
                                valid_placements.append(((i+2) % 5, (i+4) % 5))
                    elif len(cur_col) == 3:
                        for i in range(0,5):
                            if e2_idx_in_col == i:
                                if ((i + 1)%5)*5 not in cur_col:
                                    valid_placements.append(((i+2) % 5, (i+4) % 5))
                                if ((i + 3)%5)*5 not in cur_col:
                                    valid_placements.append(((i+1) % 5, (i+4) % 5))
                    if valid_placements != []:
                        placement = random.choice(valid_placements)
                        self.add_char(d1, placement[0] * 5 + e2_idx)
                        self.add_char(e1, ((placement[0] + 1) % 5) * 5 + e2_idx)
                        self.add_char(d2, placement[1] * 5 + e2_idx)
                        # self.add_char(e2, ((placement[1] + 1) % 5) * 5 + e2_idx)
                        self.txt_idx += 2
                        return GOOD_SQR_REWARD
        if len(avbl_chars) == 2:
            if len(set([d1, d2, e1, e2])) == 3:
                if d1 == e1:
                    return -12342134123
                if e2 == d2:
                    return -1234123
                if d1 == e2:
                    if d1 in self.used:
                        if (self.used[d1] + 5) % 25 in self.avbl:
                            if (self.used[d1] + 20) % 25 in self.avbl:
                                self.add_char(d2, (self.used[d1] + 20) % 25)
                                self.add_char(e1, (self.used[d1] + 5) % 25)
                                self.txt_idx +=2
                                return GOOD_SQR_REWARD
                        return -1012432341
                    if d2 in self.used:
                        if (self.used[d2] + 5)%25 in self.avbl:
                            if (self.used[d2] + 10)%25 in self.avbl:
                                self.add_char(d1, (self.used[d2]+5) % 25)
                                self.add_char(e1, (self.used[d2]+10) % 25)
                                self.txt_idx +=2
                                return GOOD_SQR_REWARD
                            return -1012432341
                        return -1012432341
                    elif e1 in self.used:
                        if (self.used[e1] + 15)%25 in self.avbl:
                            if (self.used[e1] + 20)%25 in self.avbl:
                                self.add_char(d1, (self.used[e1]+20) % 25)
                                self.add_char(d2, (self.used[e1]+15) % 25)
                                self.txt_idx +=2
                                return GOOD_SQR_REWARD
                            return -1012432341
                        return -1012432341
                if d2 == e1:
                    if d2 in self.used:
                        if (self.used[d2] + 5) % 25 in self.avbl:
                            if (self.used[d2] + 20) % 25 in self.avbl:
                                self.add_char(d1, (self.used[d2] + 20) % 25)
                                self.add_char(e2, (self.used[d2] + 5) % 25)
                                self.txt_idx +=2
                                return GOOD_SQR_REWARD
                        return -1012432341
                    if d1 in self.used:
                        if (self.used[d1] + 5)%25 in self.avbl:
                            if (self.used[d1] + 10)%25 in self.avbl:
                                self.add_char(d2, (self.used[d1]+5) % 25)
                                self.add_char(e2, (self.used[d1]+10) % 25)
                                self.txt_idx +=2
                                return GOOD_SQR_REWARD
                            return -1012432341
                        return -1012432341
                    elif e2 in self.used:
                        if (self.used[e2] + 15)%25 in self.avbl:
                            if (self.used[e2] + 20)%25 in self.avbl:
                                self.add_char(d2, (self.used[e2]+20) % 25)
                                self.add_char(d1, (self.used[e2]+15) % 25)
                                self.txt_idx +=2
                                return GOOD_SQR_REWARD
                            return -1012432341
                        return -1012432341
            else:
                if d1 in self.used:
                    if e1 in self.used:
                        if self.used[e1] == (self.used[d1] + 5) % 25:
                            if (self.used[d1]+10) % 25 in self.avbl:
                                if (self.used[d1]+15) % 25 in self.avbl:
                                    self.add_char(d2, (self.used[d1]+10) % 25)
                                    self.add_char(e2, (self.used[d1]+15) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                            if (self.used[d1]+15) % 25 in self.avbl:
                                if (self.used[d1]+20) % 25 in self.avbl:
                                    self.add_char(d2, (self.used[d1]+15) % 25)
                                    self.add_char(e2, (self.used[d1]+20) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        return -1231243124
                    if d2 in self.used:
                        if self.used[d2] == (self.used[d1] + 10) % 25:
                            if (self.used[d1]+5) % 25 in self.avbl:
                                if (self.used[d1]+15) % 25 in self.avbl:
                                    self.add_char(e2, (self.used[d1]+15) % 25)
                                    self.add_char(e1, (self.used[d1]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        if self.used[d2] == (self.used[d1] + 15):
                            if (self.used[d1]+5) % 25 in self.avbl:
                                if (self.used[d1]+20) % 25 in self.avbl:
                                    self.add_char(e2, (self.used[d1]+20) % 25)
                                    self.add_char(e1, (self.used[d1]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        return -1231243124
                    if e2 in self.used:
                        if self.used[e2] == (self.used[d1] + 15):
                            if (self.used[d1]+5) % 25 in self.avbl:
                                if (self.used[d1]+10) % 25 in self.avbl:
                                    self.add_char(d2, (self.used[d1]+10) % 25)
                                    self.add_char(e1, (self.used[d1]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        if self.used[e2] == (self.used[d1] + 20):
                            if (self.used[d1]+5) % 25 in self.avbl:
                                if (self.used[d1]+15) % 25 in self.avbl:
                                    self.add_char(d2, (self.used[d1]+15) % 25)
                                    self.add_char(e1, (self.used[d1]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        return -1231243124
                elif d2 in self.used:
                    if e1 in self.used:
                        if self.used[e1] == (self.used[d2] + 15):
                            if (self.used[d2]+5) % 25 in self.avbl:
                                if (self.used[d2]+10) % 25 in self.avbl:
                                    self.add_char(d1, (self.used[d2]+10) % 25)
                                    self.add_char(e2, (self.used[d2]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        if self.used[e1] == (self.used[d2] + 20):
                            if (self.used[d2]+5) % 25 in self.avbl:
                                if (self.used[d2]+15) % 25 in self.avbl:
                                    self.add_char(d1, (self.used[d2]+15) % 25)
                                    self.add_char(e2, (self.used[d2]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        return -1231243124
                    if e2 in self.used:
                        if self.used[e2] == (self.used[d2] + 5) % 25:
                            if (self.used[d2]+10) % 25 in self.avbl:
                                if (self.used[d2]+15) % 25 in self.avbl:
                                    self.add_char(d1, (self.used[d2]+10) % 25)
                                    self.add_char(e1, (self.used[d2]+15) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                            if (self.used[d2]+15) % 25 in self.avbl:
                                if (self.used[d2]+20) % 25 in self.avbl:
                                    self.add_char(d1, (self.used[d2]+15) % 25)
                                    self.add_char(e1, (self.used[d2]+20) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        return -1231243124
                elif e1 in self.used:
                    if e2 in self.used:
                        if self.used[e2] == (self.used[e1] + 10) % 25:
                            if (self.used[e1]+5) % 25 in self.avbl:
                                if (self.used[e1]+20) % 25 in self.avbl:
                                    self.add_char(d1, (self.used[e1]+20) % 25)
                                    self.add_char(d2, (self.used[e1]+5) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        if self.used[e2] == (self.used[e1] + 15) % 25:
                            if (self.used[e1]+10) % 25 in self.avbl:
                                if (self.used[e1]+20) % 25 in self.avbl:
                                    self.add_char(d1, (self.used[e1]+20) % 25)
                                    self.add_char(d2, (self.used[e1]+10) % 25)
                                    self.txt_idx += 2
                                    return GOOD_SQR_REWARD
                        return -1231243124
        # if len(avbl_chars) == 1:
        #     if len(set([d1, d2, e1, e2])) == 3:
        #         if d1 == d2:
        #             return -12342134123
        #         if e2 == d2:
        #             return -1234123
        #         if d1 == e2:
        #             if d1 in self.used:











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
            if d1 not in avbl_chars and d2 not in avbl_chars:    #  If something breaks retest this/ but I did test it 
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
            if d1 not in avbl_chars and e1 not in avbl_chars:     # both in same row, tested 6/1
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
            if d2 not in avbl_chars and e2 not in avbl_chars:     # both in same row, tested!
                row_used1 = self.used[d2] // 5
                col_used1 = self.used[d2] % 5
                row_used2 = self.used[e2] // 5
                col_used2 = self.used[e2] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if col_used1 == col_used2:
                    return
                if row_used1 == row_used2:
                    max_row1 = row_used1
                    max_col1 = col_used1  # d2
                    max_col2 = col_used2  # e2
                    for i in range(len(rows)-1):
                        max_row2 = rows[-1-i][0]
                        we_good = (max_row2 * 5) + max_col1 in self.avbl
                        we_good &= (max_row2 * 5) + max_col2 in self.avbl
                        if we_good:
                            # self.add_char(d1, (max_row1*5) + max_col1)
                            self.add_char(d1, (max_row2*5) + max_col2)
                            # self.add_char(d2, (max_row2*5) + max_col2)
                            self.add_char(e1, (max_row2*5) + max_col1)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD
            if d1 not in avbl_chars and e2 not in avbl_chars:  # both in same column, tested 6/1, feel pretty good about this one
                row_used1 = self.used[d1] // 5
                col_used1 = self.used[d1] % 5
                row_used2 = self.used[e2] // 5
                col_used2 = self.used[e2] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if row_used1 == row_used2:  #  is this necessary? Possible Optimaztion.
                    return
                if col_used1 == col_used2:                   
                    max_col1 = col_used1
                    max_row1 = row_used1  # d1
                    max_row2 = row_used2  # e2
                    for i in range(len(cols)-1):
                        max_col2 = cols[-1-i][0]
                        we_good = (max_row1 * 5) + max_col2 in self.avbl
                        we_good &= (max_row2 * 5) + max_col2 in self.avbl
                        if we_good:
                            # self.add_char(d1, (max_row1*5) + max_col1)
                            self.add_char(e1, (max_row1*5) + max_col2)
                            # self.add_char(d2, (max_row2*5) + max_col2)
                            self.add_char(d2, (max_row2*5) + max_col2)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD
            if d2 not in avbl_chars and e1 not in avbl_chars:  # both in same column, tested 6/1, feel pretty good about this one
                row_used1 = self.used[d2] // 5
                col_used1 = self.used[d2] % 5
                row_used2 = self.used[e1] // 5
                col_used2 = self.used[e1] % 5
                if self.avbl_row[row_used1]==0 or self.avbl_col[col_used1]==0:
                    return
                if self.avbl_row[row_used2]==0 or self.avbl_col[col_used2]==0:
                    return
                if row_used1 == row_used2:  #  is this necessary? Possible Optimaztion.
                    return
                if col_used1 == col_used2:                   
                    max_col1 = col_used1
                    max_row1 = row_used1  # d2
                    max_row2 = row_used2  # e1
                    for i in range(len(cols)-1):
                        max_col2 = cols[-1-i][0]
                        we_good = (max_row1 * 5) + max_col2 in self.avbl
                        we_good &= (max_row2 * 5) + max_col2 in self.avbl
                        if we_good:
                            # self.add_char(d1, (max_row1*5) + max_col1)
                            self.add_char(e2, (max_row1*5) + max_col2)
                            # self.add_char(d2, (max_row2*5) + max_col2)
                            self.add_char(d1, (max_row2*5) + max_col2)
                            self.txt_idx += 2
                            return GOOD_SQR_REWARD
        if len(avbl_chars) == 1:
            if e1 not in avbl_chars and e2 not in avbl_chars and d1 not in avbl_chars:  # d2 is missing
                row_used1 = self.used[e2] // 5
                col_used1 = self.used[e1] % 5 
                we_good = (row_used1 * 5) + col_used1 in self.avbl
                if we_good:
                    self.add_char(d2, (row_used1 * 5) + col_used1)
                    self.txt_idx += 2
                    return GOOD_SQR_REWARD
            if e1 not in avbl_chars and e2 not in avbl_chars and d2 not in avbl_chars:  # d1 is missing
                row_used1 = self.used[e1] // 5
                col_used1 = self.used[e2] % 5 
                we_good = (row_used1 * 5) + col_used1 in self.avbl
                if we_good:
                    self.add_char(d1, (row_used1 * 5) + col_used1)
                    self.txt_idx += 2
                    return GOOD_SQR_REWARD
            if e1 not in avbl_chars and d1 not in avbl_chars and d2 not in avbl_chars:  # e2 is missing
                row_used1 = self.used[d2] // 5
                col_used1 = self.used[d1] % 5 
                we_good = (row_used1 * 5) + col_used1 in self.avbl
                if we_good:
                    self.add_char(e2, (row_used1 * 5) + col_used1)
                    self.txt_idx += 2
                    return GOOD_SQR_REWARD
            if e2 not in avbl_chars and d1 not in avbl_chars and d2 not in avbl_chars:  # e1 is missing
                row_used1 = self.used[d1] // 5
                col_used1 = self.used[d2] % 5 
                we_good = (row_used1 * 5) + col_used1 in self.avbl
                if we_good:
                    self.add_char(e1, (row_used1 * 5) + col_used1)
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
