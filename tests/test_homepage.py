import logging
from pages.homepage import HomePage
import pytest


class TestHomepage:
    @pytest.mark.order(1)
    def test_homepage_title(self, browser):
        logging.info("Starting tests: Homepage Title")
        homepage = HomePage(browser)
        assert "Automation Exercise" in homepage.get_title()
        logging.info("Test Passed: Title contains 'Automation Exercise'")
    
    @pytest.mark.order(6)
    def test_testcases_page(self, browser):
        logging.info("Starting tests: TestCase Page")
        homepage = HomePage(browser)
        element_text = homepage.click_testcases()

        assert "TEST CASES" in element_text, f"Expected 'TEST CASES' in page text, got '{element_text}'"
        logging.info("Test Passed: 'TEST CASES' page loaded successfully")
        


