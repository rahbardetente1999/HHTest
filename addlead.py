from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pyautogui
import time
import requests
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from selenium.common.exceptions import NoSuchElementException
import os
import random

# Create a Faker instance with 'ar_QA' locale for Qatar-specific data
fake = Faker('ar_EG')

class HaiderPropertiesLogin:
    def __init__(self):
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome()
        
    def open_website(self, url):
        """Open the login page and maximize the window."""
        self.driver.get(url)
        self.driver.maximize_window()
        
    def login(self, username_value, password_value):
        """Perform login using provided username and password."""
        username = self.driver.find_element(By.XPATH, "//input[@id='txtUsername']")
        username.send_keys(username_value)
        password = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        password.send_keys(password_value)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
    def navigate_to_add_lead(self):
        
        wait = WebDriverWait(self.driver, 10)
        
        leasing_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Leasing Management']")
        leasing_management.click()
        time.sleep(10)
        
        lead_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Lead Management']")
        lead_management.click()
        time.sleep(5)
        
        add_lead = self.driver.find_element(By.XPATH, "//a[normalize-space()='Add Lead']")
        add_lead.click()
        time.sleep(5)
        
        # Fill Name
        name_input = self.driver.find_element(By.XPATH, "//input[@id='txtName']")
        name_input.send_keys(fake.name())

        # Fill Mobile Number
        mobile_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div/input")
        mobile_input.send_keys(self.generate_qatari_phone_number())

        # Fill Alternative Mobile 1
        alt_mob1_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[2]/div[1]/div[1]/input")
        alt_mob1_input.send_keys(self.generate_qatari_phone_number())

        # Fill Alternative Mobile 2
        alt_mob2_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[2]/div[1]/div[2]/input")
        alt_mob2_input.send_keys(self.generate_qatari_phone_number())

        # Fill Email
        email_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[2]/div[2]/div[1]/input")
        email_input.send_keys(fake.email())

        # Fill Email 1
        email1_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[2]/div[2]/div[2]/input")
        email1_input.send_keys(fake.email())

        # Fill Referred By
        referred_by_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[3]/div[2]/input")
        referred_by_input.send_keys(fake.name())

        # Fill Remarks
        remarks_input = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[4]/div[1]/input")
        remarks_input.send_keys(fake.text())
        time.sleep(2)
        
        self.driver.execute_script("window.scrollBy(0, 100);")

        # Handle dropdowns (select random option except the first)
        # For Agents dropdown
        agents_dropdown = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlManagar-container']")
        agents_dropdown.click()
        time.sleep(3)
        agent_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlManagar-container-results']/li")
        if len(agent_options) > 1:
                random.choice(agent_options[1:]).click()  # Avoid first option
        time.sleep(3)
        
        self.driver.execute_script("window.scrollBy(0, 100);")
        

        # For Source of Call dropdown
        source_dropdown = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlSource-container']")
        source_dropdown.click()
        time.sleep(3)
        source_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlSource-container-results']/li")
        if len(source_options) > 1:
                random.choice(source_options[1:]).click()
        time.sleep(3)
        
        
        save_button = self.driver.find_element(By.XPATH, "//button[@id='btnSave']")
        save_button.click()
        time.sleep(3)
        
    def generate_qatari_phone_number(self):
        """Generate a random Qatari phone number (e.g., starting with +974)."""
        return f"{fake.random_int(min=5000_0000, max=5999_9999)}"
        

        
    def close_browser(self):
        """Wait for 20 seconds and close the browser."""
        time.sleep(20)
        self.driver.quit()
        
if __name__ == "__main__":
    # Create an instance of the class
    login = HaiderPropertiesLogin()

    # Open the website and perform login
    login.open_website("https://test.haiderproperties.com/")
    time.sleep(5)
    login.login("superadmin", "Admin$213")  # Replace with actual username and password
    time.sleep(15)

    # Loop to add a landlord three times with different passport file names
    # for i in range(3):
    #     time.sleep(15)
    login.navigate_to_add_lead()
    # time.sleep(10)
    

    # Close the browser
    login.close_browser()