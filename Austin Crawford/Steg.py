######################################################################
# Name:         Austin Crawford
# File:         Steg.py
# Class:        CSC 442, Louisiana Tech Univeristy, Spring 2020
# Instructor:   Dr. Jean Gourd
# Description:  This program takes stores or retrieves a hidden
#               file within a hidden wrapper file using either
#               bit or byte mode with arguments taken in
#               for offsets and intervals
#
# This program uses Python v. 2
######################################################################

# import libraries which allow for standard input and arguments to be taken
# from the command line

from sys import stdin, argv

# Debug Mode
DEBUG = False

# Constants for minimum number of arguments, maximum number of arguments, and
# sentinel values
MIN_ARGS = 3
MAX_ARGS = 7
SENTINEL = ["0", "ff", "0", "0", "ff", "0"]

# function which takes in an argument, determines if it is valid and returns
# the argument type
def arg_type(arg):
	if(arg[0] != "-" or arg[1] not in ["s", "r", "b", "B", "o", "i", "w", "h"]):
		raise Exception("Invalid argument type")
	else: 
		return arg[1]

if (DEBUG):
	print argv

# functions which determine if their is an appropriate number of arguments
if (len(argv) < MIN_ARGS):
	raise Exception("Too few arguments")
elif(len(argv) > MAX_ARGS):
	raise Exception ("Too many arguments")
else:   # if appropriate number ofargs, put arg types in an array
	arg_types = []
	for val in argv[1:]: 
		arg_types.append(arg_type(val))

if(DEBUG):
	print arg_types

# set default values for modes, offset, interval, and files

bit_mode = False
byte_mode = False
store_mode = False
retrieve_mode = False
offset = 0
interval = 1
wrapper_file = None
hidden_file = None

# make sure there are no logical inconsistencie within args
i = 1
for char in arg_types: 
	if(char == "s"): 
		if(retrieve_mode == False):
			store_mode = True
		else: 
			raise Exception("Invalid argument. Retrieve Mode" 
				" already selected")
	elif(char == "r"):
		if(store_mode == False):
			retrieve_mode = True
		else: 
			raise Exception("Invalid argument. Store Mode already"
				" selected")
        elif(char == "b"):
                if(byte_mode == False):
                        bit_mode = True
                else:
                        raise Exception("Invalid argument. Byte Mode already"
                                " selected")

        elif(char == "B"):
                if(bit_mode == False):
                        byte_mode = True
                else:
                        raise Exception("Invalid argument. Bit Mode already"
                                " selected")

	elif(char == "o"):
		offset = argv[i][2:]
		
		if (offset.isdigit() == False):
			raise Exception ("Invalid offset. Must be integer value")
		else: 
			offset = int(offset)

	elif(char == "i"):
		interval = argv[i][2:]
		if (interval.isdigit() == False):
			raise Exception ("Invalid interval. Must be integer value")
		else: 
			interval = int(interval)

	elif(char == "w"):
		wrapper_file = argv[i][2:]

	elif(char == "h"):
		hidden_file = argv[i][2:]
	
	else: 
		raise Exception ("Invalid argument")
	i += 1

if (not (bit_mode or byte_mode)):
	raise Exception("Please select mode (bit or byte)")

if (not (store_mode or retrieve_mode)):
	raise Exception("Please select function (store or retrieve")

if (wrapper_file == None):
	raise Exception("Please select wrapper file")

if (DEBUG):
	print "Store mode: {}".format(store_mode)
	print "Retrieve mode: {}".format(retrieve_mode)
	print "Bit mode: {}".format(bit_mode)
	print "Byte mode: {}".format(byte_mode)
	print "Offset: {}".format(offset)
	print "Interval: {}".format(interval)
	print "Wrapper file: {}".format(wrapper_file)
	print "Hidden file: {}".format(hidden_file)

# if the assemby is in byte mode and store mode, perform the apprpriate algorithm

