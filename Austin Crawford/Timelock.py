# use Python 2

from sys import stdin
from datetime import datetime
import pytz
from hashlib import md5

# debug mode?
DEBUG = False

# set to True if on the challenge server
ON_SERVER = False

#valid time interval
INTERVAL = 60

# manual current datetime?
MANUAL_DATETIME = "2013 05 06 12 43 25"

# function which parses the input of a datetime and returns separate values for 
# year, month, day, hour, minute, and second
def sep_datetime(datetime):
	year = ""
	month = ""
	day = ""
	hour = ""
	minute = ""
	second = ""
	for char in datetime:
		if (char.isdigit()):
			if (len(year)<4):
				year = year + char
			elif (len(month)<2):
				month = month + char
			elif (len(day)<2):
				day = day + char
			elif (len(hour)<2):
				hour = hour + char
			elif (len(minute)<2):
				minute = minute + char
			elif (len(second)<2):
				second = second + char
	return int(year), int(month), int(day), int(hour), int(minute), int(second)

# determines whether a year is a leap year or not
def isLeapYear(year):
	if(year%4 == 0):
		return True
	else: 
		return False

# function which returns the appropriate number of days, given a month and a year
def days_in_month(month, year):
	if(month in {1, 3, 5, 7, 8, 10, 12}):
		return 31
	elif(month in {4, 6, 9, 11}):
		return 30
	else: 
		if isLeapYear(year):
			return 29
		else:
			return 28

# take std input and store as the epoch
epoch = stdin.read().rstrip("\n")

# store the current datetime as a string
current_datetime = str(datetime.now())

# if in debug mode, store the current datetime as the manual datetime
if(DEBUG):
	current_datetime = MANUAL_DATETIME

# use the sep_datetime function to parse through the current datetime and 
# the epoch datetime and rerturn their respective year, month, day, hour
# minute, and second
cyear, cmonth, cday, chour, cmin, csec =  sep_datetime(current_datetime)
eyear, emonth, eday, ehour, emin, esec = sep_datetime(epoch)

# print out detailed current and epoch datetime info if in debug mode
if(DEBUG):
	print "Current Datetime Info:"
	print cyear
	print cmonth
	print cday
	print chour
	print cmin
	print csec
	print "Current (UTC):{}".format(current_datetime)
	print "Epoch Datetime Info:"
	print eyear
	print emonth
	print eday
	print ehour
	print emin
	print esec
	print "Epoch (UTC): {}".format(epoch)

# Calculate the number of seconds that have passed from epoch to current time.
# We will start from the smallest unit (seconds) and keep counting upwards until
# we reach the value of those units in the current time. If we "roll over", we 
# will simply add one to the next larger unit. 

sec = 0		# initialize seconds varable

# if the current seconds are greater than the epoch seconds, simply take the 
# difference and add that to seconds. if not, "roll over" by counting the seconds
# until the next minute, add one to the epoch minutes and then contiue counting up
# to the current seconds. 
if(csec >= esec):
	sec += csec - esec
else: 
	sec += 60 - esec
	emin += 1
	sec += csec

if (DEBUG):
	print sec

# similar to the seconds method, except add 60 seconds for each minute
if(cmin >= emin):
	sec += (cmin - emin)*60
else: 
	sec += (60 - emin)*60
	ehour += 1 
	sec += cmin*60

if (DEBUG):
	print sec

# add 3600 seconds for each hour
if(chour >= ehour):
	sec += (chour - ehour)*3600
else: 
	sec += (24 - ehour)*3600
	eday += 1 
	sec += chour*3600

if (DEBUG):
	print sec

# add 86400 seconds for each day
if(cday >= eday):
	sec += (cday - eday)*86400
else:
	sec += (days_in_month(emonth, eyear)-eday)*86400
	emonth += 1
	sec += cday*86400

if (DEBUG):
	print sec

# slightly more complex because the number of days in each month varies.
# however, general process is the same, except call the function days_in_month
# each time a month is added and multiply by 86400 to add the appropriate number 
# of seconds
if(cmonth >= emonth):
	while(emonth < cmonth):
		sec += days_in_month(emonth, eyear)*86400
		emonth += 1 
else: 
	while(emonth < 13):
		sec += days_in_month(emonth, eyear)*86400
                emonth += 1
	eyear += 1
	emonth = 0
        while(emonth < cmonth):
		sec += days_in_month(emonth, eyear)*86400
                emonth += 1
if (DEBUG):
	print sec

# assume that the current year is greater than the epoch year. therefore, 
# we do not need to worry about "rolling over." just count up to the current year
# and add 365 days (366 days if a leap year) times 86400 to add the appropriate 
# number of seconds in a year. 
if(cyear > eyear):
	sec += 365*86400
	eyear += 1
while(cyear > eyear):
	if(isLeapYear(eyear)):
		sec += 366*86400
	else: 
		sec += 365*86400
	eyear += 1

if(DEBUG):
	print sec


# convert the seconds variable into the largest multiple of 60 less than the 
# current value
sec = str(sec - sec%INTERVAL)

if(DEBUG):
	print sec

# encode the number of seconds twice
md51 = md5(sec.encode()).hexdigest()
md52 = md5(md51.encode()).hexdigest()

if(DEBUG):
	print "MD5 #1: {}".format(md51)
        print "MD5 #2: {}".format(md52)

output = ""		# initialize output string

# go through md5 #2 string twice. find first two letters going forward and add those
# to output. find first two numbers going backwards and add those to the output
for char in md52:
	if (len(output) < 2):
		if char.isalpha():
			output += char

for char in reversed(md52):
	if (len(output) < 4):
		if char.isdigit():
			output+= char

# print the output code
print output

