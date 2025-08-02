from selenium.webdriver.common.by import By

class ProductPageLoc:
    all_product_title = (By.XPATH, "//h2[@class='title text-center']")
    products = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    product_price = (By.CSS_SELECTOR, ".productinfo h2")
    product_name = (By.CSS_SELECTOR, ".productinfo p")
    view_product = (By.PARTIAL_LINK_TEXT, "product_details")
    #equivalent xpath
    #product_price = (By.XPATH, ".//div[contains(@class, 'productinfo')]//h2")
    #product_name = (By.XPATH, ".//div[contains(@class, 'productinfo')]//p")