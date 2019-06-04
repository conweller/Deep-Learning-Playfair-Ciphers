""""""
import keyenv
import cipher
KEY = cipher.generate_key()
# print(key)

TEXT =       "abefghijk"
CIPHERTEXT = "calmnopqr"

KS = keyenv.KeyState(TEXT, CIPHERTEXT, KEY)
