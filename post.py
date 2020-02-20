###########################################################################################################
#                        Twitter AUTOPOST script by David Simmerson (SimmyDizzle)                         #
###########################################################################################################
# This script will scrape a folder every 5 seconds for new files and then automatically tweet them to the #
# twitterverse on the specified twitter account.                                                          #
###########################################################################################################
# Videos can be a maximum of 2 minutes and 20 seconds and have to be the appropriate file format otherwise#
# the tweet will be rejected. Videos cannot exceed 512MB, otherwise they will be rejected.                #
###########################################################################################################
# Any image file should work properly out of the gate so long as it is not larger than 20MB if the API    #
# guide is to be trusted.                                                                                 #
###########################################################################################################

###########################################################################################################
# Import required modules(packages) to ensure that the twitterpost system will work.
import random           # import the random number generator (for science)

import time             # import the time system
import datetime         # import the datetime system

import tweepy           # tweepy may require the installation of pip.
import os               # import the operating system functions

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

###########################################################################################################
# Consumer keys and access tokens, used for OAuth
# you will need to generate these on dev.twitter.com
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

###########################################################################################################
# grab a baseline timeframe before main is called. (Filler)
today = time.strftime("%Y-%m-%d %H:%M")

###########################################################################################################
# list of our approved filetypes
approved_types = ['jpeg', 'jpg', 'gif', 'png', 'bmp', 'avi', 'mp4', 'mkv']

###########################################################################################################
# list of phrases used in tweet generation (we can keep adding these)
# the idea will be like STREAMER_NAME + COMMENT, so like 'SimmyDizzle is on a roll!' will be generated.
phrases = [
    'Strikes Again!',
    'is on a roll!',
    'cannot believe its not butter!',
    'has something special here.',
    'needs your approval! Hit that like and follow button!',
    'cannot believe it!',
    'would like to your opinion!',
    'is this the flavour of the month?',
    'what do you think?',
    'has let loose something here!',
    'thinks this is interesting enough to share.',
    'is out of crazy ideas'
]

###########################################################################################################
##                               CONFIGURATIONAL SETTINGS FOR THE TWEET                                  ##
###########################################################################################################
# This is how many seconds the application will sleep between system passes
SECONDS_TO_SLEEP = 5

# CHANGE ME -- This is the folder where your new files will be scraped from!
DIRECTORY_TO_WATCH = "path/to/your/files" # Windows Example: c:\\users\\myusername\\pictures\\

# Streamer-Name
STREAMER_NAME = "SimmyDizzle"

# Website-Name
WEBSITE_NAME = "http://www.dlive.tv/SimmyDizzle"

# do we want to use the 'random' phrases we generated below?
USE_PHRASES = false

# do we want to use a series of Retweet bots to push our data out
# this should be disabled when you have a large following as it will
# get VERY spammy to those who follow you. Use with caution.
USE_RT = true

###########################################################################################################


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=False) # True if you want subfolders checked.
        self.observer.start()
        try:
            while True:
                today = time.strftime("%Y-%m-%d %H:%M") # Year-Month-Day Hour:Minute
                time.sleep(SECONDS_TO_SLEEP) # Configured above
        except:
            self.observer.stop()
            print ("Error with the watcher")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)

            found = False

            for i in approved_types: 
                if (event.src_path.find("." + approved_types[i]) != '-1'):
                    found = True
                    break

            # Moving on to bigger and brighter things
            if found: 
                # load image/video
                imagePath = event.src_path # this should be the file that was created

                # Set the string, we don't want the tweet being blocked by repeating, so we set date/time of the event.
                if USE_PHRASES:
                    status = "#NPC " + STREAMER_NAME + " " + phrases[random.randint(0,len(phrases)-1)] + today + " " + WEBSITE_NAME
                else:
                    status = "#NPC (" + today + ") Visit " + STREAMER_NAME + " over on @OfficialDlive" + WEBSITE_NAME

                # if we are going to use RT bots
                if USE_RT:
                    status = status + " @sme_rt @DriptRT @FearRTs @Pulse_Rts"
                
                # Send the tweet.
                api.update_with_media(imagePath, status)
		else:
			print ("File is not an approved type")

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print "Received modified event - %s." % event.src_path


###########################################################################################################
# Prostitute the mission, I mean, execute the script function.
if __name__ == '__main__':
    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)

    # Creates the user object. The me() method returns the user whose authentication keys were used.
    user = api.me()
   
    # print out the list of approved filetypes
    print("Accepted Filestypes: " + approved_types )

    # Testing to see if the API is borked or not. (on boot, if this displays wrong, then something was done wrong)
    print('Name: ' + user.name)
    print('Location: ' + user.location)
    print('Friends: ' + str(user.friends_count))

    # Create watcher
    w = Watcher()

    # Execute the watcher script
    w.run()

###########################################################################################################
#EOF
