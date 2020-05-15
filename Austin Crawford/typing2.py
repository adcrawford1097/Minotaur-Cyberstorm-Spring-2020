from pynput.keyboard import Key, Controller
from time import sleep
from random import uniform
from termios import tcflush, TCIFLUSH
from sys import stdin, stdout

DEBUG = False 

password = raw_input()
timings = raw_input()

keyboard = Controller()

if(DEBUG):
	print "password = {}".format(password)
	print "timings = {}".format(timings)

password = password.split(",")
password = password[:len(password) / 2 + 1]
password = "".join(password)

if(DEBUG):
	print password


timings = timings.split(",")
timings = [float(a) for a in timings]
keypress = timings[:len(timings) / 2 + 1]
keyintervals = timings[len(timings) / 2 + 1 : len(timings) + 1]

if(DEBUG):
	print "Keypress times  = {}".format(keypress)
	print "Keyinterval times = {}".format(keyintervals)

sleep(5)

i = 0
for char in password: 
	keyboard.press(char)
	sleep(keypress[i])
	keyboard.release(char)
	sleep(keyintervals[i])

tcflush(stdout, TCIFLUSH)
print 
