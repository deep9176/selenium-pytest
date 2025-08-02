import logging
import pytest
from pages.homepage import HomePage
from pages.products import ProductsPage


class TestProducts:
    def test_all_products_list(self, browser):
        logging.info("Starting Tests: Getting list of all products")
        homepage = HomePage(browser)
        homepage.click_products()

        products_page = ProductsPage(browser)
        product_list = products_page.extract_all_products()

        for product in product_list:
            print(f"Product: {product['name']}, Price: {product['price']}")

        assert len(product_list) > 0, "No products were found on the products page."
