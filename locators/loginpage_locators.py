from selenium.webdriver.common.by import By    

class LoginLocators:
# Define locators for the login page
    email_field = (By.XPATH, "//input[@data-qa='login-email']")
    password_field = (By.XPATH, "//input[@data-qa='login-password']")
    login_button = (By.XPATH, "//button[@data-qa='login-button']")
    logged_in_check = (By.PARTIAL_LINK_TEXT, "Logout") 
    delete_account = (By.XPATH, "//a[contains(text(), 'Delete')]")
    delete_msg = (By.XPATH, "//h2[@data-qa='account-deleted']")
    invalid_login_error_msg = (By.XPATH, "//p[contains(text(),'Your email or password is incorrect!')]")