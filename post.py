###########################################################################################################
#                         Tumblr AUTOPOST script by David Simmerson (SimmyDizzle)                         #
###########################################################################################################
# Please think of the children, on tumblr we can post 10 videos per day via API calls.                    #
# Or a maximum of 5 minutes of video content. 30 second clips * 10 = 5 minutes if my math is right.       #
# Or 5 1 minute videos. Keep this in mind.                                                                #
###########################################################################################################
# Images can be posted at a rate of 150 per day. The system only detects png files for the time being.    #
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
from datetime import date

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
# list of phrases used in tweet generation (we can keep adding these)
# the idea will be like STREAMER_NAME + COMMENT, so like 'SimmyDizzle is on a roll!' will be generated.
phrases = [
    ' strikes again!',
    ' has struck again!',
    ' is on a roll!',
    ' cannot believe its not butter!',
    ' has something special here.',
    ' needs your approval! Hit that like and follow button!',
    ' cannot believe it!',
    ' would like to your opinion!',
    ' is this the flavour of the month?',
    ' what do you think?',
    ' gamer extroadinaire!',
    ' lover extroadinaire!',
    ' is thinking about an onlyfans page, ya know, for science.',
    ' has let loose something here!',
    ' thinks this is interesting enough to share.',
    ' is out of crazy ideas.'
    ' could fap to this.'
    ' would fap to this.'
    ' has fapped to this.'
    ' has truly gone mad!',
    ' is thinking this is something everyone should see.'
    ' is thinking this is badass.'
    ' is wondering if you could give me your thoughts on this.'
    ' is pontificating existence, and this.',
    ' would like to know what you think of this.',
    ' has a crazy idea.',
    ' had a crazy idea.',
    ' would like you to give a follow.',
    ' would like you to share this around.',
    ' would like you to RT this.',
    ' requires you to fap to this, or RT.',
    ' requires you to fap to this, or RT, choice is yours.',
    ' requests you clickity on that RT button!',
    ' thanks you for your viewership.',
    ' thanks you for being here.',
    ' thanks you for caring.',
    ' is thirsty.',
    '...',
]

#########################################################################################################
# This block does NOT use the STREAMER_NAME variable at all in the generation, this is just a straight up
# random generation string. (Completed) with the reason of being stuff that should not be randomly generated.
# Basically this is for complete sentences that do not need the streamers name.
captions_to_use = [
    'Crazy times',
    'What up fam!',
    'Check this out fam',
    'What do you guys think?',
    'Is this the flavour of the month?',
    'Thoughts?',
    'Rip or Nah?',
    'Well fam, join me on stream!',
    'Remember to join me on stream!',
    'Remember I stream, so join me!',
    'Drop that follow here, and on stream!',
    'Hit that like and follow button fam!',
    'Captions tend to be random',
    'Sauce?',
    'Tarnations!',
    'Has this made you thirsty for me? It should!',
    'Join the No Pants Crew Discord: https://discord.gg/FnQrQ5N',
    'Do not forget to join the No Pants Crew Discord: https://discord.gg/FnQrQ5N',
    'The No Pants Crew and I invite you to check this shit out!',
    'The No Pants Crew and I invite you to check this out!',
    'The No Pants Crew and I invite you to follow us on stream!',
    'Git-Sum',
    'Is that a challenge?',
    'I think that is a challenge.',
    'Caption this',
    'Do not forget to follow!',
    'If you like this, hit that RT and like button!',
    'RT this if you like it!',
    'Do not forget to like this post!',
    'Feedback people?',
    'I\'d like some feedback on this.',
    'Like, follow, subscribe to my page, see my profile for details!',
    'Follow, like, these things are important!',
    'Spread the word!',
    'Hit that RT button!'
    'Share me with your family and friends, awww yeee.',
    'Share me with your family and friends!',
    'Share me with your family, I am a treat!',
    'RT me to your grandma!'
    'What are your thoughts on this?',
    'Hey, what is your take on this?',
    'Fam, serious question, what do you think?',
    'Heresy, this is heresy!',
    'Exterminatus!',
    'I would like to know your opinion on this matter.',
    'Do tell me what you think.',
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
    'Thank you for looking at this.',
    'Thanks be to you for your viewership!',
    'do dew do do',
    'Want some more?',
    'Would you like more?',
    'If you could, would you want more?',
    'More is better than less, would you like more?',
    'Your thoughts?',
    'Emoji for your thoughts?',
    'What ya think of this?',
    'Ha!',
    'Follow me for more of this stuff, here, in this. Yeah.',
    'Follow me for more of this!',
    'Give a follow if you like what you see!',
    '[Hypnotoad Eyes] Follow Me, Share Me, subscribe to me [/Hypnotoad Eyes]',
    '[Hypnotoad Eyes] Follow Me, Share Me, subscribe to me [/Hypnotoad Eyes] What was that?',
    '[Hypnotoad Eyes] Follow Me, Share Me, subscribe to me [/Hypnotoad Eyes] Yussssss!',
    'I am just a click away from being followed, give that click, do it, do it do it do it!',
    'I am not wearing pants, or am I. No Pants Crew for Life!', 
    'Guess what I was thinking.',
    'Do you know what I was thinking?',
    'Uhh, blamsauce?',
    'Blam to the sauce!',
    'Winner Winner drinking paint thinner!',
    'RT for clout!',
    'RT for prestige!', 
    'Retweet for clout!',
    'Retweet for prestige!',
    'Oooh Shiny!',
    'Pizzazz!',
    '...',
    'I suggest recklessness!'
]

