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
