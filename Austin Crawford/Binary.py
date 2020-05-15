######################################################################
# Name:         Austin Crawford
# File:         Binary.py
# Class:        CSC 442, Louisiana Tech Univeristy, Spring 2020
# Instructor:   Dr. Jean Gourd
# Description:  This program takes 7-bit or 8-bit binary input
#               and decodes it into readable text
######################################################################

# allow input to be read from the terminal 
from sys import stdin

# function to decode binary input to n-bit ASCII
# output
def decode(binary, n):
    text = ""                   # initialize ASCII text output
    i = 0                       # initialize byte iterator
    # go to the end of the binary input
    while (i < len(binary)):
        byte = binary[i:i+n]    # store byte as n-bit section of input
        byte = int(byte, 2)     # convert binary to integer

        if (byte == 8):         # if the character is a backspace
            text = text[0:-1]   # remove last character
            
        else:                   # otherwse,
            text += chr(byte)   # convert integer to ASCII text and add to text
        
        i += n  # move n bits 

    return text

# read console input; remove new line at the end
binary = stdin.read().rstrip("\n")

# if length of binary input is divisible by 7, decode
# 7-bit ASCII; same if divisible by 8
if (len(binary) % 7 == 0):
    text = decode(binary, 7)
    print "7-bit:"
    print text
if (len(binary) % 8 == 0):
    text = decode(binary, 8)
    print "8-bit:"
    print text
