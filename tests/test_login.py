import logging
import pytest
from pages.login_page import LoginPage
from pages.login_page import user_data_from_json

test_data = [
    pytest.param("none", True, marks=pytest.mark.valid, id="Valid Login"),
    pytest.param("invalid_email", False, marks=pytest.mark.invalid, id="Invalid Login - Wrong Email"),
    pytest.param("invalid_password", False, marks=pytest.mark.invalid, id="Invalid Login - Wrong Password"),
]

@pytest.mark.parametrize("modifier, expect_success", test_data)
@pytest.mark.order(3)
def test_login(browser, user_data_from_json, modifier, expect_success):
    email = user_data_from_json["email"]
    password = user_data_from_json["password"]

    logging.info(f"Running login test: modifier={modifier}, expect_success={expect_success}")

    if modifier == "invalid_email":
        email = "invalid_" + email
    elif modifier == "invalid_password":
        password = "invalid_" + password

    login_page = LoginPage(browser)
    login_page.click_login()
    login_page.login_with_credentials(email, password, expect_success=expect_success)

    if expect_success:
        logging.info(f"Login succeeded for: {email}")
    else:
        logging.info(f"Login failed as expected for: {email}")