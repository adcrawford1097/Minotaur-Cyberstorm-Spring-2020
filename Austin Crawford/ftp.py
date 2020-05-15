c#################################################################################
# Name: 	Austin Crawford
# File: 	ftp.py
# Class: 	CSC 442, Louisiana Tech University, Spring 2020
# Instructor: 	Dr. Jean Gourd
# Date: 	4/1/2020
# Description:	This program navigates into an FTP server and decodes the file 
# 		permissions into ASCII text output. Can be used as a covert 
# 		communication channel, assuming both parties have access to the 
# 		the server. 
################################################################################

# Note: this script is written for Python 2. 

# constant which controls the mode of the program. this determines if the file
# permissions will be read as a 7-bit or 10-bit string. For 7-bit insert "7"
# and for 10-bit insert "10"
METHOD = "7"

# set IP, port, and folder constants
IP = "localhost"
PORT = 21
FOLDER = "/test"

# set to True to debug, False if not
DEBUG = False

# import FTP library
from ftplib import FTP

# function which takes a file permission "bit-string" and converts it a binary string
def ToBinary(bit_string):
	binary = ""
	for char in bit_string:
		if (char == "-"):		# if a character is a dash,
			binary = binary + "0"	# add 0 to the binary string

		else:				# otherwise, 
			binary = binary + "1"	# add 1 to the binary string
	return binary

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

# initialize CONTENTS which will contain files and permissions of FOLDER
contents = []

# initialize FTP object, connect to the designated IP and PORT, login, navigate
# to FOLDER, add the contents of the folder to CONTENTs, and exit FTP. 
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login()
ftp.cwd(FOLDER)
ftp.dir(contents.append)
ftp.quit()

# initialize bit string. this will only include the file permissions 
# either as a 7-bit or 10-bit string depending on the mode. 
bit_string = ""

# if the METHOD is 7, only add the last 7 characters of the file permissions for 
# each row in CONTENTS
if(METHOD == "7"):
	for row in contents:
		# if the the first 3 bits are "empty", add the other 7 bits
		# to the bit string. if otherwise, ignore entire row. 
		if (row [0:3] == "---"):
			bit_string = bit_string +  row[3:10]

# if the METHOD is 10, add all 10 characters of the file permissions for each row in 
# CONTENTS
elif(METHOD == "10"):
	for row in contents:
		bit_string = bit_string + row[0:10]

# otherwise, raise Exception. 
else:
	raise Exception("Invalid Mode. Must be 7 or 10.")


if(DEBUG):
	for row in contents: 
		print row
	print bit_string

# convert the permissions bit string to a binary string
binary_string = ToBinary(bit_string)

# decode the binary string based off the appropriate number of bits
# and print output
if (len(binary_string) % 7 == 0):
    text = decode(binary_string, 7)
    print text
if (len(binary_string) % 8 == 0):
    text = decode(binary_string, 8)
    print text
