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


# Configure logging
log_filename = f"test_run_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Create a Faker instance with 'ar_EG' locale for Qatar-specific data
fake = Faker('ar_EG')

class HaiderPropertiesLogin:
    def __init__(self):
        # Initialize the Chrome driver
        self.driver = webdriver.Chrome()
        
        # Define equipment to department mapping
        self.equipment_department_map = {
            "TV": "Electrical Department",
            "AC": "Electrical Department",
            "Sofa": "Carpentry Department",
            "Dining Table": "Carpentry Department",
            "Washing Machine": "Electrical Department",
            "Dishwasher": "Electrical Department",
            "Portable AC": "Electrical Department",
            "Refrigerator": "Electrical Department",
            "Microwave": "Electrical Department",
            "Stove": "Electrical Department",
            "Wall Painting": "Carpentry Department"
        }
        
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
        
        asset_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Asset Management']")
        asset_management.click()
        time.sleep(10)
        self.log_action("Clicked on Asset Management")
        
        
        asset = self.driver.find_element(By.XPATH, "//a[normalize-space()='Asset']")
        asset.click()
        self.log_action("Clicked on Asset")
        time.sleep(5)
        
        add_asset_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn-outline-primary btn-icon-text']")
        add_asset_button.click()
        time.sleep(10)
        self.log_action("Clicked on Add Asset button")
    
    def add_asset(self):
        """Add a new asset with details filled automatically."""
        # Step 1: Select equipment and then proceed with other fields
        selected_equipment = self.select_random_equipment()
        time.sleep(3)
        # Step 2: Select item type
        self.select_item_type()
        time.sleep(3)
        
        # Step 3: Fill in the asset code
        self.fill_asset_code()
        time.sleep(3)
        
        # Step 4: Fill in the serial number
        self.fill_serial_no()
        time.sleep(2)
        
        # Step 5: Fill in the model number
        self.fill_model_no()
        time.sleep(2)
        
        # Step 6: Fill in the asset price
        self.fill_asset_price()
        time.sleep(2)
        
        # Step 7: Select department based on the selected equipment
        if selected_equipment:
            self.select_department(selected_equipment)
        time.sleep(5)
        
        self.select_vendor()
        time.sleep(3)
        self.select_location()
        time.sleep(3)
        # self.manufacturer()
        if selected_equipment:
            self.select_department(selected_equipment)
            manufacturer_name = self.generate_manufacturer_name(self.equipment_department_map[selected_equipment])
            self.manufacturer(manufacturer_name)
            
        time.sleep(3)
        manufacturing_year = self.generate_manufacturing_year()
        time.sleep(3)
        manufacturing_date = self.generate_manufacturing_date(manufacturing_year)
        time.sleep(3)
        self.generate_purchased_and_warranty_dates(manufacturing_date)
        time.sleep(3)
        self.warranty_cover()
        self.driver.execute_script("window.scrollBy(0, 100);")
        self.save()
    
    def select_random_equipment(self):
        equipment_dropdown = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[1]/div[1]/span")
        equipment_dropdown.click()
        time.sleep(2)

        attempts = 3
        for attempt in range(attempts):
            try:
                # Fetch dropdown options and filter by valid options
                equipment_dropdown_options = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
                equipment_options = list(self.equipment_department_map.keys())
                filtered_options = [option for option in equipment_dropdown_options if option.text in equipment_options]
                
                if filtered_options:
                    random_choice = random.choice(filtered_options)
                    selected_equipment = random_choice.text
                    random_choice.click()  # Select the equipment
                    print(f"Selected Equipment: {selected_equipment}")
                    self.log_action(f"Selected Equipment: {selected_equipment}")
                    return selected_equipment
            except StaleElementReferenceException:
                if attempt < attempts - 1:
                    time.sleep(1)  # Retry after a short wait
                else:
                    print("Could not select equipment due to a stale element reference.")
                    return None

    def select_item_type(self):
        """Select the item type for the asset."""
        item_type = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[1]/div[2]/span/span[1]/span")
        item_type.click()
        time.sleep(5)
        
        search_box = self.driver.find_element(By.XPATH, "//input[@class='select2-search__field']")
        search_box.send_keys("Parent")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        self.log_action("Selected Parent")
        
    def fill_asset_code(self):
        """Fill in a randomly generated asset code."""
        code = self.driver.find_element(By.XPATH, "//*[@id='txtCode']")
        code.send_keys(str(random.randint(1, 100)))
        time.sleep(1)
        self.log_action("filled code")
        
    def fill_serial_no(self):
        """Fill in a randomly generated serial number."""
        serial_no = self.driver.find_element(By.XPATH, "//*[@id='txtSerialNo']")
        serial_no.send_keys(self.generate_fake_serial_no())
        time.sleep(1)
        self.log_action("Filled Serial No")
        
    def fill_model_no(self):
        """Fill in a randomly generated model number."""
        model_no = self.driver.find_element(By.XPATH, "//*[@id='txtPartNumber']")
        model_no.send_keys(self.generate_fake_serial_no())
        time.sleep(1)
        self.log_action("Filled Model no")
        
    def fill_asset_price(self):
        """Fill in a randomly generated asset price."""
        asset_price = self.driver.find_element(By.XPATH, "//*[@id='txtPrice']")
        asset_price.send_keys(self.generate_fake_price())
        time.sleep(1)
        self.log_action("Filled asset price")
        
    def select_department(self, selected_equipment):
        """Select the department based on the selected equipment."""
        department = self.equipment_department_map.get(selected_equipment)
        
        if department:
            department_type = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[2]/div[3]/span")
            department_type.click()
            time.sleep(5)
            
            # Locate and select the department option
            department_dropdown_option = self.driver.find_element(By.XPATH, f"//ul[contains(@class, 'select2-results__options')]/li[contains(text(), '{department}')]")
            department_dropdown_option.click()  # Select the matched department
            print(f"Selected Department: {department}")
            self.log_action(f"Selected Department: {department}" )
            
    def select_vendor(self):
        """Select the item type for the asset."""
        vendor_type = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[2]/div[4]/span")
        vendor_type.click()
        time.sleep(3)
        
        search_box = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(search_box) > 1:
                selected_option = random.choice(search_box[1:])
                selected_vendor = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected Vendor: {selected_vendor}")   # Exclude the first option
        time.sleep(1)
        
    
    def select_location(self):
        """Select the item type for the asset."""
        location = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[3]/div[1]/span")
        location.click()
        time.sleep(3)
        
        search_box = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(search_box) > 1:
                selected_option = random.choice(search_box[1:])
                selected_location = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected location: {selected_location}")  # Exclude the first option
        time.sleep(1)
        
    def manufacturer(self,manufacturer_name):
        manufacturer_field = self.driver.find_element(By.XPATH, "//*[@id='txtMake']")
        manufacturer_field.send_keys(manufacturer_name)
        print(f"Manufacturer: {manufacturer_name}")
        self.log_action(f"Manufacturer: {manufacturer_name}")
        
        time.sleep(1)
        
        
    def generate_manufacturer_name(self, department):
        """Generate a fake manufacturer name based on the equipment's department."""
        if department == "Electrical Department":
            return fake.company() + " Electronics"
        elif department == "Carpentry Department":
            return fake.company() + " Carpentry"
        return fake.company()
    
    def generate_manufacturing_year(self):
        """Generate a random manufacturing year within the past 10 years and fill it in the form."""
        current_year = datetime.now().year
        manufacturing_year = random.randint(current_year - 10, current_year)
        
        # Locate and fill in the manufacturing year field
        manufacturing_year_field = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[3]/div[3]/input")
        manufacturing_year_field.send_keys(str(manufacturing_year))
        print(f"Manufacturing Year: {manufacturing_year}")
        self.log_action(f"Manufacturing Year: {manufacturing_year}")
        time.sleep(1)
        
        return manufacturing_year
    
    def generate_manufacturing_date(self, manufacturing_year):
        """Generate a random manufacturing date within the manufacturing year and fill it in the form."""
        # Define the start and end of the manufacturing year
        start_date = datetime(manufacturing_year, 1, 1)
        end_date = datetime(manufacturing_year, 12, 31)
        
        # Generate a random date within the manufacturing year
        random_manufacturing_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        # Locate and fill in the manufacturing date field
        manufacturing_date_field = self.driver.find_element(By.XPATH, "//*[@id='manufacturedate']/input")
        manufacturing_date_field.send_keys(random_manufacturing_date.strftime('%m-%d-%Y'))
        manufacturing_date_field.send_keys(Keys.RETURN)
        print(f"Manufacturing Date: {random_manufacturing_date.strftime('%m-%d-%Y')}")
        self.log_action(f"Manufacturing Date: {random_manufacturing_date.strftime('%m-%d-%Y')}")
        time.sleep(1)
        
        return random_manufacturing_date
    
    def generate_purchased_and_warranty_dates(self, manufacturing_date):
        """Generate purchased date (after manufacturing date) and warranty end date and fill them in the form."""
        # Purchased date is generated to be between 0 and 180 days after the manufacturing date
        purchased_date = manufacturing_date + timedelta(days=random.randint(0, 180))
        
        # Warranty end date is generated to be between 1 and 5 years after the purchased date
        warranty_end_date = purchased_date + timedelta(days=random.randint(365, 365 * 5))
        
        # Locate and fill in the purchased date field
        purchased_date_field = self.driver.find_element(By.XPATH, "//*[@id='purchaseddate']/input")
        purchased_date_field.send_keys(purchased_date.strftime('%m-%d-%Y'))
        purchased_date_field.send_keys(Keys.RETURN)
        print(f"Purchased Date: {purchased_date.strftime('%m-%d-%Y')}")
        self.log_action(f"Purchased Date: {purchased_date.strftime('%m-%d-%Y')}")
        time.sleep(1)
        
        # Locate and fill in the warranty date field
        warranty_date_field = self.driver.find_element(By.XPATH, "//*[@id='warrantydate']/input")
        warranty_date_field.send_keys(warranty_end_date.strftime('%m-%d-%Y'))
        warranty_date_field.send_keys(Keys.RETURN)
        print(f"Warranty End Date: {warranty_end_date.strftime('%m-%d-%Y')}")
        self.log_action(f"Warranty End Date: {warranty_end_date.strftime('%m-%d-%Y')}")
        
        time.sleep(1)
        
    def warranty_cover(self):
        """Select the item type for the asset."""
        warranty_cover_type = self.driver.find_element(By.XPATH, "//*[@id='addassetsmmodal']/div/div/form/div[1]/div[4]/div[3]/span")
        warranty_cover_type.click()
        time.sleep(3)
        
        search_box = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'select2-results__options')]/li")
        if len(search_box) > 1:
                selected_option = random.choice(search_box[1:])
                selected_warranty_cover = selected_option.text
                selected_option.click()  # Click on the selected location option
                self.log_action(f"Selected Warranty Cover: {selected_warranty_cover}")  # Exclude the first option
        time.sleep(1)
    
    def save(self):
        save_button = self.driver.find_element(By.XPATH, "//*[@id='btnsave']")
        save_button.click()
        time.sleep(3)
        self.log_action("Saved the asset")
    
    def generate_fake_serial_no(self):
        """Generate a fake serial number (9 digits)."""
        serial_no = random.randint(100000000, 999999999)
        return str(serial_no)
    
    def generate_fake_price(self):
        """Generate a fake price for assets in Qatari Riyals."""
        min_price = 1000
        max_price = 10000
        price = random.uniform(min_price, max_price)
        return f"{price:.2f} QAR"  # Price formatted to 2 decimal places with currency
    
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
    login.add_asset()

    # Close the browser
    login.close_browser()
