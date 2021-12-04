#!/usr/bin/env python3
import os
import subprocess
import time
import re
import requests
import urllib.request
import zipfile
import io
from google.cloud import speech_v1
from sys import platform
from random import randint, uniform
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Install all requirements before executing script
# pip install -r requirements.txt

# Create Google Cloud Speech-to-Text API service account and API key file
# The API key file must be in the same directory as this script and must be named s2t-api.json


class Gcaptcha:
    class transcription:
        def __init__(self):
            self.attempts = 0
            self.successful = 0
            self.failed = 0

    class recaptcha:
        def __init__(self):
            self.solved = 0

    def __init__(self, url):
        self.response = None

        self.transcription.attempts = 0
        self.transcription.successful = 0
        self.transcription.failed = 0
        self.recaptcha.solved = 0

        # Set Chrome to run in headless mode and mute the audio
        opts = webdriver.ChromeOptions()
        opts.headless = True
        opts.add_argument("--mute-audio")

        # Try to use the current chromedriver, if outdated or missing, download
        # and patch the version that corresponds with the installed Google Chrome version
        try:
            self.driver = webdriver.Chrome('./chromedriver', options=opts, service_log_path=os.path.devnull)
        except:
            get_chromedriver()
            self.driver = webdriver.Chrome('./chromedriver', options=opts, service_log_path=os.path.devnull)

        self.driver.maximize_window()
        self.driver.get(url)
        self.__bypass_webdriver_check()

        # Initialize gcaptcha solver
        self.__initialize()

        while True:
            # Download MP3 file
            mp3_file = self.__download_mp3()

            # Transcribe MP3 file
            audio_transcription = transcribe(mp3_file)
            self.transcription.attempts += 1

            # If the MP3 file is properly transcribed
            if type(audio_transcription) is str:
                self.transcription.successful += 1

                # Verify transcription
                verify = self.__submit_transcription(audio_transcription)

                # Transcription successful with confidence >60%
                if verify:
                    gcaptcha_response = self.__get_response()
                    self.response = gcaptcha_response
                    self.recaptcha.solved += 1

                    # Delete MP3 file
                    os.remove(mp3_file)
                    self.driver.close()
                    self.driver.quit()
                    break
                # Multiple correct solutions required. Solving again.
                else:
                    self.recaptcha.solved += 1

                    # Delete MP3 file
                    os.remove(mp3_file)
                    time.sleep(uniform(2, 4))
            # If the MP3 file could not be transcribed
            else:
                self.transcription.failed += 1

                # Delete MP3 file
                os.remove(mp3_file)

                # Click on the "Get a new challenge" button to use a new MP3 file
                self.__refresh_mp3()
                time.sleep(uniform(2, 4))

    def __initialize(self):
        # Access initial gcaptcha iframe
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[name^=a]'))
        self.__bypass_webdriver_check()

        # Click the gcaptcha checkbox
        checkbox = self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-anchor')
        self.__mouse_click(checkbox)

        # Go back to original content to access second gcaptcha iframe
        self.driver.switch_to.default_content()

        # Wait roughly 3 seconds for second gcaptcha iframe to load
        time.sleep(uniform(2.5, 3))

        # Find second gcaptcha iframe
        gcaptcha = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name^=c]'))
        )

        # Access second gcaptcha iframe
        self.driver.switch_to.frame(gcaptcha)
        self.__bypass_webdriver_check()

        # Click the audio button
        audio_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.rc-button-audio'))
        )
        self.__mouse_click(audio_button)
        time.sleep(0.5)

    def __mouse_click(self, element):
        cursor = ActionChains(self.driver)
        cursor.move_to_element(element)
        cursor.pause(uniform(0.3, 0.5))
        cursor.click()
        cursor.perform()

    def __bypass_webdriver_check(self):
        self.driver.execute_script('const newProto = navigator.__proto__; delete newProto.webdriver; navigator.__proto__ = newProto;')

    def __download_mp3(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[name^=c]'))
        self.__bypass_webdriver_check()

        # Check if the Google servers are blocking us
        if len(self.driver.find_elements(By.CSS_SELECTOR, '.rc-doscaptcha-body-text')) == 0:
            audio_file = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#audio-source'))
            )

            # Click the play button
            play_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.rc-audiochallenge-play-button > button'))
            )
            self.__mouse_click(play_button)

            # Get URL of MP3 file
            audio_url = audio_file.get_attribute('src')

            # Predefine the MP3 file name
            mp3 = 'audio{}.mp3'.format(randint(0, 100))

            # Download the MP3 file
            urllib.request.urlretrieve(audio_url, mp3)

            return mp3
        else:
            Error('Too many requests have been sent to Google. You are currently being blocked by their servers.')
            exit(-1)

    def __refresh_mp3(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[name^=c]'))
        self.__bypass_webdriver_check()

        # Click on the refresh button to retrieve a new mp3 file
        refresh_button = self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-reload-button')
        self.__mouse_click(refresh_button)

    def __submit_transcription(self, text):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[name^=c]'))
        self.__bypass_webdriver_check()

        # Input field for response
        input_field = self.driver.find_element(By.CSS_SELECTOR, '#audio-response')

        # Input response from transcription character by character with random delay between keystrokes
        # for char in text:
        #     time.sleep(uniform(0.1, 0.2))
        #     input_field.send_keys(char)

        # Instantly type the full text without delays because Google isn't checking delays between keystrokes
        input_field.send_keys(text)

        # Click "Verify" button
        verify_button = self.driver.find_element(By.CSS_SELECTOR, '#recaptcha-verify-button')
        self.__mouse_click(verify_button)

        # Wait roughly 3 seconds for verification to complete
        time.sleep(uniform(2, 3))

        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[name^=a]'))
        self.__bypass_webdriver_check()

        # Check to see if verified by recaptcha
        try:
            self.driver.find_element(By.CSS_SELECTOR, '.recaptcha-checkbox-checked')
        except NoSuchElementException:
            return False
        else:
            return True

    def __get_response(self):
        # Switch back to main parent window and get gcaptcha response
        self.driver.switch_to.default_content()
        response = self.driver.find_element(By.CSS_SELECTOR, '#g-recaptcha-response').get_attribute('value')
        return response


class Error(Exception):
    def __init__(self, message):
        get_files = os.listdir()
        match_regex = re.compile(r'^audio\d+.mp3|chromedriver_\w+\d+.zip$')
        filtered_files = [f for f in get_files if match_regex.match(f)]

        for file in filtered_files:
            os.remove(file)

        raise Exception(f'ERROR: {message}')


def transcribe(mp3):
    # You must create a Google Cloud Speech-to-Text API service account and create a key called 's2t-api.json'
    client = speech_v1.SpeechClient.from_service_account_json('./s2t-api.json')
    config = {'language_code': 'en-US'}

    with io.open(mp3, 'rb') as f:
        content = f.read()

    audio = {'content': content}
    response = client.recognize(config, audio)

    try:
        transcript = response.results[0].alternatives[0].transcript
        confidence = response.results[0].alternatives[0].confidence
    except IndexError:
        return 1
    else:
        return transcript if confidence >= 0.60 else 2


def get_os():
    if platform == 'win32':
        return 'Windows'
    elif platform == 'darwin':
        return 'Mac'
    elif platform == 'linux' or platform == 'linux2':
        return 'Linux'
    else:
        return None


def chrome_version(os_name):
    version = None

    # Depending on the OS, use different ways to figure out what version of Chrome is installed
    if os_name == 'Windows':
        chrome_path_files = os.listdir('C:\\Program Files (x86)\\Google\\Chrome\\Application\\')
        version = [name for name in chrome_path_files if re.match(r'\d+.\d+.\d+.\d+', name)][0]
    elif os_name == 'Mac':
        output = str(subprocess.check_output('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --version',
                                             shell=True))
        version = re.search(r'(\d+.\d+.\d+.\d+)', output)[1]
    elif os_name == 'Linux':
        output = str(subprocess.check_output('google-chrome --version', shell=True))
        version = re.search(r'(\d+.\d+.\d+.\d+)', output)[1]

    return version


def driver_url(version, os_name):
    if os_name == 'Windows':
        os_id = 'win32'
    elif os_name == 'Mac':
        os_id = 'mac64'
    elif os_name == 'Linux':
        os_id = 'linux64'
    else:
        Error('Could not detect the OS when trying to get the URL for chromedriver.')

    chrome_version_regex = re.search('(\d+.\d+.\d+).\d+', version)
    chrome_version = chrome_version_regex.group(1)

    chromedriver_version_page = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_' + chrome_version)
    chromedriver_version = chromedriver_version_page.content.decode("utf-8")

    return f'https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_{os_id}.zip'


def get_chromedriver():
    os_name = get_os()
    version = chrome_version(os_name)
    file_url = driver_url(version, os_name)

    # Download the chromedriver.zip file
    open('chromedriver.zip', 'wb').write(requests.get(file_url).content)

    # Extract chromedriver
    zipfile.ZipFile('chromedriver.zip', 'r').extractall()

    os.remove('chromedriver.zip')

    # Set the name of the chromedriver file
    driver_name = 'chromedriver'

    # Add .exe extension if script is being executed on Windows
    if os_name == 'Windows':
        driver_name += '.exe'
    # Give execute(x) permissions to chromedriver if the script is executed on Mac or Linux
    elif os_name == 'Mac' or os_name == 'Linux':
        subprocess.check_output(f'chmod +x {driver_name}', shell=True)

    # The remainder of the function patches chromedriver which will
    # bypass any checks to see if the browser is being automated
    content = open(driver_name, 'rb').read()

    key_string = re.search(bytes(r"var key = '.*?'", 'Latin-1'), content)[0]
    dummy_fill = ''.join(['0' for i in range(len(key_string) - 12)])
    new_key_string = re.sub(bytes(r"'.*?'", 'Latin-1'), bytes(f"'{dummy_fill}'", 'Latin-1'), key_string)
    new_content = content.replace(key_string, new_key_string)

    open(driver_name, 'wb').write(new_content)
