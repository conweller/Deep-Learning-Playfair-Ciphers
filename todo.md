# Plan for the Project

## Key State:
* Fields:
    * Used spaces: dictionaries of letters to index
    * Available spaces
* If both letters are used, check that key works, give reward
* 4 actions:
    * Place in col:
        * Check if one letter is in used, if yes, try to place other in same
          column
        * else find col to place both
    * Place in row:
        * Check if one letter is in used, if yes, try to place other in same
          row
        * else find row to place both
    * Place in Square:
        * Place unused letters in pair in some availible spaces
* If actions fail give negative reward
## Neural Net architecture
* Each input node is one 4 letter tuple (2 plaintext, 2 ciphertext)
  * If there are 100 chars in the input text, then their should be 50 inpute nodes 
* Outputs a key
