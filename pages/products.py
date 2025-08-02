from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.productpage_locators import ProductPageLoc


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

                print(f"Product: {name}, Price: {price}")
                all_data.append({"name": name, "price": price})
            except Exception as e:
                print(f"Error extracting product: {e}")
                continue

        return all_data