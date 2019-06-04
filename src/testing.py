""""""
import keyenv
import cipher
KEY = cipher.generate_key()
# print(key)

TEXT =       "abefghijk"
CIPHERTEXT = "cdlmnopqr"

KS = keyenv.KeyState(TEXT, CIPHERTEXT, KEY)
KS.add_char("a", 0)
KS.add_char("b", 10)
KS.add_char("c", 5)
KS.add_char("d", 15)
KS.get_key()
