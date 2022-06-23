from xml.dom.minidom import Element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import init_config
import time
import random
import pandas as pd

from datetime import datetime

class RSC_Checker():
    def __init__(self, driver):
        self.config = init_config()
        self.driver = driver
        self.login()
        self.get_status()
    
    def login(self):
        url = self.config.get("RSC", "url")
        username = self.config.get("RSC", "username")
        password = self.config.get("RSC", "password")

        self.driver.get(url)
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.element_to_be_clickable((By.ID, "logInButton")))

        # 1: Username
        self.driver.find_element(By.ID, 'USERID').send_keys(username)
        time.sleep(random.uniform(2, 5))
        # 2: Password
        self.driver.find_element(By.ID, 'PASSWORD').send_keys(password)
        time.sleep(random.uniform(2, 5))
        # 3: Login
        self.driver.find_element(by=By.ID, value='logInButton').click()
        time.sleep(random.uniform(2, 5))

    def get_status(self):
        wait = WebDriverWait(self.driver, 10)
        author_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, 'AUTHOR_VIEW_MANUSCRIPTS')]")))
        time.sleep(random.uniform(2, 5))
        author_button.click()
        time.sleep(random.uniform(2, 5))


        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.ID, "authorDashboardQueue")
            )
        )
        
        element = self.driver.find_element(By.ID, "authorDashboardQueue")

        table_headers = [item.text for item in element.find_elements(By.TAG_NAME, "th")]
        print(table_headers)
        print()

        mc_status = [item.text.split("\n")[0] for item in element.find_elements(By.XPATH, "//td[@data-label='status']")]
        mc_id = [item.text for item in element.find_elements(By.XPATH, "//td[@data-label='ID']")]
        mc_title = [item.text.split("\n")[0] for item in element.find_elements(By.XPATH, "//td[@data-label='title']")]
        mc_submitted = [datetime.strftime(datetime.strptime(item.text,'%d-%b-%Y'), '%Y-%m-%d') for item in element.find_elements(By.XPATH, "//td[@data-label='submitted']")]
        print(mc_status)
        print()
        print(mc_id)
        print()
        print(mc_title)
        print()
        print(mc_submitted)
        print()

        # today = datetime.strftime(datetime.today(),'%Y-%m-%d')