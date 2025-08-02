import pytest
import logging
import os
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.homepage import HomePage

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def pytest_configure(config):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = f"reports/report_{timestamp}.html"

    # If html plugin is available, set the report path dynamically
    config.option.htmlpath = report_file
    config.option.self_contained_html = True


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="all", help="Browser to run tests on: chrome, firefox, or all"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )


def initialize_chrome(headless=False):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")

    # Use cache only, don't check GitHub every time
    driver_path = ChromeDriverManager(driver_version="138.0.7204.183").install()
    service = ChromeService(driver_path)
    return webdriver.Chrome(service=service, options=options)


def initialize_firefox(headless=False):
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")

    # Use cache only, valid for 1 year
    driver_path = GeckoDriverManager(version="v0.36.0").install()
    service = FirefoxService(driver_path)
    return webdriver.Firefox(service=service, options=options)


@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    logging.info("Initializing browser: {browser_name}")

    if browser_name != "all":
        browsers_to_run = [browser_name]
    else:
        browsers_to_run = ["chrome", "firefox"]

    if request.param not in browsers_to_run:
        pytest.skip(f"Skipping {request.param} since it is not in browsers_to_run")

    if request.param == "chrome":
        driver = initialize_chrome(headless)
    elif request.param == "firefox":
        driver = initialize_firefox(headless)
    else:
        raise ValueError(f"Unsupported Browser: {request.param}")

    driver.maximize_window()

    logging.info("Navigating to Automation Exercise website")
    driver.get("https://www.automationexercise.com/")

    WebDriverWait(driver, 10).until(EC.title_contains("Automation Exercise"))

    homepage = HomePage(driver)
    title = homepage.get_title()
    logging.info("Page loaded successfully with title: %s", title)

    yield driver
    driver.quit()