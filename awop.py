from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import random
import time
import logging
from faker import Faker

# Create a Faker instance with 'ar_EG' locale for Qatar-specific data
fake = Faker('ar_EG')

class HaiderPropertiesLogin:
    def __init__(self):
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome()
        
    def log_action(self, action):
        """Log each action to a text file."""
        logging.info(action)
        
    def open_website(self, url):
        """Open the login page and maximize the window."""
        self.driver.get(url)
        self.driver.maximize_window()
        self.log_action(f"Opened website: {url}")
        
    def login(self, username_value, password_value):
        """Perform login using provided username and password."""
        username = self.driver.find_element(By.XPATH, "//input[@id='txtUsername']")
        username.send_keys(username_value)
        password = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        password.send_keys(password_value)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        self.log_action("Logged in with username: " + username_value)
        
    def navigate_to_add_asset(self):
        """Navigate to the 'Add Asset' section."""
        facility_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Facility Management']")
        facility_management.click()
        time.sleep(10)
        self.log_action("Clicked on Facility management")
        
        work_order = self.driver.find_element(By.XPATH, "//span[normalize-space()='Work Order']")
        work_order.click()
        time.sleep(10)
        self.log_action("Clicked on Work order")
        
        
        corrective = self.driver.find_element(By.XPATH, "//a[normalize-space()='Preventive']")
        corrective.click()
        self.log_action("Clicked on Corrective")
        time.sleep(5)
        
        add_work_order_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn-outline-primary btn-icon-text']")
        add_work_order_button.click()
        time.sleep(10)
        self.log_action("Clicked on Add Asset button")
        
    def generate_random_preventive_work_order(self):
        """Generate a random title for a preventive work order."""
        preventive_issues = [
            "AC Maintenance",
            "Refrigerator Maintenance",
            "Heater Inspection",
            "Water Heater Check",
            "Electrical Panel Inspection",
            "Smoke Detector Test",
            "Roof Inspection",
            "Plumbing Inspection",
            "Fire Extinguisher Check",
            "Pest Control Inspection",
            "Window Sealing Check",
            "Door Lubrication",
            "Filter Replacement",
            "Gutter Cleaning",
            "Mold Inspection",
            "Vent Cleaning",
            "Paint Touch-Up",
            "Garage Door Maintenance"
        ]
        title = random.choice(preventive_issues)
        return title
        
    def add_work_order_preventive(self):
        
        title = self.generate_random_preventive_work_order()
        
        title_input = self.driver.find_element(By.XPATH, "//*[@id='addpreventmmodal']/div/div/form/div[1]/div/div[1]/input")
        title_input.clear()
        title_input.send_keys(title)
        self.log_action(f"Entered title: {title}")
        time.sleep(3)
        
        type_sales_rent = self.driver.find_element(By.XPATH, "//*[@id='addpreventmmodal']/div/div/form/div[1]/div/div[2]/span")
        type_sales_rent.click()
        time.sleep(3)
        
        type_sales_rent_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(type_sales_rent_option) > 2:
                selected_option = random.choice(type_sales_rent_option[2:])
                type_sales_rent = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {type_sales_rent}")  # Exclude the first option
        time.sleep(5)
        
        venture_name = self.driver.find_element(By.XPATH, "//*[@id='addpreventmmodal']/div/div/form/div[1]/div/div[3]/span/span[1]/span")
        venture_name.click()
        time.sleep(3)
        
        venture_name_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(venture_name_option) > 0:
                selected_option = random.choice(venture_name_option[0:])
                venture_name = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {venture_name}")  # Exclude the first option
        time.sleep(5)
        
        property = self.driver.find_element(By.XPATH, "//*[@id='addpreventmmodal']/div/div/form/div[1]/div/div[4]/span/span[1]/span")
        property.click()
        time.sleep(3)
        
        property_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(property_option) > 1:
                selected_option = random.choice(property_option[1:])
                property = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {property}")  # Exclude the first option
        time.sleep(3)
        save_button = self.driver.find_element(By.XPATH, "//*[@id='btnAddPMsave']")
        save_button.click()
        time.sleep(3)
        self.log_action("Saved the asset")
        
        
        
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

    # Navigate to Add Asset and add an asset
    login.navigate_to_add_asset()
    login.add_work_order_preventive()

    # Close the browser
    login.close_browser()