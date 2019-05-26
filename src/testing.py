""""""
import keyenv
import cipher
KEY = cipher.generate_key()
# print(key)

CIPHERTEXT = "abcdcb"
TEXT = "efghxy"

KS = keyenv.KeyState(TEXT, CIPHERTEXT, KEY)
