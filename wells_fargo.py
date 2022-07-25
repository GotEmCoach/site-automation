from auto_site import AutoSite
from selenium.webdriver.common.by import By

WELLS_URL = "https://connect.secure.wellsfargo.com/auth/login/present?origin=cob&LOB=CONS"

class WellsFargoSite(AutoSite):
    def __init__(self):
        super().__init__(url=WELLS_URL, name="wells_fargo")

    
    def get_login_page(self):
        self.driver.get(self.url)
        self.driver.find_element(By.NAME, "j_username").send_keys()
        
    