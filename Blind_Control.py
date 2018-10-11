import time
import RPi.GPIO as GPIO
import sys
import os

# You may have to create the channels.txt file and need to change the directory that it is in to suit your needs.

# Channel Information for my house

# Ch1 - All Front Blinds
# Ch2 - First & Third Front Blinds (Not Door)
# Ch3 - Office Blind
# Ch4 - Back Room Blinds
# Ch5 - ALL Blinds


# Using Pins 2, 3, 4 and 14 for no particular reason.
# 2 is for channel button
# 3 is for UP
# 4 is for DOWN
# 14 is for STOP


# Take values from command-line
requested_channel = int(sys.argv[1])
action = sys.argv[2]

# Somfy Telis 4 has 5 channels
NR_CHANNELS = 5
    
# timeout after which remote channel flashing has gone
CHANNEL_TIMEOUT = 6     # seconds
    
# time interval for normal button presses
BUTTON_HOLD    = 0.1    # seconds
BUTTON_TIMEOUT = 0.2 # seconds


# Set which channel we need.
def set_channel(cur_channel, new_channel):

        # do we need to switch?
        if cur_channel != new_channel:

	    GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD

            print ("Changing to channel " + str(new_channel)) + ", Please wait about 6 seconds..."
            # how many channels to switch? this works also fine for negative numbers
            channel_diff = (new_channel - cur_channel) % NR_CHANNELS
            # we need 1 press more than the channel difference
            for i in range(channel_diff+1):
		GPIO.setup(2, GPIO.OUT) 
		time.sleep (0.1)
		GPIO.setup(2, GPIO.IN)
		time.sleep (0.1)
            
	    # after channel switching wait until channel flashing is over
            time.sleep(CHANNEL_TIMEOUT)

            # store new channel
            with open("/var/www/html/somfy/channel.txt", 'w') as file:
            	data[0] = str(int(new_channel))
                file.writelines(data)

	else:
		print "No Channel Change Needed"


# Set what to do with the blind
def set_blind(action):

	GPIO.setmode(GPIO.BCM)             

	if action in ("up", "Up", "UP"):

		print "Sending UP command"
		GPIO.setup(3, GPIO.OUT)          
		time.sleep (1)
		GPIO.setup(3, GPIO.IN)

	elif action in ("down", "Down", "DOWN"):

		GPIO.setup(4, GPIO.OUT)          
                time.sleep (1)
                GPIO.setup(4, GPIO.IN)
		print "Sending DOWN command"

	elif action in ("stop", "Stop", "STOP"):
	
		GPIO.setup(14, GPIO.OUT)         
                time.sleep (1)
                GPIO.setup(14, GPIO.IN)
                print "Sending STOP command"



# Main Program Start

with open("/var/www/html/somfy/channel.txt", 'r') as file:# the files are un a subfolder "somfy"
	data = file.readlines()
	channel_stored = int(data[0])
	print ("Channel stored is: " + str(channel_stored))
	print ("Channel requested is: " + str(requested_channel))

set_channel(channel_stored,requested_channel)
set_blind(action)
quit()
