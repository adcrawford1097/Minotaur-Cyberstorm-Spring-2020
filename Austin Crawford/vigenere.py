###########################################################################
# Name:         Austin Crawford
# File:         vigenere.py
# Class:        CSC 442, Louisiana Tech University, Spring 2020
# Instructor:   Dr. Jean Gourd
# Date:         3/27/2020
# Description:  This program takes text input from the user and either
#               encodes or decodes based on user arguments according to
#               the vigenere cipher. 
###########################################################################


# allow for user input and arguments
from sys import stdin, argv

# function which takes a letter and returns a value corresponding to A = 0, B = 1, C = 2, etc.
# works for both uppercase and lowercase letters
def ToNum(char):
    if char.isupper():          # if character is uppercase, shift accordingly
        return ord(char)-65     # ASCII value of capital A is 65
    return ord(char)-97         # otherwise, shift accordingly
                                # ASCII value of lowercase a is 97
                                
# function which takes a character(used to determine case of output) and returns the character
# corresponding to the input number
def ToChar(char, number):
    if char.isupper():
        return chr(number + 65)
    return chr(number + 97)
    
# function which encrypts readable plaintext into ciphertext
def encrypt(plaintext, key):
    ciphertext = ""
    j = 0   # key iterator
    for i in range(0, len(plaintext)):  # plaintext iterator
        while(j >= len(key)):           # if j is greater than the length of the key
            j = j - len(key)            # find appropriate value for j
            
        # what to do if the plaintext character is a letter
        if(plaintext[i].isalpha()):
            # convert plaintext and ket characters to
            # appropriate numbers
            pi_num = ToNum(plaintext[i])
            ki_num = ToNum(key[j])
            
            # calculate cyphertext value
            ci_num = (pi_num + ki_num)%26
            
            # convert cyphertext number to character
            # (the plaintext character is needed to determined
            # the case of the cyphertext)
            ci = ToChar(plaintext[i], ci_num)

            j = j + 1
            
        # what to do if the plaintext character is not a letter
        else:
            ci = plaintext[i]   # the cyphertext character is simply the plaintext character
        ciphertext = ciphertext + ci    # append calculate character to the ciphertext

    return ciphertext

# function which decrypts ciphertext into readable plaintext
# reverse process of encryption
def decrypt(ciphertext, key):
    plaintext = ""
    j = 0
    for i in range(0, len(ciphertext)):
        while(j >= len(key)):
            j = j - len(key)

        if(ciphertext[i].isalpha()):
            ci_num = ToNum(ciphertext[i])
            ki_num = ToNum(key[j])

            # similar to calculating cipher character number in encryption function, but
            # the values are subtracted instead of added. add 26 to ensure that the
            # result is never negative
            pi_num = (ci_num - ki_num + 26)%26

            pi = ToChar(ciphertext[i], pi_num)

            j = j + 1
            
        else:
            pi = ciphertext[i]

        plaintext = plaintext + pi

    return plaintext


mode = argv[1]              # the second argument is the mode for the program
                            # -d for decode and -e for encode
                            
if ((len(argv) == 3)):      # the third argument is the key for the cipher
    key = argv[2]
elif(len(argv) > 3):        # if more than three arguments are entered, raise an exception
    raise Exception("""Invalid Argument. viginere.py accepts a maximum of 2 arguments.
                The first argument determines the program's mode:
                -d is used to decode ciphertext into plaintext
                -e is used to encode plaintext into ciphertext
                The second argument determines the program's key (must be composed of letters
                and spaces only:
                example: 'my key' (defaults to 'a' which makes no change to the original text)""")
else:                       # if no third argument is given,
    key = "a"               # set default key as "a". this will not change the plaintext at all

unspaced_key = ""           # remove all spaces from the key and ensure no other characters
                            # besides letters are used
for char in key:
    if (char.isalpha() == False and char != " "):
        raise Exception("Invalid key. Must be composed of letters and spaces only.")
    if (char != " "):
        unspaced_key += char

text = stdin.read().rstrip("\n")    # take user input and remove any newlines

if (mode == "-e"):                  # if the mode argument is -e, encrypt
    ciphertext = encrypt(text, unspaced_key)
    print ciphertext
elif(mode == "-d"):                 # if the mode argument is -d, decrypt
    plaintext = decrypt(text, unspaced_key)
    print plaintext
else:                               # if a mode argument other than -e  or -d is entered, raise
                                    # raise a value error
    raise ValueError('Invalid argument. Expecting -e or -d. Use -e to encrypt and -d to decrypt.')
