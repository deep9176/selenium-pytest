import random
import logging
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.productpage_locators import ProductPageLoc
from locators.homepage_locators import HomePageLocators


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def save_screenshot(self, test_name):
        """Capture screenshot with a unique name based on timestamp."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"{test_name}_{timestamp}.png"  # Name includes test name and timestamp
        
        folder = "test_logs/screenshots/"
        if not os.path.exists(folder):
            os.makedirs(folder)  # Create directory if it doesn't exist

        screenshot_path = os.path.join(folder, screenshot_name)
        self.driver.save_screenshot(screenshot_path)
        logging.info(f"Screenshot saved to: {screenshot_path}")

    def wait_for(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def extract_all_products(self):
        self.wait_for(ProductPageLoc.products)
        products = self.driver.find_elements(*ProductPageLoc.products)
        all_data = []

        for product in products:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
                price = product.find_element(*ProductPageLoc.product_price).text.strip()
                name = product.find_element(*ProductPageLoc.product_name).text.strip()

                if not price:
                    price = product.find_element(*ProductPageLoc.product_price).get_attribute("innerText").strip()
                if not name:
                    name = product.find_element(*ProductPageLoc.product_name).get_attribute("innerText").strip()

                logging.info("Product: %s, Price: %s", name, price)
                all_data.append({"name": name, "price": price, "element": product})
            except Exception as e:
                logging.warning("Error extracting product: %s", e)
                self.save_screenshot("extract_all_products_failure")  # Capture screenshot on failure
        return all_data

    def add_products_to_cart(self, products):
        for product in products:
            try:
                product_element = product["element"]
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_element)
                add_button = product_element.find_element(*ProductPageLoc.add_to_cart_button)
                add_button.click()
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(ProductPageLoc.continue_shopping)
                ).click()
                logging.info(f"Added to cart: {product['name']}")
            except Exception as e:
                logging.warning(f"Failed to add product to cart: {e}")
                self.save_screenshot("add_products_to_cart_failure")  # Capture screenshot on failure
        self.driver.find_element(*HomePageLocators.cart_button).click()

    def view_product(self):
        products = self.extract_all_products()
        if not products:
            raise Exception("No products found")
        selected = random.choice(products)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected["element"])
        selected["element"].find_element(*ProductPageLoc.view_product).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLoc.review_submit))
        logging.info(f"View product page visible for product: {selected['name']}")
        
        # Take a screenshot after viewing the product
        self.save_screenshot("view_product_page")
        return selected

    def extract_prices_and_total(self):
        self.wait_for(ProductPageLoc.cart_price)
        price_elements = self.driver.find_elements(*ProductPageLoc.cart_price)
        individual_prices = []

        for elem in price_elements:
            try:
                price = int(elem.text.strip().replace("Rs.", "").replace(",", ""))
                individual_prices.append(price)
            except ValueError:
                logging.warning(f"Could not parse individual price: {elem.text}")

        total_expected = sum(individual_prices)
        total_actual = 0

        total_elements = self.driver.find_elements(*ProductPageLoc.cart_total_price)
        totals = []

        for elem in total_elements:
            try:
                value = int(elem.text.strip().replace("Rs.", "").replace(",", ""))
                totals.append(value)
            except ValueError:
                logging.warning(f"Could not parse total price: {elem.text}")

        total_actual = max(totals) if totals else 0

        logging.info("Expected total: Rs. %s | Displayed total: Rs. %s", total_expected, total_actual)
        return total_expected, total_actual

    def fill_payment_details_and_place_order(self, name, card_number, cvc, exp_month, exp_year):
        place_order = self.driver.find_element(*ProductPageLoc.place_order_button)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order)
        place_order.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(ProductPageLoc.name_on_card))

        self.driver.find_element(*ProductPageLoc.name_on_card).send_keys(name)
        self.driver.find_element(*ProductPageLoc.card_number).send_keys(card_number)
        self.driver.find_element(*ProductPageLoc.cvc).send_keys(cvc)
        self.driver.find_element(*ProductPageLoc.expiry_month).send_keys(exp_month)
        self.driver.find_element(*ProductPageLoc.expiry_year).send_keys(exp_year)
        self.driver.find_element(*ProductPageLoc.pay_confirm_order).click()

        order_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ProductPageLoc.order_placed_msg)
        ).text.strip()
        logging.info(f"Order confirmation message text: '{order_message}'")
        assert "ORDER PLACED!" in order_message
        
        # Capture screenshot after order placement
        self.save_screenshot("order_placed")
        return order_message

    def checkout(self, name, card_number, cvc, exp_month, exp_year):
        products = self.extract_all_products()
        if len(products) < 3:
            raise Exception("Not enough products to add to cart")
        selected = random.sample(products, 3)
        self.add_products_to_cart(selected)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(ProductPageLoc.proceed_to_checkout)).click()

        total_expected, total_actual = self.extract_prices_and_total()
        
        # Take screenshot after checking the prices
        self.save_screenshot("checkout_prices")

        message_text = self.fill_payment_details_and_place_order(name, card_number, cvc, exp_month, exp_year)
        
        # Take screenshot after completing checkout
        self.save_screenshot("checkout_complete")

        return total_expected, total_actual, message_text

    def search_products(self, name, card_number, cvc, exp_month, exp_year):
        products = self.extract_all_products()
        if not products:
            raise Exception("Product list is empty")

        selected = random.sample(products, 3)

        for product in selected:
            product_name = product["name"]
            logging.info(f"Searching for product: {product_name}")

            # Clear and search
            search_input = self.driver.find_element(*ProductPageLoc.search_text)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_input)
            search_input.clear()
            search_input.send_keys(product_name)
            self.driver.find_element(*ProductPageLoc.search_button).click()

            # Wait until search results are visible
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(ProductPageLoc.products)
            )

            # Simply add the first product in the search results
            result_products = self.driver.find_elements(*ProductPageLoc.products)
            if result_products:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result_products[0])
                add_btn = result_products[0].find_element(*ProductPageLoc.add_to_cart_button)
                add_btn.click()
            else:
                raise Exception(f"No product found for search: {product_name}")
            
            # Take screenshot after each product is added
            self.save_screenshot(f"searched_product_{product_name}")

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(ProductPageLoc.continue_shopping)
            ).click()

        self.driver.find_element(*HomePageLocators.cart_button).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ProductPageLoc.proceed_to_checkout)
        ).click()

        total_expected, total_actual = self.extract_prices_and_total()
        message_text = self.fill_payment_details_and_place_order(name, card_number, cvc, exp_month, exp_year)

        return total_expected, total_actual, message_text