#########################################################################################################
# this is the easier way to generate strings for random messages. The messages above while working
# are not always the best bets. This method here is more 'creative' as they generate multiple methods
# of hilarity within the string. Depending how we sculpt this, we could have thousands of possibilities
# with minimal work.
# STREAMER_NAME + rand_1 + rand_2 + rand_3 + rand_4 = caption ?
rand_1 = [
    ' is',
    ' was',
    ' continues',
    ' continued',
    ' persists at',
    ' prevails at',
    ' is proficiently',
    ' cannot be'
    ' the badass is',
    ' the badass was',
    ' the badass continues',
    ' the true badass is',
    ' the simplord is',
    ' the simplord was',
    ' the badass simplord is',
    ' the badass simplord was',
    ' the badass simplord continues',
    ', the pimp, is',
    ', the simp, is',
    ', the pimp, was',
    ', the simp, was',
    '(NPC Founder) was',
    '(NPC Founder) is',
    '(NPC Founder) continues',
    '(NPC Founder) continued',
    '\'s is here, ',
    '\'s was here, '
]

rand_2 = [
    ' gaming',
    ' playing games',
    ' streaming games',
    ' winning games',
    ' streaming',
    ' playing',
    ' crushing',
    ' rocking',
    ' blasting'
    ' dominating',
    ' dominating it',
    ' winning',
    ' losing',
    ' crushing it',
    ' battling',
    ' winning it',
    ' playing it',
    ' rocking it'
]

rand_3 = [
    ' hardcore',
    ' advantageously'
    ', hardcore',
    ' hardcore porn style',
    ', masterfully',
    ' hardcore, 100% masterclass',
    ' masterfully',
    ' with masterclass style',
    ' with skill',
    ' with style',
    ' with clout',
    ' with the right stuff',
    ' with what it takes',
    ' exemplifying skill',
    ' with pizzazz',
    ' with might and main',
    ' exemplifying technique',
    ' famously',
    ' sensationally',
    ' awkwardly',
    ' badly',
    ' poorly',
    ' swimmingly',
    ' swimmingly well',
    ' seemingly well',
    ' well'
]

rand_4 = [
    '.',
    '.',
    '.',
    '.',
    '.',
    '.',
    '!',
    ', thoughts?',
    '?',
    '??',
    '!!',
    '..',
    ', maybe.',
    ', maybe!',
    ', maybe?',
    ', perhaps.',
    ', perhaps!',
    ', perhaps?',
    ', perhaps...',
    '...',
    ', maybe...',
    ', thoughts...',
    ', thoughts?!?',
    ', for your consideration.'
]

###########################################################################################################
# array for tracking files to push.
push_array = [] # empty array(list).
exceeded_files = []
broken_files = []

# Start the google translator (we need this for later)
translator = Translator()

