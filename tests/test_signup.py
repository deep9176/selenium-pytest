import logging
import pytest
import random
from pages.homepage import HomePage
from pages.signup_page import SignupPage
from utils.test_data_generator import UserDataGenerator
from utils.data_loader import load_test_data

valid_countries = ["India", "United States", "Canada", "Australia", "Israel", "New Zealand", "Singapore"]

test_data = [
    pytest.param("none", True, marks=pytest.mark.valid_signup, id="Valid Signup"),
    pytest.param("existing_user", False, marks=pytest.mark.invalid_signup, id="Invalid Signup - User Exists"),
]

@pytest.fixture
def valid_country():
    return random.choice(valid_countries)


@pytest.mark.parametrize("modifier, expect_success", test_data)
@pytest.mark.order(2)
def test_valid_signup_flow(browser, valid_country, modifier, expect_success):
    logging.info(f"Starting Test: Signup Flow - Modifier: {modifier}")

    if modifier == "existing_user":
        # Load an existing user from JSON
        all_users = load_test_data("login_data.json")
        if not all_users:
            raise Exception("No existing user data found for duplicate test.")
        existing_user = list(all_users.values())[0]
        user_data = existing_user
    else:
        # Generate new user
        data_generator = UserDataGenerator()
        data_generator.generate_user_data()
        user_data = data_generator.user_data
        user_data["country"] = valid_country

    # Go to signup page
    homepage = HomePage(browser)
    homepage.click_signup()

    # Fill signup form
    signup_page = SignupPage(browser)
    signup_page.fill_signup_form(user_data, expected_success=expect_success)

    if expect_success:
        # Save only newly created users
        data_generator.user_data = user_data
        data_generator.save_user_data_with_id()
        logging.info(f"Test Passed: Signed up user {user_data['email']}")
    else:
        # Expect failure (email already exists)
        exists_msg = signup_page.check_user_exists()
        assert exists_msg == "Email Address already exist!"
        logging.info(f"Test Passed: Duplicate signup blocked for {user_data['email']}")