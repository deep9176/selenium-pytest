from locators.homepage_locators import HomePageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    
    def get_title(self):
        return self.driver.title
    
    def click_signup(self):
        self.driver.find_element(*HomePageLocators.signup_login_button).click()
    
    def click_contactus(self):
        self.driver.find_element(*HomePageLocators.contactus_button).click()

    def click_testcases(self):
        self.driver.find_element(*HomePageLocators.testcases_button).click()
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(HomePageLocators.tc_title))

        return element.text
    
    def click_products(self):
        self.driver.find_element(*HomePageLocators.products_button).click()

