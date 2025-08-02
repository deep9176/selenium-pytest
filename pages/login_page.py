import pytest
from locators.loginpage_locators import LoginLocators
from locators.homepage_locators import HomePageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.data_loader import load_test_data

@pytest.fixture
def user_data_from_json():
    # Load the user data from login_data.json
    login_data = load_test_data("login_data.json")

    if not login_data:
        raise ValueError("No user data found in login_data.json")
    
    # Fetch the first user from the data (for simplicity, you can choose a user based on some condition)
    user_id = list(login_data.keys())[0]  # Get the first user
    return login_data[user_id]

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login_with_credentials(self, email, password, expect_success=True):
        self.driver.find_element(*LoginLocators.email_field).send_keys(email)
        self.driver.find_element(*LoginLocators.password_field).send_keys(password)
        self.driver.find_element(*LoginLocators.login_button).click()

        if expect_success:
        # Wait for the login to complete, checking for user profile or logged-in user name
            assert WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(LoginLocators.logged_in_check)
            ), "Login failed unexpectedly"
            print("Test Passed: Login successful and logged out successfully.")
        else:
            assert WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(LoginLocators.invalid_login_error_msg)
            ), "Expected login failure, but login succeeded"
            print("Test Passed: Invalid login error displayed.")

    def click_login(self):
        self.driver.find_element(*HomePageLocators.signup_login_button).click()

    def click_logout(self):
        self.driver.find_element(*LoginLocators.logged_in_check).click()
    
    def delete_account_after_login(self, email, password):
        self.driver.find_element(*LoginLocators.email_field).send_keys(email)
        self.driver.find_element(*LoginLocators.password_field).send_keys(password)
        self.driver.find_element(*LoginLocators.login_button).click()

        # Wait for the login to complete, checking for user profile or logged-in user name
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(LoginLocators.logged_in_check)
        )
        self.driver.find_element(*LoginLocators.delete_account).click()
        assert WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(LoginLocators.delete_msg)
        )
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(LoginLocators.delete_msg))
        return element.text