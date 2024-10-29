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
        
        
    def navigate_to_add_unit(self):
        try:
            # Click on the landlord dropdown and select a random option
            landlord_dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[1]/span/span[1]/span")
            landlord_dropdown.click()
            time.sleep(2)
            landlord_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlLandlord-results']/li")  # Adjust XPath for the dropdown options
            random.choice(landlord_options).click()
            
        except:
            
            def is_element_visible(driver, xpath):
                try:
                    element = driver.find_element(By.XPATH, xpath)
                    return element.is_displayed()  # Check if the element is visible
                except NoSuchElementException:
                    return False  # If the element doesn't exist, it's considered not visible
            # Not on the 'Overview' page, need to navigate
            
            leasing_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Leasing Management']")
            leasing_management.click()
            time.sleep(10)

            property_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Property Management']")
            property_management.click()
            time.sleep(5)

            overview = self.driver.find_element(By.XPATH, "//a[normalize-space()='Add Unit']")
            overview.click()
            time.sleep(5)

            
            # Click on the landlord dropdown and select a random option
            landlord_dropdown = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[1]/span/span[1]/span")
            landlord_dropdown.click()
            time.sleep(2)
            landlord_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlLandlord-results']/li")  # Adjust XPath for the dropdown options
            # random.choice(landlord_options).click()
            if len(landlord_options) > 1:
                random.choice(landlord_options[1:]).click()  # Exclude the first option
            
            # Click on the unit type dropdown and select a random option
            unit_type = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[2]/span")
            unit_type.click()
            time.sleep(2)
            unit_type_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlUnitType-results']/li")  # Adjust XPath for the dropdown options
            # random.choice(unit_type_options).click()
            if len(unit_type_options) > 1:
                random.choice(unit_type_options[1:]).click()
            time.sleep(3)
            
            # Click on the venture dropdown and select a random option
            venture = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlVenture-container']")
            venture.click()
            time.sleep(2)
            venture_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlVenture-results']/li")  # Adjust XPath for the dropdown options
            if len(venture_options) > 1:
                random.choice(venture_options[1:]).click()
            time.sleep(5)
            
            # Click on the property type dropdown and select a random option
            property_type = self.driver.find_element(By.XPATH, "//span[@id='select2-ddlPropertyType-container']")
            property_type.click()
            time.sleep(2)
            property_type_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlPropertyType-results']/li")  # Adjust XPath for the dropdown options
            if len(property_type_options) > 1:
                random.choice(property_type_options[1:]).click()
            
            property_name = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[5]/input")
            property_name.send_keys(self.generate_property_name())
            time.sleep(1)
            
            property_area = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[6]/input")
            property_area.send_keys(self.generate_property_area())
            time.sleep(5)
            
          # Click on the property size dropdown and select a random option
            # property_size = self.driver.find_element(By.XPATH, "//span[@id='select2-txtPlotArea-container']")
            # property_size.click()
            # time.sleep(2)
            # property_size_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-txtPlotArea-results']/li")  # Adjust XPath for the dropdown options
            # if len(property_size_options) > 1:
            #     random.choice(property_size_options[1:]).click()
            
            # Check if the "Property Size" dropdown is visible after selecting a venture
            property_size_xpath = "//span[@id='select2-txtPlotArea-container']"
            if is_element_visible(self.driver, property_size_xpath):
                # If the dropdown is visible, click and select a random option
                property_size = self.driver.find_element(By.XPATH, property_size_xpath)
                property_size.click()
                time.sleep(2)
                property_size_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-txtPlotArea-results']/li")
                if len(property_size_options) > 1:
                    random.choice(property_size_options[1:]).click()  # Exclude the first option
            else:
                print("Property Size dropdown is not visible, skipping...")
                
            self.driver.execute_script("window.scrollBy(0, 100);")
            
                    
            
            property_flat_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[8]/input")
            property_flat_no.send_keys(self.generate_flat_no())
            time.sleep(1)
            
            property_floor_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[9]/input")
            property_floor_no.send_keys(self.generate_floor_number())
            time.sleep(1)
            
            property_no_of_floors = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[10]/input")
            property_no_of_floors.send_keys(self.generate_total_floors())
            time.sleep(1)
            
            property_rent = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[11]/input")
            property_rent.send_keys(self.generate_rent_amount())
            time.sleep(1)
            
            self.driver.execute_script("window.scrollBy(0, 100);")
            
            
            # Click on the property country dropdown and select a random option
            property_country = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[12]/span")
            property_country.click()
            time.sleep(2)
            property_country_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlCountry-results']/li")  # Adjust XPath for the dropdown options
            if len(property_country_options) > 1:
                random.choice(property_country_options[1:]).click()
            time.sleep(3)
            
            # Check if the selected country is Canada
            if "Canada" in property_country.text:
                # Use the XPath for Canadian city dropdown
                city_xpath = "//span[@id='select2-ddlPCity-container']"
                # city_options_xpath = "//ul[@id='select2-ddlPCity-results']/li"
            else:
                # Use the general XPath for other countries
                city_xpath = "//span[@id='select2-ddlCity-container']"
                # city_options_xpath = "//ul[@id='select2-ddlCity-results']/li"

            # Click on the property city dropdown and select a random option excluding the first
            property_city = self.driver.find_element(By.XPATH, city_xpath)
            property_city.click()
            time.sleep(2)
            property_city_options = self.driver.find_elements(By.XPATH, "//ul[@id='select2-ddlCity-results']/li" if "Canada" not in property_country.text else "//ul[@id='select2-ddlPCity-results']/li")
            if len(property_city_options) > 1:
                random.choice(property_city_options[1:]).click()  # Exclude the first option
            time.sleep(1)
            
            self.driver.execute_script("window.scrollBy(0, 100);")
            
            
        
            property_bldg_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[14]/input")
            property_bldg_no.send_keys(self.generate_building_number())
            time.sleep(1)
            
            property_street_name = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[15]/input")
            property_street_name.send_keys(self.generate_street_name())
            time.sleep(1)
            
            property_shop_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[16]/input")
            property_shop_no.send_keys(self.generate_shop_no())
            time.sleep(1)
            
            property_street_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[17]/input")
            property_street_no.send_keys(self.generate_street_number())
            time.sleep(1)
            
            property_zone_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[18]/input")
            property_zone_no.send_keys(self.generate_zone_number())
            time.sleep(1)
            self.driver.execute_script("window.scrollBy(0, 100);")
            
            
            property_p_o_box_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[19]/input")
            property_p_o_box_no.send_keys(self.generate_po_box())
            time.sleep(5)
            
            # Locate the dropdown element by name attribute
            property_board_dropdown = self.driver.find_element(By.NAME,"Board")
            # Create a Select object
            select = Select(property_board_dropdown)
            
            select.select_by_index(1)
            
            property_board_karahma = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[20]/select/option[2]")
            property_board_karahma.click
            time.sleep(1)
            
            
            property_view = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[21]/input")
            property_view.send_keys(self.generate_view())
            time.sleep(1)
            
            property_net_size = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[22]/input")
            property_net_size.send_keys(self.generate_net_size())
            time.sleep(1)
            
            property_gross_size = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[23]/input")
            property_gross_size.send_keys(self.generate_gross_size())
            time.sleep(1)
            
            property_consumer_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[24]/input")
            property_consumer_no.send_keys(self.generate_consumer_number())
            time.sleep(1)
            self.driver.execute_script("window.scrollBy(0, 100);")
            
            
            property_electicity_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[25]/input")
            property_electicity_no.send_keys(self.generate_electricity_number())
            time.sleep(1)
            
            property_water_no = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[26]/input")
            property_water_no.send_keys(self.generate_water_number())
            time.sleep(1)
            
            property_description = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/div[27]/textarea")
            property_description.send_keys(self.generate_fake_description())
            time.sleep(1)
            
            fake_property_path = self.generate_fake_property_image()
            time.sleep(15)  # Add a delay if necessary (for example, if page load is slow)

            # Locate the file input element using its ID
            file_input = self.driver.find_element(By.ID, "file-input")

            # Upload the image by sending the file path to the input element
            file_input.send_keys(fake_property_path)
            print(f"Image uploaded successfully: {fake_property_path}")
            time.sleep(3)
            
            save_button = self.driver.find_element(By.XPATH, "//button[@id='btnSaveProperty']")
            save_button.click()
            time.sleep(3)
            
            
            
               
    # Generate a fake property name
    def generate_property_name(self):
        # List of predefined property names
        property_names = ["TestProp", "Property-23", "Property-24"]
        # Randomly choose one of the names
        name = random.choice(property_names)
        return name
    # Function to generate a random property area in square meters
    def generate_property_area(self,min_sqm=50, max_sqm=1000):
        return random.randint(min_sqm, max_sqm)
    
    # Function to generate Flat No
    def generate_flat_no(self):
        return random.randint(1, 100)

    # Function to generate Floor Number
    def generate_floor_number(self):
        return random.randint(1, 50)

    # Function to generate Total No of Floors
    def generate_total_floors(self):
        return random.randint(10, 100)

    # Function to generate Rent Amount (assuming currency is in Egyptian Pounds)
    def generate_rent_amount(self):
        return round(random.uniform(1000, 10000), 2)

    # Function to generate Building Number
    def generate_building_number(self):
        return fake.building_number()

    # Function to generate Street Name
    def generate_street_name(self):
        return fake.street_name()

    # Function to generate Zone Number
    def generate_zone_number(self):
        return random.randint(1, 50)

    # Function to generate Shop No
    def generate_shop_no(self):
        return random.randint(1, 500)

    # Function to generate Street Number
    def generate_street_number(self):
        return fake.building_number()

    # Function to generate P.O Box
    def generate_po_box(self):
        return random.randint(1000, 9999)

    # Function to generate View (like "Sea view", "Garden view", etc.)
    def generate_view(self):
        views = ['Sea view', 'Garden view', 'City view', 'Mountain view']
        return random.choice(views)

    # Function to generate Net Size (in sqm)
    def generate_net_size(self):
        return round(random.uniform(50, 200), 2)

    # Function to generate Gross Size (in sqm)
    def generate_gross_size(self):
        return round(random.uniform(100, 300), 2)

    # Function to generate Consumer Number
    def generate_consumer_number(self):
        return fake.random_number(digits=10)

    # Function to generate Electricity Number
    def generate_electricity_number(self):
        return fake.random_number(digits=8)

    # Function to generate Water Number
    def generate_water_number(self):
        return fake.random_number(digits=8)
    
    def generate_fake_description(self,max_length=150):
        description = fake.text(max_nb_chars=max_length)
        
        # Ensure the description is not longer than max_length
        if len(description) > max_length:
            description = description[:max_length].rstrip() + "..."
    
        return description

    def generate_fake_property_image(self):
        """Generate a fake property image and save it as a .jpg file with a unique name."""
        # Create a unique name for the image file using current timestamp
        image_file_name = f"fake_property_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        image_path = os.path.abspath(image_file_name)

        # Download the property image
        self.download_random_image(image_path)

        return image_path

    def download_random_image(self, image_path):
        """Download a random fake property image from 'loremflickr'."""
        url = "https://loremflickr.com/640/480/house"  # URL for random house images
        response = requests.get(url)

        if response.status_code == 200:
            # Save the image to the specified path
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully: {image_path}")
        else:
            print("Failed to download the image.")
                    
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
    login.navigate_to_add_unit()
    # time.sleep(10)
    

    # Close the browser
    login.close_browser()