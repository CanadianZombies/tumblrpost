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
# tumblr: https://www.tumblr.com/docs/en/api/v2                                                           #
# Rate limits:                                                                                            #
#   300 API calls per minute, per IP address.                                                             #
#    18,000 API calls per hour, per IP address.                                                           #
#    432,000 API calls per day, per IP address.                                                           #
#    1,000 API calls per hour, per consumer key.                                                          #
#    5,000 API calls per day, per consumer key.                                                           #
#    250 new posts (including reblogs) per day, per user.                                                 #
#    150 images uploaded per day, per user.                                                               #
#    200 follows per day, per user.                                                                       #
#    1,000 likes per day, per user.                                                                       #
#    10 new blogs per day, per user.                                                                      #
#    10 videos uploaded per day, per user.                                                                #
#    5 minutes of total video uploaded per day, per user.                                                 #
###########################################################################################################
# Highlight: 5 minutes of total video uploaded per day per user, this means after 5 1 minute uploads it   #
# will reject any further uploads. This will return 8011 bad requeust. Sadly this cannot be 'tricked'     #
# so as a result we continue to develop this, the qeuue will get bigger every day until the script resets #
# or all items get eventually posted.                                                                     #
# 8009 may also occur if there is a problem with the file, i.e. it cannot upload properly or it has an    #
# error that is detected and cannot be transcoded as a result. If you see the same videos rejecting please#
# remove them from the queue.                                                                             #
###########################################################################################################
# Screenshots (when the create_photo is properly employed) will allow for 250 posts per day.              #
# With this volume of posts per day and the way our queue system works, you will not see 250 posts per    #
# day using this method. However you will have a very 'active' tumblr page, with fresh content posting    #
# on a reguular basis. And not 'scheduled'.                                                               #
###########################################################################################################
# Import required modules(packages) to ensure that the twitterpost system will work.
import random           # import the random number generator (for science)
import array            # import the array module

import time             # import the time system
import datetime         # import the datetime system

import os               # import the operating system functions

import re

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import json             # import the json package to process files
import pytumblr         # import the pytumblr package

# the google translator is important for parts of the future.
from googletrans import Translator

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

# Will update this later to use STREAMER_NAME instead of using hard-coded data.
captions_to_use = [
    'SimmyDizzle Live Presents:',
    'Crazy times with SimmyDizzle:',
    'SimmyDizzle and the whats this?',
    'What-up fam! Check out SimmyDizzle!',
    'SimmyDizzle Strikes Again!',
    'SimmyDizzle is on a roll!',
    'SimmyDizzle has something special here.',
    'I cannot believe its not butter, SimmyDizzle Edition!',
    'LiveSimmy is SimmyDizzle, duh!',
    'Check this out fam',
    'What do you guys think?',
    'Is this the flavour of the month?',
    'Thoughts?',
    'Rip or Nah?',
    'Hit that like and follow button fam!',
    'Captions tend to be random'
    'Sauce?',
    'SimmyDizzle could fap to this.',
    'Tarnations!',
    'Git-Sum',
    'No Pants Crew through and Through!',
    'Founder of NPC reporting in!',
    'Fancy no pantsie!',
    'Blamsauce!',
    'Magic here!',
    'Continued success?',
    'Streaming games is fun!',
    'Streaming games is entertaining!',
    'Video game streaming!',
    'Successful streaming like whaaa!',
    'I am inevitable',
    'I am Iron Pan',
    'Pan, Cast-Iron, Pan.',
    'Is this where the zombie apocalypse starts?',
    'do do do do do... Do do!?',
    'do dew do do',
]

###########################################################################################################
# array for tracking files to push.
push_array = [] # empty array(list).

# Start the google translator (we need this for later)
translator = Translator()

###########################################################################################################
##                               CONFIGURATIONAL SETTINGS FOR THE TWEET                                  ##
###########################################################################################################
# This is how many seconds the application will sleep between system passes
SECONDS_TO_SLEEP = 5 # 5 seconds was old default

# CHANGE ME -- This is the folder where your new files will be scraped from!
#DIRECTORY_TO_WATCH = "C:\\Users\\myusername\\Videos\\Captures" # Windows Example: c:\\users\\myusername\\pictures\\
DIRECTORY_TO_WATCH = "C:\\Users\\myusuername\\Videos\\Replays"

PATHS = ['C:\\Users\mysuername\\Videos\\Replays','C:\\Users\\myusername\\Videos\\Captures']       # Future

# Streamer-Name
STREAMER_NAME = "SimmyDizzle"

# Website-Name
WEBSITE_NAME = "http://www.twitch.tv/SimmyDizzle"

# do we want to use the 'random' phrases we generated below?
USE_PHRASES = False

