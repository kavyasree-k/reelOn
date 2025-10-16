# conftest.py
import os
import pytest
from selenium import webdriver
from datetime import datetime
from utils.logger_util import get_logger
logger = get_logger(__name__)


@pytest.fixture(scope="function")
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Hook: Log test start
def pytest_runtest_setup(item):
    logger.info(f" STARTING TEST: {item.name}")

# Hook: Log test result + capture screenshot on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        if report.failed:
            logger.error(f"❌ TEST FAILED: {item.name}")
            driver = item.funcargs.get("setup")
            if driver:
                now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"screenshots/{item.name}_{now}.png"
                os.makedirs("screenshots", exist_ok=True)
                driver.save_screenshot(filename)
                logger.info(f" Screenshot saved to {filename}")
        elif report.passed:
            logger.info(f"✅ TEST PASSED: {item.name}")
