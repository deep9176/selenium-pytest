import logging
from pages.homepage import HomePage


class TestHomepage:
    def test_homepage_title(self, browser):
        logging.info("Starting tests: Homepage Title")
        homepage = HomePage(browser)
        assert "Automation Exercise" in homepage.get_title()
        logging.info("Test Passed: Title contains 'Automation Exercise'")