# enabled for debugging purposes (True/False)
DEBUG_MODE = True

# tweepyControl (Disable this if you want to test thins without posting them to twitter)
# works best when DEBUG_MODE is enable and this is disabled (you'll see logs of things being
# detected/changed without posting to twitter)
TWEEPY_CONTROL = False

# do we want to use a series of Retweet bots to push our data out
# this should be disabled when you have a large following as it will
# get VERY spammy to those who follow you. Use with caution.
USE_RT = True

tags_to_use = ["LiveSimmy", "Streaming", "Streamer", "Games", "ok", "twitchtv", "twitch", "SimmyDizzle", "NextLevel", "video games", "video", "gaming"]

###########################################################################################################

# Logger function, tracks the current time of the log-entry, and the log message so long as DEBUG_MODE is enabled.
# designed to allow for debugging purposes. Obviously we want to minimize all output to maintain minimal footprint.
def Logger(str):
    if DEBUG_MODE:
        print("{%s} %s" % (time.strftime("%Y-%m-%d %H:%M"), str))


# finding a string within a string? you got it dude!
# https://stackoverflow.com/questions/4154961/find-substring-in-string-but-only-if-whole-words
def string_found(string1, string2):
    if string1.find(string2) > 0:
        return True

    return False

###########################################################################################################
# Watcher class for tracking a directory and its changes.
class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, PATHS[0], recursive=False) # True if you want subfolders checked.
        self.observer.schedule(event_handler, PATHS[1], recursive=False) # True if you want subfolders checked.
        self.observer.start()
        
        old_timer = 400
        the_timer = 400
        try:
            ticker = 0
            # this loop is infinite! (Unless we crash)
            while True:
                today = time.strftime("%Y-%m-%d %H:%M") # Year-Month-Day Hour:Minute
                time.sleep(SECONDS_TO_SLEEP) # Configured above

                ticker = ticker +1                      # ticker +1, counting up to our goal

                # ticker should be 300 to push to tumblr. (because science)
                # 150 is 2.5 minutes, but with a 5 second sleep every iteration, this should be roughly 15 minutes.
                # updated to 500 to delay how long it will be between posts.
                if ticker >= the_timer:
                    try:
                        if len(push_array) != 0:
                            x = random.randrange(0,5)

                            try:
                                # Randomly generate a status message, between this and a random caption this should cause
                                # the services like tumblr and twitter from encountering issues with using the same message
                                # more than once. Preventing their systems from blocking 'spam' (not that this is spam)
                                if(x == 0):
                                    status = "#NPC / #NoPantsCrew (" + today + ") Visit " + STREAMER_NAME + " over on #Twitch. " + WEBSITE_NAME
                                elif(x==1):
                                    status = "#NPC (" + today + ") Visit " + STREAMER_NAME + " over on " + WEBSITE_NAME + "."
                                elif(x==2):
                                    status = "#NPC (" + today + ") Visit " + STREAMER_NAME + " over on #Twitch. " + WEBSITE_NAME
                                elif(x==3):
                                    status = "#NoPantsCrew (" + today + ") Visit " + STREAMER_NAME + " over on #Twitch. " + WEBSITE_NAME
                                elif(x==4):
                                    status = "#NPC (" + today + ") Visit me on #Twitch. " + WEBSITE_NAME
                                elif(x==5):
                                    status = "#NoPantsCrew #NPC (" + today + ") " + STREAMER_NAME + " on ze #Twitch. " + WEBSITE_NAME
                                else:
                                    status = "#NPC (" + today + ") Visit " + STREAMER_NAME + " over on #Twitch. " + WEBSITE_NAME
    
                                # assign the caption to use (for science)
                                the_caption = captions_to_use[random.randrange(0, len(captions_to_use)-1)]
                                
                                # are we going to translate?
                                if (random.randrange(0,5) == 3):
                                    x = random.randrange(0,5)
                                    if(x == 0):
                                        status = translator.translate(status, dest='ru')
                                        the_caption = translator.translate(the_caption, dest='ru')
                                    elif(x == 1):
                                        status = translator.translate(status, dest='ja')
                                        the_caption = translator.translate(the_caption, dest='ja')
                                    elif(x == 2):
                                        status = translator.translate(status, dest='fr')
                                        the_caption = translator.translate(the_caption, dest='fr')
                                    elif(x == 3):
                                        status = translator.translate(status, dest='la')
                                        the_caption = translator.translate(the_caption, dest='la')
                                    elif(x == 4):
                                        status = translator.translate(status, dest='ko')
                                        the_caption = translator.translate(the_caption, dest='ko')
                                    elif(x == 5):
                                        status = translator.translate(status, dest='eo')
                                        the_caption = translator.translate(the_caption, dest='eo')
                            
                            except Exception as e:
                                print('An exception has occured, possibly in translations')
                                print(e)
                                print('Autocorrecting status and caption to defaults.')
                                status = "#NPC / #NoPantsCrew (" + today + ") Visit " + STREAMER_NAME + " over on #Twitch. " + WEBSITE_NAME
                                the_caption = captions_to_use[random.randrange(0, len(captions_to_use)-1)]

                            # add our website to the caption to link back to the OG content.
                            the_caption = the_caption + ' ' + WEBSITE_NAME
                                
                            imagePath = push_array[0]       # get the image/video path

                            # Debugging code to help track everything nicely.
                            Logger("Status update: %s\nImage Path: %s" % (status, imagePath) )

                            push_array.remove(imagePath)               # push the old image off the stack

                            # blank response is key
                            response = '{}'

                            if (string_found(imagePath, 'png') != False):
                                print("Attempting to queue photo post:")
                                response = client.create_photo('livesimmy.tumblr.com', state="published", tags=tags_to_use, caption=the_caption, tweet=status, data=imagePath)                    
                            elif (string_found(imagePath, 'mp4') != False):
                                print("Attempting to queue video post:")
                                response = client.create_video('livesimmy.tumblr.com', state="published", tags=tags_to_use, caption=the_caption, tweet=status, data=imagePath)
                            else:
                                response = '{UNKNOWN TYPE PROVIDED - Skipping}'

                            ticker = 0                      # reset the ticker to 0

                            # help randomize the amount of 'ticks' until the content is posted to tumblr
                            # this will help avoid the appearance of being 'a bot', which is what we want to
                            # avoid because we do not want the tumblr service to prevent our uploading
                            if(old_timer < 400):
                                old_timer = the_timer
                                the_timer = random.randrange(450, 700)

                            else:
                                old_timer = the_timer
                                the_timer = random.randrange(250, 600)
                            
                            print("--------------------------------------------------------------------------------")

                            # the state is in the response? It should read transcoding to be accurate.
                            if "state" in response:
                                print("File state: %s" % response['state'])
                            elif "errors" in response:
                                print("An error was encountered (details below), pushing the imagePath to the back of the array.")
                                push_array.append(imagePath);
                            else:
                                print("Unknown state has been reached, expect an exception below.");

                            # Response should always be from tumblr
                            print("JSON Response from Tumblr:")
                            print(json.dumps(response, indent=4))


                            print("--------------------------------------------------------------------------------")
                            if(len(push_array) != 0):
                                print('\n\nRemaining entries')
                                print(*push_array, sep = "\n")
                            print ("Next post is in %d seconds or %d minutes." % ((the_timer * SECONDS_TO_SLEEP), (the_timer * SECONDS_TO_SLEEP)/60 ) )
                    except Exception as e:
                        print("Error occured within array handler:")
                        print(e)
                
        except Exception as e:
            self.observer.stop()
            print ("Error with the watcher:")
            print (e)

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            Logger("Received created event - %s." % event.src_path)

            found = False

            # Validate that the file type discovered is actually one that we can push
            # to twitter. (This is vital to ensure we don't push somethin that should be pushed)
            if (string_found(event.src_path, 'png') != False):
                found = True
                print("New photo found")
            elif (string_found(event.src_path, 'mp4') != False):
                found = True
                print("New video found")
            else:
                found = False

            # Moving on to bigger and brighter things
            if found: 
                # load image/video
                imagePath = event.src_path # this should be the file that was created

                push_array.append(imagePath)
                #print (push_array)

            else:
                Logger("File is not an approved type")

        #elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            # this print statement will be removed when we are done debuggin the application.
            #Logger("Received modified event - %s." % event.src_path)


###########################################################################################################
# Prostitute the mission, I mean, execute the script function.
if __name__ == '__main__':

    ###########################################################################################################
    # Consumer keys and access tokens, used for OAuth
    # you will need to generate these on tumblr.com

    print("--------------------------------------------------------------------------------")
    print("Loading credentials")
    with open('tumblr_credentials.json', 'r') as f:
        credentials = json.loads(f.read())
        client = pytumblr.TumblrRestClient(credentials['consumer_key'], credentials['consumer_secret'], credentials['oauth_token'], credentials['oauth_token_secret'])

    print("--------------------------------------------------------------------------------")
    print (json.dumps(client.info(), indent=4))
    print("--------------------------------------------------------------------------------")

    print("Initiating Watcher class");
    # Create watcher
    w = Watcher()

    # Execute the watcher script
    print("Watcher executed")
    w.run()

###########################################################################################################
#EOF
