##################################################################
# Name: Austin Crawford
# Date: 5/6/20
# File: xor.py
# Class: CSC 442, Spring 2020, Louisiana Tech Unversity
# Instructor: Dr. Jean Gourd
# Description: This program takes in input from the console
# and encodes or decodes the input based off XOR cryptograpy with 
# a key coming from a designated file
##################################################################

# Note: this program is written for Python 2

import binascii
from sys import stdin

# Debug mode
DEBUG = False
# Input mode
INPUT = True
# Input key file here
KEY_FILE = "text1"

# Function to decode binary input into ascii text
def decode(binary, n):
	text = ""
	i = 0

	while(i < len(binary)):
		byte = binary[i:i+n]
		byte = int(byte, 2)

		text += chr(byte)
		
		i += n

	return text

# Function to encode ascii text into a binary string 
def ToBinary(string):
	bin_string = ""
	for char in string:
		number = ord(char)
		binary = str(bin(number))[2:]
		binary = "0"*(8 - len(binary)) + binary
		bin_string += binary
	return bin_string

# If input mode is off, set default input and key.
if(INPUT == False):
	input_str = "Example plaintext message"
	key = "This is my sample key"
# If input mode is on, take take input and store it in a  string. Read key from
# KEY_FILE
else:
        input_str = stdin.read()
	keyfile = open(KEY_FILE, mode = "r")
        key = keyfile.read()
        keyfile.close()

# Ensure that the input and key are the same length
if(len(input_str) < len(key)):
        input_str += chr(255) * (len(key)-len(input_str))
elif(len(key) <  len(input_str)):
        key += chr(255) * (len(input_str)-len(key))

if(DEBUG):
	print "Input: {}".format(input_str)
	print "Key: {}".format(key)

# Convert the input and key into a binary string
bin_input = ToBinary(input_str)
bin_key = ToBinary(key)

if(DEBUG):
	print "Input (Binary): {}".format(bin_input)
	print "Key (Binary): {}".format(bin_key)

# Go through each bit in each binary string and XOR it
bin_output = ""
i = 0
for char in bin_input:
	if(char == bin_key[i]):
		bin_output += "0"
	else:
		bin_output += "1"
	i += 1
if(DEBUG):
	print "Output (Binary): {}".format(bin_output)

# Decode binary output into ascii text
output = decode(bin_output, 8)

if(DEBUG):
	print "Output: {}".format(output)
else: 
	print output
