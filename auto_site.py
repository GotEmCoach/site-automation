import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os
import cryptography
from cryptography.fernet import Fernet
from utils.encrypt_creds import generate_key
import getpass

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
BASE_PATH = Path(os.path.abspath(__file__)).parents[0]
CRED_PATH = Path(f"{BASE_PATH}/credentials/credentials.json.enc")


class AutoSite:
    def __init__(self, url=None, name=None, browser="chrome"):
        self.url = url
        self.name = name
        self.browser = browser
        self._load_credentials()
        self._initiate_session()
        

    def _initiate_session(self):
        if self.browser == "chrome":
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            self.driver.implicitly_wait(1.5)

    def _load_credentials(self):
        cred_pass = getpass.getpass("Enter the password for the encrypted file: ")
        cred_key = generate_key(cred_pass, load_existing_salt=True, save_salt=False)
        f = Fernet(cred_key)
        with open(CRED_PATH, "rb") as enc_file:
            enc_data = enc_file.read()
        try:
            decrypted_data = f.decrypt(enc_data)
        except cryptography.fernet.InvalidToken:
            print("Invalid token, most likely password is wrong.")
            return
        self.cred_dict = json.loads(decrypted_data)
        print(self.cred_dict)    
