orgname = "My Org"
user = "yoursubsplashusername"
passwd = "yoursubsplashpw"

# This program will not create the media series in Subsplash for you. 
# Make sure this is taken care of prior to running this script, otherwise
# the series will be left as blank during the upload process.
series = {
    "June 2020": "Series", 
    "May 2020": "Another Series",
    "July 2020": "Example Series"
    }

from main import Org

c = Org(name=orgname, user=user, passwd=passwd, series=series)

# Example of uploading a singular video
filepath = "path/to/your/video.mp4"
videoname = "Title of your video"
c.upload(video=filepath, name=videoname)

# Example of uploading multiple videos from a folder
folderpath = "path/to/a/folder/with/videos"
c.bulkUpload(folderpath)