###########################################################################################################
##                               CONFIGURATIONAL SETTINGS FOR THE TWEET                                  ##
###########################################################################################################
# This is how many seconds the application will sleep between system passes
SECONDS_TO_SLEEP = 5 # 5 seconds was old default

# CHANGE ME -- This is the folder where your new files will be scraped from!
PATHS = ['C:\\Users\mysuername\\Videos\\Replays','C:\\Users\\myusername\\Videos\\Captures']       # Future

# Streamer-Name
STREAMER_NAME = "SimmyDizzle"             #Put your streamername here

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

###########################################################################################################
# Write the files to flatfile.
def writeFiles():
    with open('phrases.dat', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in phrases)

    with open('captions_to_use.dat', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in captions_to_use)

    with open('rand_1.dat', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in rand_1)

    with open('rand_2.dat', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in rand_2)
        
    with open('rand_3.dat', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in rand_3)

    with open('rand_4.dat', 'w') as filehandle:
        filehandle.writelines("%s\n" % place for place in rand_4)

###########################################################################################################
# open our flat-files that we have dumped.
def openFiles():
    with open('phrases.dat', 'r') as filehandle:
        phrases = [current_place.rstrip() for current_place in filehandle.readlines()]
  
    with open('captions_to_use.dat', 'r') as filehandle:
        captions_to_use = [current_place.rstrip() for current_place in filehandle.readlines()]

    with open('rand_1.dat', 'r') as filehandle:
        rand_1 = [current_place.rstrip() for current_place in filehandle.readlines()]

    with open('rand_2.dat', 'r') as filehandle:
        rand_2 = [current_place.rstrip() for current_place in filehandle.readlines()]

    with open('rand_3.dat', 'r') as filehandle:
        rand_3 = [current_place.rstrip() for current_place in filehandle.readlines()]

    with open('rand_4.dat', 'r') as filehandle:
        rand_4 = [current_place.rstrip() for current_place in filehandle.readlines()]
        
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
        currentDate = date.today()
        lastDate = currentDate
        
        try:
            ticker = 0
            # this loop is infinite! (Unless we crash)
            while True:
                today = time.strftime("%Y-%m-%d %H:%M") # Year-Month-Day Hour:Minute
                
                lastDate = currentDate                  # datetime tracking
                currentDate = date.today()              # change the currentDate value
                
                # if we changed current day, check against the exceeded_files array
                # and restore any pending files
                if (lastDate != currentDate)
                    if(len(exceeded_files) > 0):
                        for h in exceeded_files:
                            push_array.append(h)
                            exceeded_files.remove(h)
                            
                        print('\n\Added entries from exceeded_files array:')
                        print(*push_array, sep = "\n")   
                
                # sleep the script for a specified length of time
                time.sleep(SECONDS_TO_SLEEP)            # Configured above

                ticker = ticker +1                      # ticker +1, counting up to our goal

                # The ticker will go up by one every SECONDS_TO_SLEEP. Default value of 5 seconds.
                # the_timer will be given a value (in seconds to sleep). Therefore, the total time
                # for the next 'execution' of the code below will be the_timer * SECONDS_TO_SLEEP (in real time)
                # Defaulting to 5 seconds works wonderfully, I recommend not changing this value.
                if ticker >= the_timer:
                    try:
                        if len(push_array) != 0:
                            x = random.randrange(0,5)

                            try:
                                # Randomly generate a status message, between this and a random caption this should cause
                                # the services like tumblr and twitter from encountering issues with using the same message
                                # more than once. Preventing their systems from blocking 'spam' (not that this is spam)
                                # This fills the 'tweet' block, which is not-used unless you have your tumblr autoposting to your twitter
                                # which does *NOT* always work. This is why IFTTT has been used in this.
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
                                rx = random.randrange(0,3);
                                if(rx == 0):
                                    the_caption = captions_to_use[random.randrange(0, len(captions_to_use)-1)]
                                elif(rx == 1):
                                    the_caption = STREAMER_NAME + phrases[random.randrange(0, len(phrases)-1]
                                elif(rx == 2:
                                    the_caption = STREAMER_NAME + rand_1[random.randrange(0, len(rand_1)-1)] + rand_2[random.randrange(0,len(rand_2)-1)] + rand_3[random.randrange(0,len(rand_3)-1)] + rand_4[random.randrange(0,len(rand_3)-1)]
                                else:
                                    the_caption = captions_to_use[random.randrange(0, len(captions_to_use)-1)]
                                     
                                # are we going to translate?
                                if (random.randrange(0,5) == 3):
                                    x = random.randrange(0,7)
                                    if(x == 0):
                                        tr_status = translator.translate(status, dest='ru')
                                        tr_the_caption = translator.translate(the_caption, dest='ru')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     elif(x == 1):
                                        tr_status = translator.translate(status, dest='ja')
                                        tr_the_caption = translator.translate(the_caption, dest='ja')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     elif(x == 2):
                                        tr_status = translator.translate(status, dest='fr')
                                        tr_the_caption = translator.translate(the_caption, dest='fr')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     elif(x == 3):
                                        tr_status = translator.translate(status, dest='la')
                                        tr_the_caption = translator.translate(the_caption, dest='la')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     elif(x == 4):
                                        tr_status = translator.translate(status, dest='ko')
                                        tr_the_caption = translator.translate(the_caption, dest='ko')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     elif(x == 5):
                                        tr_status = translator.translate(status, dest='eo')
                                        tr_the_caption = translator.translate(the_caption, dest='eo')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     elif(x == 6):
                                        tr_status = translator.translate(status, dest='de')
                                        tr_the_caption = translator.translate(the_caption, dest='de')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     else:
                                        tr_status = translator.translate(status, dest='hi')
                                        tr_the_caption = translator.translate(the_caption, dest='hi')
                                        status = tr_status.text
                                        the_caption = tr_status.text
                                     
                            except Exception as e:
                                print('An exception has occured, possibly in translations')
                                print(e)
                                print('Autocorrecting status and caption to defaults.')
                                status = "#NPC / #NoPantsCrew (" + today + ") Visit " + STREAMER_NAME + " over on #Twitch. " + WEBSITE_NAME
                                the_caption = captions_to_use[random.randrange(0, len(captions_to_use)-1)]

                            ####################################################################################################
                            # add our website to the caption to link back to the OG content.
                            the_caption = the_caption + ' (' + WEBSITE_NAME + ')'
                                
                            imagePath = push_array[0]       # get the image/video path

                            # Debugging code to help track everything nicely.
                            Logger("Status update: %s\nImage Path: %s\nCaption update: %s\n" % (status, imagePath, the_caption) )

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
                                # Photos we don't need long wait times for to post the next content
                                # we don't want to wait an hour if we do not need to, but we still want
                                # to be random.
                                if (string_found(imagePath, 'png') != False):
                                    the_timer = random.randrange(150, 450)
                                else
                                    the_timer = random.randrange(450, 700)
                            else:
                                old_timer = the_timer
                                # same thing here, no need to hold thinsg up for a png file.
                                # tumblr accepts those without much issue.
                                if (string_found(imagePath, 'png') != False):
                                    the_timer = random.randrange(250, 600)
                                else:
                                    the_timer = random.randrange(400, 650)
                            
                            print("--------------------------------------------------------------------------------")

                            # the state is in the response? It should read transcoding to be accurate.
                            if "state" in response:
                                print("File state: %s" % response['state'])
                            elif "errors" in response:
                                print("An error was encountered (details below), pushing the imagePath to the back of the array.")
                                print(response['errors'])
                                if "8009" in response['errors']:
                                     # 8009 is used when videos encounter an issue on upload.
                                     broken_files.append(imagePath)
                                elif "8011" in response['errors']:
                                     # error 8011 is when we have exceeded our daily quota for videos
                                     exceeded_files.append(imagePath)
                                else:
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
                            else:
                                # let us re-try those broken files shall we?
                                if(len(broken_files) > 0):
                                    for h in broken_files:
                                        push_array.append(h)
                                        broken_files.remove(h)
                                     
                                    print('\n\Added entries from broken_files array:')
                                    print(*push_array, sep = "\n")   
                                     
                            #######################################################################################################
                            # Print out when the next post will be. For those interested in it.
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

    # attempt to open our flat-files (important)
    #writeFiles()
    #openFiles()

    print("Initiating Watcher class");
    # Create watcher
    w = Watcher()

    # Execute the watcher script
    print("Watcher executed")
    w.run()

###########################################################################################################
#EOF
