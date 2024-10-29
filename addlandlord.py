import pytest
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
import os

# Create a Faker instance with 'ar_EG' locale for Qatar-specific data
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

    def navigate_to_add_landlord(self, iteration):
        """Navigate to add landlord and perform the addition."""
        try:
            # Look for the landlord element to determine if we need to navigate
            landlord_element = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div[3]/a/div/span")
            landlord_element.click()
        except Exception as e:
            # Not on the 'Overview' page, need to navigate
            leasing_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Leasing Management']")
            leasing_management.click()
            time.sleep(20)

            property_management = self.driver.find_element(By.XPATH, "//span[normalize-space()='Property Management']")
            property_management.click()
            time.sleep(10)

            overview = self.driver.find_element(By.XPATH, "//a[normalize-space()='Overview']")
            overview.click()
            time.sleep(10)

            # Now click on Landlord
            landlord = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div[3]/a/div/span")
            landlord.click()
            time.sleep(10)

        # Proceed to click the 'Add Landlord' button
        add_landlord = self.driver.find_element(By.XPATH, "//a[@class='btn btn-outline-primary btn-icon-text']")
        add_landlord.click()
        time.sleep(10)

        # Click to open the Select2 dropdown for Company selection
        dropdown = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div/form/div[1]/div[1]/div[1]/span")
        dropdown.click()
        time.sleep(5)

        search_box = self.driver.find_element(By.XPATH, "//input[@class='select2-search__field']")
        search_box.send_keys("Haider Holding")
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Fill in details for the new landlord
        name = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div/form/div[1]/div[1]/div[2]/input")
        name.send_keys(fake.name())
        time.sleep(1)

        email = self.driver.find_element(By.XPATH, "//*[@id='addlandlord']/div/div/form/div[1]/div[1]/div[3]/input")
        email.send_keys(fake.email())
        time.sleep(1)

        phone_no = self.driver.find_element(By.XPATH, "//*[@id='txtMobileNo']")
        phone_no.send_keys(self.generate_qatari_phone_number())
        time.sleep(1)

        # List of ID Types
        id_types = ["Passport", "QID", "CR"]

        # Select the ID Type based on the current iteration
        select_element = self.driver.find_element(By.ID, "VcName")
        select_dropdown = Select(select_element)
        select_dropdown.select_by_visible_text(id_types[iteration % len(id_types)])  # Alternate ID types
        time.sleep(1)

        # Enter the ID number based on selected ID type
        type_no = self.driver.find_element(By.ID, "TTypeNo")
        if id_types[iteration % len(id_types)] == "Passport":
            type_no.send_keys(fake.passport_number())
        elif id_types[iteration % len(id_types)] == "QID":
            type_no.send_keys(self.generate_fake_qatari_qid_number())
        elif id_types[iteration % len(id_types)] == "CR":
            type_no.send_keys(self.generate_fake_qatari_cr_number())
        time.sleep(1)

        # Enter the expiry date
        expiry_date_field = self.driver.find_element(By.ID, "DExpiryDate")
        expiry_date_field.send_keys("25-12-2030")
        time.sleep(3)

        # Generate a fake passport and upload it
        fake_passport_path = self.generate_fake_passport()
        time.sleep(15)
        browse_button = self.driver.find_element(By.XPATH, "//*[@id='addlandlord']/div/div/form/div[1]/div[2]/div[4]/div/div/span/button")
        browse_button.click()
        time.sleep(3)

        # Use pyautogui to upload the generated passport
        pyautogui.write(fake_passport_path)
        pyautogui.press('enter')
        time.sleep(3)

        # Click add and save buttons
        add_button = self.driver.find_element(By.XPATH, "//*[@id='addlandlord']/div/div/form/div[1]/div[2]/button")
        add_button.click()
        time.sleep(3)
        save_button = self.driver.find_element(By.XPATH, "//*[@id='btnsavell']")
        save_button.click()
        time.sleep(10)

        # Verify the addition (e.g., check for a success message)
        # assert "success message or expected condition" in self.driver.page_source

    def generate_fake_passport(self):
        """Generate a fake passport image and return the file path with a unique name."""
        # Create a dynamic name for the passport file
        passport_file_name = f"fake_passport_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
        image_path = os.path.abspath(f"fake_passport_photo_{time.strftime('%Y%m%d_%H%M%S')}.jpg")
        self.download_random_image(image_path)

        # Generate fake details using Faker (Qatari-specific)
        details = self.generate_fake_passport_details()

        # Create a PDF passport with the fake details
        output_pdf = passport_file_name
        self.create_fake_passport(image_path, details, output_pdf)

        return os.path.abspath(output_pdf)

    def download_random_image(self, image_path):
        """Download a random fake person image from 'thispersondoesnotexist'."""
        url = "https://thispersondoesnotexist.com/"
        response = requests.get(url)

        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully: {image_path}")
        else:
            print("Failed to download the image.")

    def generate_fake_passport_details(self):
        """Generate fake details for a Qatari passport."""
        return {
            'name': fake.name(),
            'passport_number': self.generate_fake_qatari_passport_number(),
            'nationality': "Qatar",
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%d-%m-%Y"),
            'expiry_date': fake.date_this_century(after_today=True).strftime("%d-%m-%Y"),
            'gender': fake.random_element(elements=('M', 'F')),
            'place_of_birth': fake.city(),
        }

    def create_fake_passport(self, image_path, details, output_pdf):
        """Generate a fake passport PDF with given details and image."""
        c = canvas.Canvas(output_pdf, pagesize=letter)
        width, height = letter

        # Add a title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Passport")

        # Add the fake passport image
        c.drawImage(image_path, 1 * inch, height - 3 * inch, width=2 * inch, height=2 * inch)

        # Add the fake passport details
        c.setFont("Helvetica", 12)
        c.drawString(4 * inch, height - 1.5 * inch, f"Name: {details['name']}")
        c.drawString(4 * inch, height - 2 * inch, f"Passport No: {details['passport_number']}")
        c.drawString(4 * inch, height - 2.5 * inch, f"Nationality: {details['nationality']}")
        c.drawString(4 * inch, height - 3 * inch, f"Date of Birth: {details['date_of_birth']}")
        c.drawString(4 * inch, height - 3.5 * inch, f"Expiry Date: {details['expiry_date']}")
        c.drawString(4 * inch, height - 4 * inch, f"Gender: {details['gender']}")
        c.drawString(4 * inch, height - 4.5 * inch, f"Place of Birth: {details['place_of_birth']}")

        c.save()

    def generate_fake_qatari_passport_number(self):
        """Generate a fake Qatari passport number."""
        return f"{fake.random_int(min=100000, max=999999)}-{fake.random_int(min=100, max=999)}"

    def generate_fake_qatari_qid_number(self):
        """Generate a fake Qatari QID number."""
        return f"{fake.random_int(min=10000000, max=99999999)}"

    def generate_fake_qatari_cr_number(self):
        """Generate a fake Qatari CR number."""
        return f"{fake.random_int(min=100000, max=999999)}-{fake.random_int(min=100, max=999)}"

    def generate_qatari_phone_number(self):
        """Generate a fake Qatari phone number."""
        return "+974 " + str(fake.random_int(min=30000000, max=39999999))

    def close(self):
        """Close the driver."""
        self.driver.quit()


# Test class using pytest
@pytest.fixture(scope="module")
def setup_driver():
    """Fixture to set up the driver before tests."""
    haider_properties = HaiderPropertiesLogin()
    yield haider_properties
    haider_properties.close()


def test_login_and_add_landlord(setup_driver):
    """Test to login and add a landlord."""
    haider_properties = setup_driver
    haider_properties.open_website("https://test.haiderproperties.com/")  # Replace with actual login URL
    time.sleep(10)
    haider_properties.login("superadmin", "Admin$213")  # Replace with actual credentials
    time.sleep(15)

    # Perform the landlord addition multiple times
    for i in range(3):  # Adjust the number of iterations as needed
        time.sleep(15)
        haider_properties.navigate_to_add_landlord(i)

