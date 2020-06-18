# EDIT THESE
churchname = "My Church"
user = "yoursubsplashusername"
passwd = "yoursubsplashpw"

filepath = "path/to/your/video.mp4"
videoname = "Title of your video"

# This program will not create the media series in Subsplash for you. 
# Make sure this is taken care of prior to running this script, otherwise
# the series will be left as blank during the upload process.
series = {
    "June 2020": "The Physics of Faith", 
    "May 2020": "Enjoying Good Health",
    "July 2020": "Example Series"
    }

###########################################
# DON'T TOUCH ANYTHING BELOW THIS LINE :) #
###########################################

from main import Church

c = Church(name=churchname, user=user, passwd=passwd, series=series)

c.upload(video=filepath, name=videoname)