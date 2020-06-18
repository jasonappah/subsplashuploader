# The plan:
    # 0) have a dictionary where keys are Month + Year and the value is the Sermon series (you could use S1 to manage this! or we could try goJSON) --DONE
    # 1) post to dashboard.thechurchapp.org w/ email + password to login - done
    # 2) get https://dashboard.thechurchapp.org/18953/#/library/media - done 
    # 3) click on the button element with id ember398 (this is the create media item button) - done
    # 4) enter today's date into the input with id ember405 (this is the title) - done
    # 5) click on the option inside the select element inside div id ember301 that matches the sermon series that the video was made in (using dictionary from 0) - done
    # 6) click on button id ember412 to create item - done
    # 7) on the page that loads, upload the video to the input with id="ember677_fileUploader" - done
    # 8) wait until the div inside div id ember709 has style="width:100%" (this means the video has been fully uploaded)
    # 9) i forgot to get the id for the publish button, but y'know, click that

import time, os
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
LOGGING=True

def getTime():
    return (datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ": ")

def log(msg):
    if LOGGING:
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
    
    def upload(self, video="", name=datetime.now().strftime("%B %d, %Y")):
        video = os.path.abspath(video)
        log(f"Beginning to upload video to Subsplash with title {name}: {video}")

        videocreationdate = datetime.fromtimestamp(int(os.path.getmtime(video)))

        # my = datetime.now().strftime("%m %Y")
        videomonthyear = videocreationdate.strftime("%B %Y")
        series = ""

        opts = Options()
        browser = Chrome(options=opts)
        browser.get('https://dashboard.thechurchapp.org')
        log("Started browser.")

        # Logging in
        browser.find_element_by_id('Email').send_keys(self.user)
        browser.find_element_by_id('Password').send_keys(self.passwd)
        browser.find_element_by_id('js-login-form-submit').click()
        log("Logged in.")

        # Navigating to on-demand page
        # WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ember56 > svg")))
        # browser.find_element_by_css_selector("#ember56 > svg").click()
        
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ember-action-53='53']")))
        browser.find_element_by_xpath("//button[@data-ember-action-53='53']").click()

    
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "ember60")))
        browser.find_element_by_id("ember60").click()
        log("Opened the on-demand page.")

        # Clicking the create media item button
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ga-event-action='create media item']")))
        browser.find_element_by_xpath("//button[@data-ga-event-action='create media item']").click()
        log("Clicked the create media item button.")

        # Typing in the Media title
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//label/input[@type='text']")))
        browser.find_element_by_xpath("//label/input[@type='text']").send_keys(name)
        log("Typed in the media title.")
        
        # Selecting the sermon series
        if videomonthyear in self.series.keys():
            series = self.series[videomonthyear]

        for i in browser.find_elements_by_class_name("kit-select__option"):
            if i.text.strip() == series:
                i.click()
                log(f"Clicked series {i.text.strip()}")
                break
            else: 
                print(i.text.strip())

        if series == "":
            log("Couldn't get a series from the video provided. Maybe the timestamp is wrong.")

        # Clicking the submit button
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ga-event-action='create']")))
        browser.find_element_by_xpath("//button[@data-ga-event-action='create']").click()
        log("Clicked the create button.")

        # formulating the date to input
        WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='MM/DD/YYYY']")))
        browser.find_element_by_xpath("//input[@placeholder='MM/DD/YYYY']").send_keys(videocreationdate.strftime("%m/%d/%Y"))
        log("Inputted video date.")

        # uploading the video
        #browser.find_element_by_id("ember746_fileUploader").send_keys(video)
        browser.find_element_by_xpath("//label[@class='sui-media-uploader__content']/div/input[@type='file']").send_keys(video)
        log("Beginning to upload video.")

        time.sleep(60)
        # browser.close()


