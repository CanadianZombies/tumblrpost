# tumblrpost
########################################################################################################################################
A script that will take any new files of an approved file-type, and post them to tumblr.

Requires you to understand the oauth process. You will need to visit tumblr.com and create an 'application' to link your
tumblr to this application (oauth requirement).

This script also requires that you have the 3rd party module PyTumblr, watchdog, and observer.
Commands to run:

      pip install pytumblr
      pip install watchdog
      pip install observer
      pip install googletrans

This script was originally designed to work with twitter however, the devs at twitter denied my application request so I could not get
the appropriate oauth configuration to build the application. I have since then moved to using tumblr. This change works perfectly. If
you still want to push your post over to twitter, I highly recommend using IFTTT (if this than that).

########################################################################################################################################
How this works:
It monitors your specified directory, scans it every 5 seconds, and if there is a new file created in that directory within
that timeframe, it will evaluate it against the criteria provided (approved file extensions) and if it matches, it will
proceed to generate a tweet with your username, a witty statement, the date/time group, and a link to your website.

It will also attach the image/video file and post it to tumblr on your behalf.

The files will sit in a queue that processes roughly every 25 minutes, and will publish one at a time. It does this because tumblr will
not allow you to publish more than one video at a time, it will reject the file while another one is processing. So I gave it a brief
moment between each post without returning an invalid response. Tumblr also has a daily limit of 250 posts. So that is something to be
aware of as well, however it will do the trick.

I have configured this to publish to tumblr, then I use IFTTT to push the content to twitter. This is the easiest method I have come
across to handle this unless twitter decides to approve my application next time I apply. Which I will do.

*** UPDATE ***
This system now uses googletrans from PyPi, this will translate the 'caption' string and status into different languages.
This is so that these can reach different groups of people. Hopefully. (Has been tested, officially works)
########################################################################################################################################
** load/save data files. **
The system now loads data-files from flat-file. I left the 'writing' routines in the main code for now, if you want to write
the arrays it is doable that way if you do not want to use flatfiles.  The flatfiles have been made available in this repository
as is for how I use them on my stream.

########################################################################################################################################
** captions **
The captions have 3 separate systems that build up. The third system is the biggest and most complicated system as it generates 
hundreds of thousands of options based on the variables provided. The first two systems are set phrases, one that uses the STREAMER_NAME
and one that does not use the STREAMER_NAME.

Additionally it has been added to randomly translate these captions into different languages. I intend to clean up this system
some more and make it easier for us to translate into more languages. This is great for reaching different audiences throughout
the internet.

########################################################################################################################################
** THIS HAS NOT BEEN TESTED YET **
Be warned that as this is not fully tested, it may not work, or may require minor editing to get up and running.
I will be testing this when time provides and posting a corrected version.

A note on the lack of testing, the source code has been run through PythonBuddy (pylint) for accuracy and it is
up to standard. However it has not been executed as tweepy, a third party module is not able to be tested using this
method. However functionally speaking, the code should work without error.

This is expected to work with Python 3.4 with minimal work as that is what it was designed for.

########################################################################################################################################
** WHY WAS THIS WRITTEN **
I do streaming on twutch.tv (http://www.twitch.tv/SimmyDizzle) and as a result of that, I tend to take screenshots and instant replay
videos (30-60 second clips). I wanted a quick way to automatically post them to my social media. As I have them saving to one folder
it made sense to just generate a quick system, I hit F2, it takes a 30 second video capture, the script runs as it is always running,
it sees a new file created, it tosses it to tumblr. Blamsauce, done. No work for me, middle of my stream it posts, and I don't have to
do anything to make it happen.

I am incredibly lazy that way. So with that said, I do not know if this works entirely yet, and I will probably spend a month 
debugging it but it is something that I feel will benefit the world. So I am sharing it with everyone.

########################################################################################################################################
** UPDATES **
A multitude of updates have been issued to this code without it ever being tested (properly tested). It has been tested against syntax
for correct usage. It matches appropriately according to pylint. More changes are going to come to this code. If you test this system
please feel free to let me know what you did to make it work, if there were any issues/etc so I can tweak up the main source and prevent
future issues with later releases.

########################################################################################################################################
** FUTURE **
Currently the settings for this script are all configured within the script itself, to be a little more 'future-proof' I want to create 
a configurational file, probably JSON format that will contain all the information for the config process. This will allow for faster
updates with the script. Additionally I want to include an 'auto-updater' that contacts the git repository and downloads the latest
version. (obviously this would be disabled by default). But addressing security issues, glitches, changes in approved formats, etc
would be easier to be managed at the global level instead of the local level. I.E. You patching it when I can be patching it.

Aside from the config update (yet to come), the only other updates / planned changes for the future are that of bug fixes and possibly
optimizations to the source to ensure that it is not bogging down the system it is running on. This is obviously the most important
part as this is intended to be a seemless/smooth script, hiding away in the background uploading files to tumblr for you.

I am going to add instagram into the mix here as well. I am applying for a developer api key for instagram. The goal being to be able
to automatically upload to instagram as well. Same files, different queue. This is an easy measure for development so long as instagram
approves the application. As policy has changed for 3rd party application development with instagram, this may be a ways out.
