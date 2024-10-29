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

# Create a Faker instance with 'ar_EG' locale for Qatar-specific data
fake = Faker('ar_EG')

class HaiderPropertiesLogin:
    def __init__(self):
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome()
        self.equipment_department_map = {
            "TV": "Electrical Department",
            "AC": "Electrical Department",
            "Sofa": "Carpentry",
            "Dining Table": "Carpentry",
            "Washing Machine": "Electrical Department",
            "Dishwasher": "Electrical Department",
            "Portable AC": "Electrical Department",
            "Refrigerator": "Electrical Department",
            "Microwave": "Electrical Department",
            "Stove": "Electrical Department",
            "Wall Painting": "Carpentry"
        }
        
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
        
    def navigate_to_add_asset(self):
        
        facilty_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Facility Management']")
        facilty_management.click()
        time.sleep(10)
        
        asset_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Asset Management']")
        asset_management.click()
        time.sleep(10)
        
        asset = self.driver.find_element(By.XPATH, "//a[normalize-space()='Asset']")
        asset.click()
        time.sleep(5)
        
        add_asset_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn-outline-primary btn-icon-text']")
        add_asset_button.click()
        time.sleep(10)
    
    def add_asset(self):
         # Click on the landlord dropdown and select a random option
            equipment_dropdown = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[1]/div[1]/span")
            equipment_dropdown.click()
            time.sleep(2)
            equipment_dropdown_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")  # Adjust XPath for the dropdown options
            # random.choice(equipment_dropdown_option).click()
            # if len(equipment_dropdown_option) > 1:
            #     random.choice(equipment_dropdown_option[1:]).click()  # Exclude the first option
            equipment_options = list(self.equipment_department_map.keys())
            filtered_options = [option for option in equipment_dropdown_option if option.text in equipment_options]
                
            time.sleep(3)
            item_type = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[1]/div[2]/span/span[1]/span")
            item_type.click()
            time.sleep(5)
            search_box = self.driver.find_element(By.XPATH, "//input[@class='select2-search__field']")
            search_box.send_keys("Parent")
            search_box.send_keys(Keys.RETURN)
            time.sleep(2)
            
            code = self.driver.find_element(By.XPATH, "//*[@id='txtCode']")
            code.send_keys(self.generate_code())
            time.sleep(1)
            
            serial_no = self.driver.find_element(By.XPATH, "//*[@id='txtSerialNo']")
            serial_no.send_keys(self.generate_fake_serial_no())
            time.sleep(1)
            
            model_no = self.driver.find_element(By.XPATH, "//*[@id='txtPartNumber']")
            model_no.send_keys(self.generate_fake_serial_no())
            time.sleep(1)
            
            asset_price = self.driver.find_element(By.XPATH, "//*[@id='txtPrice']")
            asset_price.send_keys(self.generate_fake_price())
            time.sleep(1)
            
            department_type = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[2]/div[3]/span")
            department_type.click()
            time.sleep(5)
            department_dropdown_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")  # Adjust XPath for the dropdown options
            # random.choice(equipment_dropdown_option).click()
            if len(department_dropdown_option) > 1:
                random.choice(department_dropdown_option[1:]).click()  # Exclude the first option
            
            
            
    def generate_code(self):
        return random.randint(1, 100)
    
    def generate_fake_serial_no(self):
        """Generate a fake Tenant ID (9 digits)."""
        serial_no = random.randint(100000000, 999999999)  # Generates a random 9-digit number
        return str(serial_no)
            
    def generate_fake_price(self):
        """Generate a fake price for assets like AC or fridge in Qatari Riyals."""
        # Define a reasonable price range for ACs and fridges
        min_price = 1000  # Minimum price in QAR
        max_price = 10000  # Maximum price in QAR
        
        price = random.uniform(min_price, max_price)  # Generate a random float in the specified range
        return f"{price:.2f} QAR"  # Format the price to 2 decimal places and append the currency
        
        
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
    login.navigate_to_add_asset()
    # time.sleep(10)
    login.add_asset()
    

    # Close the browser
    login.close_browser()