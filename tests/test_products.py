import logging
import pytest
from pages.homepage import HomePage
from pages.products import ProductsPage
from pages.login_page import user_data_from_json
from pages.login_page import LoginPage


class TestProducts:
    def test_view_product(self, browser):
        logging.info("Starting Tests: Getting list of all products")
        homepage = HomePage(browser)
        homepage.click_products()

        products_page = ProductsPage(browser)
        viewed_product = products_page.view_product()

        assert viewed_product is not None, "No product was selected to view"
        logging.info("Successfully viewed product: %s", viewed_product["name"])

    def test_checkout_3_items(self, browser, user_data_from_json):
        logging.info("Starting Tests: Add 3 products to cart and checkout")
        email = user_data_from_json["email"]
        password = user_data_from_json["password"]
        name = user_data_from_json["full_name"]
        card_num = user_data_from_json["card_number"]
        cvc = user_data_from_json["cvv"]
        exp_mth = user_data_from_json["exp_month"]
        exp_yr = user_data_from_json["exp_year"]


        logging.info(f"Logged in with user {email}")
        login_page = LoginPage(browser)
        login_page.click_login()
        login_page.login_with_credentials(email, password)
        logging.info(f"Login succeeded for: {email}")
        
        products_page = ProductsPage(browser)
        total_exp, total_act, order_message = products_page.checkout(name, card_num, cvc, exp_mth, exp_yr)
        assert total_exp == total_act, (f"Cart total mismatch! Expected: Rs. {total_exp}, Found: Rs. {total_act}")
        logging.info(f"{order_message.text} successfully ")

        


