""""""
import keyenv
import cipher
KEY = cipher.generate_key()
# print(key)

TEXT =       "abefghijk"
CIPHERTEXT = "cdlenopqr"

KS = keyenv.KeyState(TEXT, CIPHERTEXT)
KS.add_char("c", 11)
# KS.add_char("b", 13)
KS.add_char("d", 14)
# KS.add_char("a", 10)
# KS.add_char("q", 13)
# KS.add_char("y", 15)
# KS.add_char("x", 20)
# KS.add_char("z", 5)
KS.get_key()
print()
KS.action_row()
KS.get_key()
