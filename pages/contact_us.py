from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.contactus_locators import contactus_locators
from utils.data_loader import load_test_data
import pytest
import os
from selenium.common.exceptions import NoAlertPresentException


@pytest.fixture
def user_data_from_json():
    contactus_user_data = load_test_data("login_data.json")
    if not contactus_user_data:
        raise ValueError("No user data found in login_data.json")
    user_id = list(contactus_user_data.keys())[0]
    return user_id


class ContactUs_Form:
    def __init__(self, driver):
        self.driver = driver

    def fill_contactus_form(self, name, email):
        assert WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(contactus_locators.contactus_name))
        self.driver.find_element(*contactus_locators.contactus_name).send_keys(name)
        self.driver.find_element(*contactus_locators.contactus_email).send_keys(email)
        self.driver.find_element(*contactus_locators.contactus_subject).send_keys("test_deep_8000")
        self.driver.find_element(*contactus_locators.contactus_message).send_keys("This is to test that message input works from deep_8000")
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "testdata", "contact_us_sample_file.txt"))
        self.driver.find_element(*contactus_locators.contactus_upload_file).send_keys(file_path)
        self.driver.find_element(*contactus_locators.contactus_submit).click()
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print(f"Alert Message: {alert.text}")
            alert.accept()
        except NoAlertPresentException:
            print("No alert appeared after form submission")
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(contactus_locators.contactus_success_msg))
        if "Success!" in element.text:
            return True
        return False