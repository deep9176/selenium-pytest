import logging
import pytest
from pages.homepage import HomePage
from pages.contact_us import ContactUs_Form
from pages.login_page import user_data_from_json


@pytest.mark.order(5)
def test_contact_us(browser, user_data_from_json):
    logging.info("Starting Tests: Filling and Submitting Contact Us form")
    name = user_data_from_json["full_name"]
    email = user_data_from_json["email"]

    homepage = HomePage(browser)
    homepage.click_contactus()

    contact_us = ContactUs_Form(browser)

    success = contact_us.fill_contactus_form(name, email)
    assert success, "Contact Us form submission failed"
    logging.info("Form submitted successfully")