if (byte_mode and store_mode):
	if(DEBUG):
		print "Storing (byte mode)..."
	wfile = open(wrapper_file, mode = "r")
	W = wfile.read()
	wfile.close()

	hfile = open(hidden_file, mode = "r")
	H = hfile.read()
	hfile.close()
	
	if(DEBUG):
		print "Wrapper File:"
		print W
		print "Hidden File:"
		print H

	i = 0

	W = list(W)

	while(i < len(H) - 1):
		W[offset] = H[i]
		offset += interval
		i += 1

	i = 0

	while(i< len(SENTINEL)):
		W[offset] = chr(int(("0x" + SENTINEL[i]), 16))
		offset += interval
		i += 1

	W = ''.join(W)

	print W

# algorithm for byte mode and retrieve mode

if (byte_mode and retrieve_mode):
	sent_state = False
	if (DEBUG):
		print "Retrieving (byte mode)..."
	
	wfile = open(wrapper_file, mode = "r")
	W = wfile.read()
	wfile.close()

	H = []

	while (offset < len(W) and sent_state == False):
		b = W[offset]
		if(hex(ord(b))[2:] == SENTINEL[0]):
			test = []
			for j in range(6):
				try: 
					test.append(hex(ord(W[offset + j * interval]))[2:])
				except: 
					pass
			if(test == SENTINEL):
				sent_state = True
		H += b
		offset += interval

	H = ''.join(H)

	print H

# bit mode and store mode

if (bit_mode and store_mode):
	if (DEBUG): 
		print "Storing (bit mode)..."
	
	wfile = open(wrapper_file, mode = "r")
	W = wfile.read()
	wfile.close()

	hfile = open(hidden_file, mode = "r")
	H = hfile.read()
	hfile.close()
	
	if(DEBUG):
		print "Wrapper file"
		print W
		print "Hidden file"
		print H

	W = list(W)
	H = list(H)

	i = 0
	while(i < len(H) - 1):
		for j in range(8):
			W[offset] = ord(W[offset]) & 254
			W[offset] = chr(W[offset] | (ord(H[i]) & 128) >> 7)
			H[i] = (ord(H[i]) << 1) & (2 ** 8 - 1)
			H[i] = chr(H[i])
			offset += interval

		i += 1

	i = 0
	while(i < len(SENTINEL)):
		for j in range(8):
			W[offset] = ord(W[offset]) & 254
			W[offset] = chr(W[offset] | (int(("0x" + str(SENTINEL[i])), 16) & 128) >> 7)
			SENTINEL[i] = hex((int(("0x" + str(SENTINEL[i])), 16) << 1) & (2 ** 8 - 1))[2:]
			offset += interval
		i += 1

	H = ''.join(H)
	W = ''.join(W)
	if (DEBUG):
		print H
		print W

	print W

# bit mode and retrieve mode

if (bit_mode and retrieve_mode):
        sent_state = False
        
	if (DEBUG): 
		print "Receiving (bit mode)..."
	
	wfile = open(wrapper_file, mode = "r")
	W = wfile.read()
	wfile.close()

        H = []
	
	if(DEBUG):
		print "Wrapper file"
		print W
		print "Hidden file"
		print H

	W = list(W)
	H = list(H)

	
	while(offset < len(W)):
                b = 0
                
		for j in range(8):
                        try: 
                                b = b | (ord(W[offset]) & 1)
                                if(j < 7):
                                        b = (b << 1) & (2 ** 8 - 1)
                                        offset += interval
                        except:
                                if (DEBUG):
                                        print "index exceeds length of W"
                                
		if(hex(b)[2:] == SENTINEL[0]):
			test = []
			for j in range(6):
				try: 
					test.append(hex(ord(W[offset + j * interval]))[2:])
				except: 
					if (DEBUG):
                                                print "index exceeds length of W"
			if(test == SENTINEL):
				sent_state = True

		H += chr(b)
		offset += interval 

	H = ''.join(H)
	W = ''.join(W)
	if (DEBUG):
		print H
		print W

	print H
		


