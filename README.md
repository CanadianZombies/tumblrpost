# twitterpost
########################################################################################################################################
A script that will take any new files of an approved file-type, and post them to twitter.

Requires you to understand the oauth process. You will need to visit dev.twitter.com and create an 'application' to link your
twitter to this application (oauth requirement).

This script also requires that you have the 3rd party module tweepy. This can be installed via PIP.
      http://docs.tweepy.org/en/latest/   (link to tweepy's docs)

########################################################################################################################################
How this works:
It monitors your specified directory, scans it every 5 seconds, and if there is a new file created in that directory within
that timeframe, it will evaluate it against the criteria provided (approved file extensions) and if it matches, it will
proceed to generate a tweet with your username, a witty statement, the date/time group, and a link to your website.

It will also attach the image/video file and post it to twitter on your behalf.


########################################################################################################################################
** THIS HAS NOT BEEN TESTED YET **
Be warned that as this is not tested, it may not work, or may require minor editing to get up and running.
I will be testing this when time provides and posting a corrected version.

A note on the lack of testing, the source code has been run through PythonBuddy (pylint) for accuracy and it is
up to standard. However it has not been executed as tweepy, a third party module is not able to be tested using this
method. However functionally speaking, the code should work without error.

This is expected to work with Python 3.4 with minimal work as that is what it was designed for.

########################################################################################################################################
** WHY WAS THIS WRITTEN **
I do streaming on dlive.tv (http://www.dlive.tv/SimmyDizzle) and as a result of that, I tend to take screenshots and instant replay
videos (30-60 second clips). I wanted a quick way to automatically post them to my social media. As I have them saving to one folder
it made sense to just generate a quick system, I hit F2, it takes a 30 second video capture, the script runs as it is always running,
it sees a new file created, it tosses it to twitter. Blamsauce, done. No work for me, middle of my stream it posts, and I don't have to
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
part as this is intended to be a seemless/smooth script, hiding away in the background uploading files to twitter for you.

