# twitterpost
A script that will take any new files of an approved file-type, and post them to twitter.

This script has not been tested yet, it will most likely require additional python files culled from PIP to work properly.
And it will require you to create a new 'application' and put in the proper information from the dev.twitter.com site.
This will be your key information.

How this works:
It monitors your specified directory, scans it every 5 seconds, and if there is a new file created in that directory within
that timeframe, it will evaluate it against the criteria provided (approved file extensions) and if it matches, it will
proceed to generate a tweet with your username, a witty statement, the date/time group, and a link to your website.

It will also attach the image/video file and post it to twitter on your behalf.

** THIS HAS NOT BEEN TESTED YET **
Be warned that as this is not tested, it may not work, or may require minor editing to get up and running.
I will be testing this when time provides and posting a corrected version.

This is expected to work with Python 3.6 with minimal work as that is what it was designed for.


** WHY WAS THIS WRITTEN **
I do streaming on dlive.tv (http://www.dlive.tv/SimmyDizzle) and as a result of that, I tend to take screenshots and instant replay
videos (30 second clips). I wanted a quick way to automatically post them to my social media. As I have them saving to one folder
it made sense to just generate a quick system, I hit F2, it takes a 30 second video capture, the script runs as it is always running,
it sees a new file created, it tosses it to twitter. Blamsauce, done. No work for me, middle of my stream it posts, and I don't have to
do anything to make it happen.

I am incredibly lazy that way. So with that said, I do not know if this works entirely yet, and I will probably spend a month debugging it
but it is something that I feel will benefit the world. So I am sharing it with everyone.
