import os

import pytest
from selenium import webdriver

from .common.base_methods import BasePage


def pytest_addoption(parser):
    """
    Adds custom command-line options to pytest.

    Args:
        parser (ArgumentParser): The argument parser used by pytest to parse command-line options.
    """
    parser.addoption('--browser', help='Which test browser?', default='chrome')
    parser.addoption('--headless', help='headless or non-headless?', choices=['true', 'false'], default='false')
    parser.addoption(
        '--extension', help='load "coordinates.crx" extension?', choices=['true', 'false'], default='false')


@pytest.fixture(scope='session')
def test_browser(request):
    """
    Retrieves the selected browser from the command-line options.

    Args:
        request (FixtureRequest): A pytest fixture that provides information about the requesting test function.

    Returns:
        str: The name of the browser specified in the --browser option (e.g., 'chrome', 'firefox').
    """
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def headless(request):
    """
    Retrieves the headless mode option from the command-line options.

    Args:
        request (FixtureRequest): A pytest fixture that provides information about the requesting test function.

    Returns:
        str: 'true' or 'false', based on the value of the --headless option.
    """
    return request.config.getoption('--headless')


@pytest.fixture(scope='session')
def extension(request):
    """
    Load the 'coordinates' extension to browser.

    Args:
        request (FixtureRequest): A pytest fixture that provides information about the requesting test function.

    Returns:
        str: 'true' or 'false', based on the value of the --headless option.
    """
    return request.config.getoption('--extension')


@pytest.fixture(scope='function', autouse=True)
def driver(request, test_browser, headless):
    """
    Initializes the WebDriver instance based on the selected browser and headless mode.

    Args:
        request (FixtureRequest): A pytest fixture that provides information about the requesting test function.
        test_browser (str): The name of the browser to use ('chrome' or 'firefox').
        headless (str): Specifies whether to run the browser in headless mode ('true' or 'false').

    Yields:
        WebDriver: The initialized WebDriver instance.

    Raises:
        ValueError: If an unsupported browser is specified.
    """
    if test_browser == 'firefox':
        if headless == 'false':
            driver = webdriver.Firefox()
        else:
            geco_options = webdriver.FirefoxOptions()
            geco_options.add_argument("-headless")
            driver = webdriver.Firefox(options=geco_options)
    elif test_browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if headless == 'true':
            chrome_options.add_argument("--headless=new")
        if extension == 'true':
            chrome_options.add_extension(f'{os.path.dirname(os.path.abspath(__file__))}/resources/0.2_0.crx')
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
    else:
        raise ValueError(f'--browser="{test_browser}" is not chrome or firefox')

    request.cls.driver = driver
    yield driver
    result = request.session.testsfailed
    if result != 0:
        BasePage.take_screenshot_as_png(request.cls, name=request.node.originalname + "_Failed_Screenshot")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "rep_outcome", rep.outcome)
    else:
        setattr(item, "rep_outcome", "")
