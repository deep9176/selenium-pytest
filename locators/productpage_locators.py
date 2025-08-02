from selenium.webdriver.common.by import By

class ProductPageLoc:
    all_product_title = (By.XPATH, "//h2[@class='title text-center']")
    products = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    product_price = (By.CSS_SELECTOR, ".productinfo h2")
    product_name = (By.CSS_SELECTOR, ".productinfo p")
    view_product = (By.CSS_SELECTOR, ".choose ul li a")
    add_to_cart_button = (By.CSS_SELECTOR, "a.btn.btn-default.add-to-cart")
    continue_shopping = (By.XPATH, "//button[@data-dismiss='modal']")
    review_submit = (By.XPATH, "//button[@id='button-review']")
    proceed_to_checkout = (By.XPATH, "//a[@class='btn btn-default check_out']")
    cart_price = (By.CSS_SELECTOR, ".cart_price")
    cart_total_price = (By.CSS_SELECTOR, ".cart_total_price")
    place_order_button = (By.XPATH, "//a[@class='btn btn-default check_out']")
    name_on_card = (By.XPATH, "//input[@name='name_on_card']")
    card_number = (By.XPATH, "//input[@name='card_number']")
    cvc = (By.XPATH, "//input[@name='cvc']")
    expiry_month = (By.XPATH, "//input[@name='expiry_month']")
    expiry_year = (By.XPATH, "//input[@name='expiry_year']")
    pay_confirm_order = (By.XPATH, "//button[@id='submit']")
    order_placed_msg = (By.XPATH, "//h2[@class='title text-center']/b")

    #equivalent xpath
    #products = (By.XPATH, "//*[contains(@class, 'features_items')]//*[contains(@class, 'col-sm-4')]")
    #product_price = (By.XPATH, ".//div[contains(@class, 'productinfo')]//h2")
    #product_name = (By.XPATH, ".//div[contains(@class, 'productinfo')]//p")