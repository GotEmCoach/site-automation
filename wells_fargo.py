from auto_site import AutoSite
from selenium.webdriver.common.by import By

WELLS_URL = "https://connect.secure.wellsfargo.com/auth/login/present?origin=cob&LOB=CONS"

class WellsFargoSite(AutoSite):
    def __init__(self):
        super().__init__(url=WELLS_URL, name="wells_fargo")

    
    def get_login_page(self):
        self.driver.get(self.url)
        username = self.cred_dict[self.name][0]
        password = self.cred_dict[self.name][1]
        self.driver.find_element(By.NAME, "j_username").send_keys(username)
        self.driver.find_element(By.NAME, "j_password").send_keys(password)
    