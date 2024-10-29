from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pyautogui
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # For adding months easily
import time
import requests
from faker import Faker
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os
import random
import string


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
        
    def navigate_to_add_tenant(self):
        
        leasing_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Leasing Management']")
        leasing_management.click()
        time.sleep(10)
        
        tenant_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Tenant Management']")
        tenant_management.click()
        time.sleep(10)
        
        add_tenant_button = self.driver.find_element(By.XPATH, "//a[normalize-space()='Add Tenant']")
        add_tenant_button.click()
        time.sleep(5)
        
    def add_tenant(self):
        
        # Select a random option for 'Type'
        self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[2]/div[1]/div/form/div[1]/div[1]/div")
        time.sleep(3)
        
        type_options = [
            "/html/body/div/div/div/div/div/div[2]/div[1]/div/form/div[1]/div[1]/div/label[1]/input",
            "/html/body/div/div/div/div/div/div[2]/div[1]/div/form/div[1]/div[1]/div/label[2]/input",
            "/html/body/div/div/div/div/div/div[2]/div[1]/div/form/div[1]/div[1]/div/label[3]/input"
        ]

        # Randomly select one 'Type' option
        selected_type = random.choice(type_options)
        type_radio_button = self.driver.find_element(By.XPATH, selected_type)
        # type_radio_button.click()
        self.driver.execute_script("arguments[0].click();", type_radio_button)
        time.sleep(2)

        # Select a random option for 'User Type'
        user_type_options = [
            "//label[normalize-space()='Broker']",
            "//label[normalize-space()='Walkin']",
            "//label[normalize-space()='Agent']"
        ]

        # Randomly select one 'User Type' option
        selected_user_type = random.choice(user_type_options)
        user_type_radio_button = self.driver.find_element(By.XPATH, selected_user_type)
        user_type_radio_button.click()
        time.sleep(3)
        
        # Check if 'Walkin' is selected and skip broker type if so
        if "Walkin" in selected_user_type:
            print("Selected 'Walkin' user type. Skipping broker type selection.")
        else:
            time.sleep(5)
            user = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlBrokerType-container']")
            user.click()
            time.sleep(3)
            user_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlBrokerType-results']/li")
            # Check if there are options to select from
            if len(user_options) > 1:
                # Skip the first option and select a random option from the remaining
                random.choice(user_options[1:]).click()  # Randomly select from options after the 
        
        time.sleep(3)
        self.driver.execute_script("window.scrollBy(0, 100);")
        
        
        tenant_name = self.driver.find_element(By.XPATH, "//input[@name='TName']")
        tenant_name.send_keys(fake.name())
        time.sleep(1)
        
        tenant_email = self.driver.find_element(By.XPATH, "//input[@id='txtEmail']")
        tenant_email.send_keys(fake.email())
        time.sleep(1)
        
        tenant_mobile = self.driver.find_element(By.XPATH, "//input[@id='txtMobileNo']")
        tenant_mobile.send_keys(self.generate_qatari_phone_number())
        time.sleep(1)
        
        
        tenant_id = self.driver.find_element(By.XPATH, "//input[@id='TenantID']")
        tenant_id.send_keys(self.generate_fake_tenant_id())
        time.sleep(1)
        
        
        tenant_agreement_id = self.driver.find_element(By.XPATH, "//input[@id='TenantAgremID']")
        tenant_agreement_id.send_keys(self.generate_fake_tenant_agreement_id())
        time.sleep(2)
        
        
        venture = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlVentureFrTnt-container']")
        venture.click()
        time.sleep(3)
        venture_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlVentureFrTnt-results']/li")
        if len(venture_options) > 1:
                random.choice(venture_options[1:]).click()  # Avoid first option
        time.sleep(10)
        
        property_type_dropdown = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ddlSublPropertyType"))
        )
        
        # Use the Select class to interact with the dropdown
        select = Select(property_type_dropdown)
        
        # Get all available options from the dropdown
        property_options = select.options
        
        # Check if there are options available
        if len(property_options) == 0:
            print("No property types available. Skipping selection for property type and property unit.")
            return  # Skip property type and unit selection

        # Skip the first option if it's a placeholder
        if len(property_options) > 1:
            random_choice = random.choice(property_options[1:])  # Skip the first option (usually a placeholder)
        else:
            random_choice = property_options[0]  # If there's only one valid option
        
        # Select the randomly chosen option
        select.select_by_visible_text(random_choice.text)
        print(f"Selected property type: {random_choice.text}")
        time.sleep(10)

        # Wait for the property unit dropdown to be visible
        property_unit_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID,"ddslPlot"))
        )
        
        select = Select(property_unit_dropdown)

        
        property_unit_options = select.options
        
        # Check if unit options are available
        if len(property_unit_options) == 0:
            print("No property units available. Skipping selection.")
            return  # Skip property unit selection
        
        if len(property_unit_options) > 1:
            random_choice_unit = random.choice(property_unit_options[1:])  # Skip the first option (usually a placeholder)
        else:
            random_choice_unit = property_unit_options[0]  # If there's only one valid option
        
        # Select the randomly chosen option
        select.select_by_visible_text(random_choice_unit.text)
        print(f"Selected Unit type: {random_choice_unit.text}")
            

        time.sleep(5)
      
        
        parking_slot = self.driver.find_element(By.XPATH, "//input[@ng-model='ParkingSlot']")
        parking_slot.send_keys(self.generate_parking_slot())
        time.sleep(1)
        car_plate_no = self.driver.find_element(By.XPATH, "//input[@ng-model='txtPlateno']")
        car_plate_no.send_keys(self.generate_parking_slot())
        time.sleep(1)
        
        fax = self.driver.find_element(By.XPATH, "//input[@name='Faxno']")
        fax.send_keys(self.generate_parking_slot())
        time.sleep(1)
        
        # Using the functions in your Selenium script
        contract_start = self.driver.find_element(By.XPATH, "//div[@class='col-sm-4 mb-3']//input[@id='txtSecRecDate']")
        future_date = self.generate_future_date()
        contract_start.send_keys(future_date)  # Sends the future start date
        time.sleep(1)
        
        contract_end = self.driver.find_element(By.XPATH, "//input[@name='ContractEndDate']")
        contract_end_date = self.generate_contract_end_date(future_date)  # Pass the future date to generate the end date
        contract_end.send_keys(contract_end_date)  # Sends the contract end date (12 months later)
        time.sleep(1)
        
        due_date = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlDueDay-container']")
        due_date.click()
        time.sleep(3)
        agent_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlDueDay-results']/li")
        if len(agent_options) > 1:
                random.choice(agent_options[1:]).click()  # Avoid first option
        time.sleep(3)
                    
               
        
    def generate_qatari_phone_number(self):
        """Generate a random Qatari phone number (e.g., starting with +974)."""
        return f"{fake.random_int(min=5000_0000, max=5999_9999)}"
    
    def generate_fake_tenant_id(self):
        """Generate a fake Tenant ID (9 digits)."""
        tenant_id = random.randint(100000000, 999999999)  # Generates a random 9-digit number
        return str(tenant_id)

    def generate_fake_tenant_agreement_id(self):
        """Generate a fake Tenant Agreement ID (6 digits)."""
        agreement_id = random.randint(100000, 999999)  # Generates a random 6-digit number
        return str(agreement_id)    
    
    def generate_parking_slot(self):
        """Generate a fake Tenant Agreement ID (6 digits)."""
        parking_slot_no = random.randint(1, 9)  # Generates a random 6-digit number
        return str(parking_slot_no) 
    
    def generate_car_number_plate(self):
        """Generate a fake car number plate."""
        # Two uppercase letters followed by two digits, followed by three more uppercase letters
        letters_part1 = ''.join(random.choices(string.ascii_uppercase, k=2))  # Two random uppercase letters
        digits = ''.join(random.choices(string.digits, k=2))  # Two random digits
        letters_part2 = ''.join(random.choices(string.ascii_uppercase, k=3))  # Three random uppercase letters
        
        number_plate = f"{letters_part1}{digits}{letters_part2}"
        return number_plate
    
    def generate_fax_no(self):
        """Generate a fake Tenant Agreement ID (6 digits)."""
        fax_no = random.randint(1, 100)  # Generates a random 6-digit number
        return str(fax_no)
    
    # Function to generate a future date (e.g., from today up to 30 days in the future)
    def generate_future_date(self):
        today = datetime.today()
        future_date = today + timedelta(days=random.randint(1, 30))  # Generates a date between 1 and 30 days from today
        return future_date.strftime("%d-%m-%Y")
    
    def generate_contract_end_date(self, future_date):
    # Convert the future date string back to a datetime object
        future_date_obj = datetime.strptime(future_date, "%d-%m-%Y")
        contract_end_date = future_date_obj + relativedelta(months=12)  # Adds 12 months to the future date
        return contract_end_date.strftime("%d-%m-%Y") 
        
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
    login.navigate_to_add_tenant()
    # time.sleep(10)
    login.add_tenant()
    

    # Close the browser
    login.close_browser()