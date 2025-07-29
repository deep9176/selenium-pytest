import logging
from pages.login_page import LoginPage
from pages.login_page import user_data_from_json
from utils.test_data_generator import UserDataGenerator


class TestDeleteAccount:

    def test_delete_account(self, browser, user_data_from_json):
        login_page = LoginPage(browser)
        login_page.click_login()
        
        # Perform the delete via UI
        delete_message = login_page.delete_account_after_login(
            user_data_from_json["email"], 
            user_data_from_json["password"]
        )

        assert "ACCOUNT DELETED!" in delete_message

        # Remove user from JSON file
        data_generator = UserDataGenerator()
        assert data_generator.delete_user_by_email(user_data_from_json["email"])