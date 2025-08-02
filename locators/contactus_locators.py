from selenium.webdriver.common.by import By


class contactus_locators:
    clk_contactus = (By.PARTIAL_LINK_TEXT, " Contact us")
    contactus_name = (By.XPATH, "//input[@name = 'name']")
    contactus_email = (By.XPATH, "//input[@name = 'email']")
    contactus_subject = (By.XPATH, "//input[@name = 'subject']")
    contactus_message = (By.XPATH, "//textarea[@name = 'message']")
    contactus_submit = (By.XPATH, "//input[@name = 'submit']")
    contactus_upload_file = (By.XPATH, "//input[@name = 'upload_file']")
    contactus_success_msg = (By.XPATH, "//div[@class='status alert alert-success']")