import logging
import pytest
from pages.homepage import HomePage
from pages.products import ProductsPage
from pages.login_page import user_data_from_json
from pages.login_page import LoginPage

class TestProducts:

    def extract_user_data(self, user_data):
        return (
            user_data["email"],
            user_data["password"],
            user_data["full_name"],
            user_data["card_number"],
            user_data["cvv"],
            user_data["exp_month"],
            user_data["exp_year"]
        )

    def login_user(self, browser, email, password):
        login_page = LoginPage(browser)
        login_page.click_login()
        login_page.login_with_credentials(email, password)
        logging.info(f"Login succeeded for: {email}")
        return login_page

    def test_view_product(self, browser):
        logging.info("Starting Test: View a random product")
        HomePage(browser).click_products()
        viewed_product = ProductsPage(browser).view_product()

        assert viewed_product is not None, "No product was selected to view"
        logging.info("Successfully viewed product: %s", viewed_product["name"])

    def test_checkout_3_items(self, browser, user_data_from_json):
        logging.info("Starting Test: Add 3 products and checkout")

        email, password, name, card_num, cvc, exp_mth, exp_yr = self.extract_user_data(user_data_from_json)
        login_page = self.login_user(browser, email, password)

        HomePage(browser).click_products()

        products_page = ProductsPage(browser)
        total_exp, total_act, order_message = products_page.checkout(name, card_num, cvc, exp_mth, exp_yr)

        assert total_exp == total_act, f"Cart total mismatch! Expected: Rs. {total_exp}, Found: Rs. {total_act}"
        logging.info(f"{order_message} successfully")
        login_page.click_logout()

    def test_search_and_checkout(self, browser, user_data_from_json):
        logging.info("Starting Test: Search for 3 products and checkout")

        email, password, name, card_num, cvc, exp_mth, exp_yr = self.extract_user_data(user_data_from_json)
        login_page = self.login_user(browser, email, password)

        HomePage(browser).click_products()

        products_page = ProductsPage(browser)
        total_exp, total_act, order_message = products_page.search_products(name, card_num, cvc, exp_mth, exp_yr)

        assert total_exp == total_act, f"Cart total mismatch! Expected: Rs. {total_exp}, Found: Rs. {total_act}"
        logging.info(f"{order_message} successfully")
        login_page.click_logout()