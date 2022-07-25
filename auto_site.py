import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager



class AutoSite:
    def __init__(self, url=None, name=None, browser="chrome"):
        self.url = url
        self.name = name
        self.browser = browser
        self._initiate_session()

    def _initiate_session(self):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            self.driver.implicitly_wait(0.5)



