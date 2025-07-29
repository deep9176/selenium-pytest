from selenium.webdriver.common.by import By
from locators.homepage_locators import HomePageLocators


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    
    def get_title(self):
        return self.driver.title
    
    def click_signup(self):
        self.driver.find_element(*HomePageLocators.signup_login_button).click()
