""""""
import keyenv
import cipher
KEY = cipher.generate_key()
# print(key)

CIPHERTEXT = "efghxy"
TEXT = "abcdcb"

KS = keyenv.KeyState(TEXT, CIPHERTEXT, KEY)
