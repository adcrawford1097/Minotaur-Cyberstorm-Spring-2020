##########################################################################
# Name: 	Austin Crawford
# File: 	chat_client.py
# Class: 	CSC 442, Louisiana Tech University, Spring 2020
# Instructor: 	Dr. Jean Gourd
# Date: 	4/23/20
# Description: 	This program opens a chat server and interprets an overt
#		message into a covert one based on timing. 
###########################################################################

# Note: this script is written for Python 2

# import necessary libraries
import socket
from sys import stdout
from time import time
from binascii import unhexlify

# enables debugging output
DEBUG = True

# set the server's IP address and port
ip = "138.47.99.163"
port = 12321

# time constants to define 0 and 1 bytes within covert message
ZERO = 0.025
ONE = 0.1

# initialize string which will contain binary data for covert message
covert_bin = ""

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
s.connect((ip, port))

# check to see if connecting to server while in debug mode
if (DEBUG):
	print "Connected to Server..."

# receive data until EOF
data = s.recv(4096)
while (data.rstrip("\n") != "EOF"):
	# output the data
	stdout.write(data)
	stdout.flush()
	# start the "timer", get more data, and end the "timer"
	t0 = time()
	data = s.recv(4096)
	t1 = time()
	# calculate the time delta (and output if debugging)
	delta = round(t1 - t0, 3)
	# if the time between characters indicates a 1, add "1" to covert string
	# otherwise, add zero
	if (delta >= ONE):
		covert_bin += "1"
	else:
		covert_bin += "0"
	# print times while in debug mode
	if (DEBUG):
		stdout.write(" {}\n".format(delta))
		stdout.flush()

# initialize interpreted covert message
covert = ""
i = 0
# for each byte in covert_bin, covert to ascii text
while (i < len(covert_bin)):
	b = covert_bin[i:i+8]
	n = int ("0b{}".format(b), 2)
	try:
		covert += unhexlify("{0:x}".format(n))
	except TypeError:	# add question mark if non printable character
		covert += "?"
	i += 8

# find the index at which EOF is located and store it
EOF = covert.find("EOF")

# print a new line followed by the covert message up to "EOF"
print "\n"
print "covert message: " + covert[0:EOF]

# close the connection to the server
s.close()

