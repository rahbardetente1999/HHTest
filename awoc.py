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
        
        
        corrective = self.driver.find_element(By.XPATH, "//a[normalize-space()='Corrective']")
        corrective.click()
        self.log_action("Clicked on Corrective")
        time.sleep(5)
        
        add_work_order_button = self.driver.find_element(By.XPATH, "//a[@class='btn btn-outline-info btn-icon-text d-md-block']")
        add_work_order_button.click()
        time.sleep(10)
        self.log_action("Clicked on Add Asset button")
        
        
        
    def generate_random_issue(self):
        """Generate a random title and description for the work order."""
        issues = {
            "AC Issue": "The air conditioning unit is not cooling properly.",
            "Water Logging": "There is significant water accumulation in the backyard.",
            "Geyser problem": "The geyser is not heating water efficiently.",
            "Electrical switch problem": "The light switch in the living room is not functioning.",
            "Tile is broken": "One of the tiles in the kitchen has cracked.",
            "Water Problem": "There is a persistent leak under the kitchen sink.",
            "Leak from ceiling bedroom 1": "Water is dripping from the ceiling in bedroom 1.",
            "Heating issue": "The heating system is not providing adequate warmth.",
            "Plumbing issue": "There is a clog in the bathroom sink.",
            "Roof leak": "Rainwater is entering through a leak in the roof.",
            "Broken window": "The window in the guest room is shattered.",
            "Flickering lights": "The lights in the hallway flicker intermittently.",
            "Pest control required": "There is an infestation of pests in the kitchen.",
            "Door handle broken": "The door handle to the garage is broken.",
            "Mold issue": "Mold is growing on the bathroom walls.",
            "Wall paint peeling": "The paint on the living room wall is peeling off."
        }
        title = random.choice(list(issues.keys()))
        return title, issues[title]
    
    def add_work_order(self):
        """Add a work order with a random title and description."""
        title, description = self.generate_random_issue()
        
        title_input = self.driver.find_element(By.XPATH, "//input[@id='txtTitle']")
        title_input.clear()
        title_input.send_keys(title)
        self.log_action(f"Entered title: {title}")
        time.sleep(3)
        
        # Select a random option for 'User Type'
        user_type_options = [
            "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/div/label[2]"
        ]

        # Randomly select one 'User Type' option
        selected_user_type = random.choice(user_type_options)
        user_type_radio_button = self.driver.find_element(By.XPATH, selected_user_type)
        user_type_radio_button.click()
        time.sleep(3)
              

        description_input = self.driver.find_element(By.XPATH, "//input[@id='txtIncidentDescription']")
        description_input.clear()
        description_input.send_keys(description)
        self.log_action(f"Entered description: {description}")
        time.sleep(3)
        
        # Locate and click the radio button
        tenant_button = self.driver.find_element(By.XPATH, "//div[@class='btn-group w-100 w-lg-60']//label[2]")
        tenant_button.click()
        time.sleep(5)
        
        tenant_selection = self.driver.find_element(By.XPATH, "//span[@id='select2--container']")
        tenant_selection.click()
        time.sleep(3)
        
        tenant_selection_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(tenant_selection_option) > 1:
                selected_option = random.choice(tenant_selection_option[1:])
                tenant_selection = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {tenant_selection}")  # Exclude the first option
        time.sleep(3)
        
        department_selection = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[3]/div[2]/span/span[1]/span")
        department_selection.click()
        time.sleep(3)
        
        department_selection_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(department_selection_option) > 1:
                selected_option = random.choice(department_selection_option[1:])
                department_selection = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {department_selection}")  # Exclude the first option
        time.sleep(5)
        
        # Locate and click the label with 'for' attribute 'Staff'
        staff_label = self.driver.find_element(By.XPATH, "//label[@for='Staff']")
        # staff_label.click()
        self.driver.execute_script("arguments[0].click();", staff_label)
        time.sleep(5)
        
        staff__selection = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[3]/div[4]/span")
        staff__selection.click()
        time.sleep(3)
        
        staff__selection_option = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(staff__selection_option) > 2:
                selected_option = random.choice(staff__selection_option[2:])
                staff__selection = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {staff__selection}")  # Exclude the first option
        time.sleep(5)
        self.driver.execute_script("window.scrollBy(0, 200);")
        
        # Calculate a future date (e.g., 7 days from today) and format it
        future_date = (datetime.now() + timedelta(days=7)).strftime('%Y/%m/%d')

        # Locate the date input field and enter the formatted future date
        date_input = self.driver.find_element(By.XPATH, "//input[@id='FacilityDate']")
        date_input.clear()  # Clear any pre-filled data if necessary
        date_input.send_keys(future_date)
        date_input.send_keys("\n")  # Simulate pressing Enter
        time.sleep(5)
        self.driver.execute_script("window.scrollBy(0, 100);")
        
        # Generate a random amount between 100 and 500
        random_amount = random.randint(100, 500)

        # Locate the amount input field and enter the random amount
        amount_input = self.driver.find_element(By.XPATH, "//input[@name='amount']")
        amount_input.clear()
        amount_input.send_keys(str(random_amount))

        print(f"Entered Amount: {random_amount}")
        time.sleep(5)
        
        # Select a random option for 'Priority'
        priority_level = [
            "//label[normalize-space()='High']"
        ]

        # Randomly select one 'User Type' option
        priority_level_option = random.choice(priority_level)
        priority_level_option_radio_button = self.driver.find_element(By.XPATH, priority_level_option)
        priority_level_option_radio_button.click()
        time.sleep(3)
        
        # save_button = self.driver.find_element(By.XPATH, "//*[@id='btnSaveIncident']")
        # self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        # time.sleep(1)  # Allow time for scrolling
        # self.driver.execute_script("arguments[0].click();", save_button)
        # time.sleep(3)
        # print(f"save button clicked")
        # self.log_action("Saved the asset")
        # Locate the "Save" button using its ID and click it
        save_button = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnSaveIncident"))
        )
        save_button.click()

        
        
        
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
    login.add_work_order()

    # Close the browser
    login.close_browser()