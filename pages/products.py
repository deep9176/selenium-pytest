from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.productpage_locators import ProductPageLoc
from locators.homepage_locators import HomePageLocators
import random
import logging


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def extract_all_products(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located(ProductPageLoc.products)
        )

        products = self.driver.find_elements(*ProductPageLoc.products)
        all_data = []

        for product in products:
            try:
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)

                price_elem = product.find_element(*ProductPageLoc.product_price)
                name_elem = product.find_element(*ProductPageLoc.product_name)

                price = price_elem.text.strip()
                name = name_elem.text.strip()

                if not price:
                    price = price_elem.get_attribute("innerText").strip()
                if not name:
                    name = name_elem.get_attribute("innerText").strip()

                logging.info("Product: %s, Price: %s", name, price)
                all_data.append({"name": name, "price": price, "element": product})
            except Exception as e:
                logging.info("Error extracting product: %s", e)
                continue

        return all_data
    
    def add_3_items_in_cart(self):
        products = self.extract_all_products()

        if len(products) < 3:
            raise Exception("Not enough products found to add 3 items to cart")

        selected = random.sample(products, k=3)

        for product in selected:
            try:
                # Re-extract fresh products before each add to avoid stale element exceptions
                fresh_products = self.extract_all_products()

                product_name = product['name']

                # Find the fresh product by name to get its current WebElement
                fresh_product = next(p for p in fresh_products if p['name'] == product_name)
                product_element = fresh_product['element']

                # Scroll product into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_element)

                # Find and click the add to cart button inside the product element
                add_button = product_element.find_element(*ProductPageLoc.add_to_cart_button)
                add_button.click()

                # Wait for the continue shopping button/modal and click it
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(ProductPageLoc.continue_shopping)
                )
                self.driver.find_element(*ProductPageLoc.continue_shopping).click()

                logging.info(f"Added to cart: {product_name}")

            except Exception as e:
                logging.info(f"Failed to add product to cart: {e}")

        # After adding all 3, go to cart
        self.driver.find_element(*HomePageLocators.cart_button).click()
        return selected
    
    def view_product(self):
        products = self.extract_all_products()

        if len(products)<1:
            raise Exception("Not enough products found to add 1 item to cart")
        
        selected = random.sample(products, k=1)[0]

        product_element = selected["element"]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product_element)
        # Find the "View Product" button inside the selected product
        view_button = product_element.find_element(*ProductPageLoc.view_product)
        view_button.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ProductPageLoc.review_submit))
        logging.info(f"View product page visible for product: {selected['name']}")
        return selected
    
    def checkout(self, name, card_number, cvv, exp_month, exp_year):
        products_to_checkout = self.add_3_items_in_cart()

        if len(products_to_checkout)<1:
            raise Exception("Error in adding products to cart")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(ProductPageLoc.proceed_to_checkout))
        self.driver.find_element(*ProductPageLoc.proceed_to_checkout).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(ProductPageLoc.cart_price)
        )
        price_elements = self.driver.find_elements(*ProductPageLoc.cart_price)
        print(price_elements)
        individual_prices = []

        for elem in price_elements:
            text = elem.text.strip().replace("Rs.", "").replace(",", "").strip()
            try:
                price = int(text)
                individual_prices.append(price)
            except ValueError:
                logging.warning(f"Could not convert price text '{text}' to int")

        total_expected = sum(individual_prices)

        total_elements = self.driver.find_elements(*ProductPageLoc.cart_total_price)
        total_actual = 0

        for elem in total_elements:
            text = elem.text.strip().replace("Rs.", "").replace(",", "")
            try:
                total_actual += int(text)
            except ValueError:
                logging.warning(f"Could not parse total: {text}")

        logging.info("Expected total from individual prices: Rs. %s", total_expected)
        logging.info("Displayed total from cart rows: Rs. %s", total_actual)
        
        logging.info("Calculated total: %s | Displayed total: %s", total_expected, total_actual)

        place_order = self.driver.find_element(*ProductPageLoc.place_order_button)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order)
        place_order.click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(ProductPageLoc.name_on_card))

        self.driver.find_element(*ProductPageLoc.name_on_card).send_keys(name)
        self.driver.find_element(*ProductPageLoc.card_number).send_keys(card_number)
        self.driver.find_element(*ProductPageLoc.cvc).send_keys(cvv)
        self.driver.find_element(*ProductPageLoc.expiry_month).send_keys(exp_month)
        self.driver.find_element(*ProductPageLoc.expiry_year).send_keys(exp_year)
        self.driver.find_element(*ProductPageLoc.pay_confirm_order).click()
        order_placed_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ProductPageLoc.order_placed_msg)
        )
        message_text = order_placed_message.text.strip()
        logging.info(f"Order confirmation message text: '{message_text}'")
        assert "ORDER PLACED!" in message_text

        return total_expected, total_actual, message_text

        
        




