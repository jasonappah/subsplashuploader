# The plan:
    # 0) have a dictionary where keys are Month + Year and the value is the Sermon series (you could use S1 to manage this! or we could try goJSON) --DONE
    # 1) post to dashboard.thechurchapp.org w/ email + password to login - done
    # 2) get https://dashboard.thechurchapp.org/18953/#/library/media - done 
    # 3) click on the button element with id ember398 (this is the create media item button) - done
    # 4) enter today's date into the input with id ember405 (this is the title) - done
    # 5) click on the option inside the select element inside div id ember301 that matches the sermon series that the video was made in (using dictionary from 0) - done
    # 6) click on button id ember412 to create item - done
    # 7) on the page that loads, upload the video to the input with id="ember677_fileUploader" - done
    # 8) wait until the div inside div id ember709 has style="width:100%" (this means the video has been fully uploaded) - DONE
    # 9) i forgot to get the id for the publish button, but y'know, click that - done!!!

import time, os
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
ALLOWED_EXT=["mp4","m4v","mov","wmv","flv"] 

def getTime():
    return (datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ": ")

def log(msg):
    print(f"{getTime()}{msg}")

class Church:
    def __init__(self, name="Generic Church", user="", passwd="", series={}):
        self.name = name
        self.series = series
        self.user = user
        self.passwd = passwd
        log(f"Created a new church: {name}")

    def addSeries(self, month, year, name):
        self.series[f"{month} {year}"] = name
        log(f"Added series: {month} {year} - {name}")
    
    def validateVideo(self, video):
        log(f"Validating video {video}")
        video = os.path.abspath(video)
        tmp = video.split(".")
        if tmp[-1] in ALLOWED_EXT:
            log("This is a valid video.")
            return video
        else:
            log("This is not a valid video.")
            return False

    def upload(self, video="", name=""):
        video = self.validateVideo(video)
        if video == False:
            log("Can't upload an invalid video. Stopping this upload...")
            return False
        log(f"Beginning to upload video to Subsplash: {video}")

        try:
            videocreationdate = datetime.fromtimestamp(int(os.path.getmtime(video)))
            if name == "":
                name = videocreationdate.strftime("%B %d, %Y")
        except Exception as e:
            log("Something went wrong! Unable to get the video creation date.")
            log(e)
            return False

        log(f"Video title {name}")

        videomonthyear = videocreationdate.strftime("%B %Y")
        series = ""
        
        # Starting the browser
        try:
            log("Starting browser...")
            opts = Options()
            browser = Chrome(options=opts)
            browser.get('https://dashboard.thechurchapp.org')
            log("Started browser.")
        except Exception as e:
            log("Something went wrong! Unable to start the browser.")
            log(e)
            try:
                browser.quit()
            except:
                pass
            return False

        # Logging in
        try:
            browser.find_element_by_id('Email').send_keys(self.user)
            browser.find_element_by_id('Password').send_keys(self.passwd)
            browser.find_element_by_id('js-login-form-submit').click()
            log("Logged in.")
        except Exception as e:
            log("Something went wrong! Unable to login.")
            log(e)
            browser.quit()
            return False

        # Navigating to on-demand page
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ember-action-53='53']")))
            browser.find_element_by_xpath("//button[@data-ember-action-53='53']").click()
        except Exception as e:
            log("Something went wrong! Unable to open the on-demand page. Maybe we weren't able to login?")
            log(e)
            browser.quit()
            return False

        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "ember60")))
            browser.find_element_by_id("ember60").click()
            log("Opened the on-demand page.")
        except Exception as e:
            log("Something went wrong! Unable to open the on-demand page. Maybe we weren't able to login?")
            log(e)
            browser.quit()
            return False

        # Clicking the create media item button
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ga-event-action='create media item']")))
            browser.find_element_by_xpath("//button[@data-ga-event-action='create media item']").click()
            log("Clicked the create media item button.")
        except Exception as e:
            log("Something went wrong! Unable to click the create media item button.")
            log(e)
            browser.quit()
            return False

        # Typing in the Media title
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//label/input[@type='text']")))
            browser.find_element_by_xpath("//label/input[@type='text']").send_keys(name)
            log("Typed in the media title.")
        except Exception as e:
            log("Something went wrong! Unable to type in the media title.")
            log(e)
            browser.quit()
            return False
        
        # Selecting the sermon series
        try:
            if videomonthyear in self.series.keys():
                series = self.series[videomonthyear]
            for i in browser.find_elements_by_class_name("kit-select__option"):
                if i.text.strip() == series:
                    i.click()
                    log(f"Clicked series {i.text.strip()}")
                    break
                else: 
                    print(f"Series: {i.text.strip()}")
            if series == "":
                log("Couldn't get a series from the video provided. Maybe the timestamp on the video is wrong.")
        except Exception as e:
            log("Something went wrong! Unable to select a sermon series or skip the selection of a series.")
            log(e)
            browser.quit()
            return False

        # clicking the submit button
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ga-event-action='create']")))
            browser.find_element_by_xpath("//button[@data-ga-event-action='create']").click()
            log("Clicked the create button.")
        except Exception as e:
            log("Something went wrong! Unable to click the create button.")
            log(e)
            browser.quit()
            return False

        # inputting the date
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='MM/DD/YYYY']")))
            browser.find_element_by_xpath("//input[@placeholder='MM/DD/YYYY']").send_keys(videocreationdate.strftime("%m/%d/%Y"))
            log("Inputted video date.")
        except Exception as e:
            log("Something went wrong! Unable to input video date.")
            log(e)
            browser.quit()
            return False

        # uploading the video
        try:
            browser.find_element_by_xpath("//label[@class='sui-media-uploader__content']/div/input[@type='file']").send_keys(video)
            log("Beginning to upload video.")
        except Exception as e:
            log("Something went wrong! Unable to begin upload of the video.")
            log(e)
            browser.quit()
            return False

        # monitoring the upload progress
        try:
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "sui-progress-bar__progress-indicator")))
            progress = browser.find_element_by_class_name("sui-progress-bar__progress-indicator")
            percent = progress.get_attribute('style').split(':')
            while len(percent) == 1:
                try:
                    percent = progress.get_attribute('style').split(':')[1]
                except:
                    pass
            while "100%" not in percent:
                # this line makes sure we only log percentages when there is an update to the progress.
                if percent != progress.get_attribute('style').split(':')[1]:
                    log(f"Upload is {percent} complete.")
                    try:
                        percent = progress.get_attribute('style').split(':')[1]
                    except AttributeError:
                        percent = "100%"
            log(f"Upload is complete.")
        except Exception as e:
            log("Something went wrong whilst monitoring the progress of this upload! Leaving browser open so that the upload may complete.")
            log(e)
            return False

        # press the publish button
        try:
            browser.find_element_by_xpath("//div/span/button").click()
        except Exception as e:
            log("Something went wrong! Unable to press the publish button.")
            log(e)
            browser.quit()
            return False

        # Verify the video has been published
        try: 
            WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "d-media-publish-manager__state")))
            state = browser.find_element_by_class_name("d-media-publish-manager__state").text.strip()
            publishdate = browser.find_element_by_class_name("d-media-publish-manager__date").text.strip()
            log(f"The video has been {state} on {publishdate}!")
        except Exception as e:
            log("Something went wrong! Unable to verify that the video has been successfully published.")
            log(e)
            browser.quit()
            return None

        browser.quit()
        return True
        
        