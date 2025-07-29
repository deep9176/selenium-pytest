from locators.signup_locators import SignupLocators
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from utils.test_data_generator import UserDataGenerator


class SignupPage:
    def __init__(self, driver):
        self.driver = driver

    def generate_and_fill_signup_form(self):
        """Convenience method to generate user data, fill the form, and save it"""
        data_generator = UserDataGenerator()
        data_generator.generate_user_data()
        user_data = data_generator.user_data

        self.fill_signup_form(user_data, expected_success=True)
        data_generator.save_user_data_with_id()
        return user_data

    def fill_signup_form(self, user_data, expected_success=True):
        """Fill out the signup form based on provided user_data"""
        self.driver.find_element(*SignupLocators.name_field).send_keys(user_data["first_name"])
        self.driver.find_element(*SignupLocators.email_field).send_keys(user_data["email"])
        self.driver.find_element(*SignupLocators.signup_button).click()

        if not expected_success:
            # For duplicate email scenario, check for the error message and return early
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(SignupLocators.user_exists_msg)
            )
            return

        # Wait for the account info section to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(SignupLocators.name_field_account)
        )

        # Gender
        if user_data["gender"] == "Male":
            self.driver.find_element(*SignupLocators.gender_male).click()
        else:
            self.driver.find_element(*SignupLocators.gender_female).click()

        self.driver.find_element(*SignupLocators.name_field_account).send_keys(user_data["full_name"])
        self.driver.find_element(*SignupLocators.password_field_account).send_keys(user_data["password"])

        Select(self.driver.find_element(*SignupLocators.dob_day)).select_by_value(str(user_data["dob_day"]))
        Select(self.driver.find_element(*SignupLocators.dob_month)).select_by_value(str(user_data["dob_month"]))
        Select(self.driver.find_element(*SignupLocators.dob_year)).select_by_value(str(user_data["dob_year"]))

        self.driver.find_element(*SignupLocators.acc_firstname).send_keys(user_data["first_name"])
        self.driver.find_element(*SignupLocators.acc_lastname).send_keys(user_data["last_name"])
        self.driver.find_element(*SignupLocators.acc_company).send_keys(user_data["company"])
        self.driver.find_element(*SignupLocators.acc_address1).send_keys(user_data["address1"])
        self.driver.find_element(*SignupLocators.acc_address2).send_keys(user_data["address2"])

        Select(self.driver.find_element(*SignupLocators.acc_country)).select_by_value(user_data["country"])

        self.driver.find_element(*SignupLocators.acc_state).send_keys(user_data["state"])
        self.driver.find_element(*SignupLocators.acc_city).send_keys(user_data["city"])
        self.driver.find_element(*SignupLocators.acc_zipcode).send_keys(user_data["zipcode"])
        self.driver.find_element(*SignupLocators.acc_mobile_num).send_keys(user_data["mobile_number"])

        self.driver.find_element(*SignupLocators.submit_button).click()

        # Wait and confirm account creation
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(SignupLocators.acc_created_msg)
        )
        acc_msg = self.driver.find_element(*SignupLocators.acc_created_msg).text
        print("Account Created Message:", acc_msg)
        assert acc_msg == "ACCOUNT CREATED!"

    def check_user_exists(self):
        """Return the text of the 'Email Address already exist!' message"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(SignupLocators.user_exists_msg)
        )
        return element.text