# The plan:
    # 0) have a dictionary where keys are Month + Year and the value is the Sermon series (you could use S1 to manage this! or we could try goJSON)
    # 1) post to dashboard.thechurchapp.org w/ email + password to login
    # 2) get https://dashboard.thechurchapp.org/18953/#/library/media
    # 3) click on the button element with id ember398 (this is the create media item button)
    # 4) enter today's date into the input with id ember405 (this is the title)
    # 5) click on the option inside the select element inside div id ember301 that matches the sermon series that the video was made in (using dictionary from 0)
    # 6) click on button id ember412 to create item
    # 7) on the page that loads, upload the video to the input with id="ember677_fileUploader" 
    # 8) wait until the div inside div id ember709 has style="width:100%" (this means the video has been fully uploaded)
    # 9) i forgot to get the id for the publish button, but y'know, click that

from datetime import datetime

def getTime():
    return (datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ": ")

def log(msg):
    print(f"{getTime()}{msg}")

class Church:
    def __init__(self, name="Generic Church", series={}, user="", passwd=""):
        self.name = name
        self.series = series
        self.user = user
        self.passwd = passwd

    def addSeries(self, month, year, name):
        self.series[f"{month} {year}"] = name