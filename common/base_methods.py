from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class BasePage:
    """
    A base class for Selenium page object models. Provides common methods for interacting with web elements.
    """

    def __init__(self, driver):
        """
        Initializes the BasePage with a WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance for interacting with the browser.
        """
        self.driver = driver

    def open_url(self, url):
        """
        Opens the specified URL in the browser.

        Args:
            url (str): The URL to be opened.
        """
        self.driver.get(url)

    def refresh_page(self):
        """Refreshes the current page."""
        self.driver.refresh()

    def click(self, locator):
        """
        Clicks the specified web element.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
        """
        time.sleep(0.5)  # Ensures the element is ready for interaction
        self.wait_for_element_to_be_clickable(locator=locator)
        element = self.driver.find_element(*locator)
        element.click()

    def get_text_from_element(self, locator):
        """
        Get text from the specified web element.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.

        Returns:
            text[string]: text from element.
        """
        self.wait_for_element_to_be_visible(locator=locator)
        element = self.driver.find_element(*locator)
        return element.text

    def find_elements(self, locator):
        """
        Finds all web elements matching the given locator.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the elements.

        Returns:
            list[WebElement]: A list of found web elements.
        """
        self.wait_for_element_to_be_present(locator=locator)
        return self.driver.find_elements(*locator)

    def find_element(self, locator):
        """
        Finds web element matching the given locator.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the elements.

        Returns:
            WebElement: found web element.
        """
        return self.driver.find_element(*locator)

    def is_displayed(self, locator):
        """
        Checks if the specified element is visible on the page.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        self.wait_for_element_to_be_visible(locator)
        element = self.driver.find_element(*locator)
        return element.is_displayed()

    def is_enabled(self, locator):
        """
        Checks if the specified element is enabled (clickable) on the page.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        element = self.driver.find_element(*locator)
        return element.is_enabled()

    def enter_text(self, locator, keys):
        """
        Enters the specified text into the input field.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
            keys (str): The text to be entered into the input field.
        """
        self.wait_for_element_to_be_visible(locator=locator)
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(keys)

    def wait_for_element_to_be_clickable(self, locator, timeout=10):
        """
        Waits until the specified element is clickable.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
            timeout (int): time to wait until expected condition.

        Returns:
            WebElement: The clickable web element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_to_be_visible(self, locator, timeout=10):
        """
        Waits until the specified element is visible on the page.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
            timeout (int): time to wait until expected condition.

        Returns:
            WebElement: The visible web element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_to_be_invisible(self, locator, timeout=10):
        """
        Waits until the specified element is invisible on the page.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
            timeout (int): time to wait until expected condition.

        Returns:
            WebElement: The visible web element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_element_to_be_present(self, locator, timeout=10):
        """
        Waits until the specified element is present in the DOM.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
            timeout (int): time to wait until expected condition.

        Returns:
            WebElement: The web element present in the DOM.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_text_to_be_present_in_element(self, locator, text, timeout=10):
        """
        Waits until the specified element is present in the DOM with text.

        Args:
            locator (tuple): The locator tuple (By.<method>, <value>) for finding the element.
            text (string): text to be present in element.
            timeout (int): time to wait until expected condition.

        Returns:
            WebElement: The web element present in the DOM with text.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_element_to_be_selected(self, element, timeout=10):
        """
        Waits until the specified element is selected in the DOM.

        Args:
            element (WebElement): WbElement.
            timeout (int): time to wait until expected condition.

        Returns:
            WebElement: The web element selected in the DOM.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_selected(element))

    def wait_title_contain_text(self, text, timeout=30, poll_frequency=0.5):
        """
        Waits until the page title contains text.

        Args:
            text (string): text.
            timeout (int): time to wait until expected condition.
            poll_frequency (float): sleep interval between calls. By default, it is 0.5 second.

        Returns:
            WebElement: The web element in the DOM.
        """
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        return wait.until(EC.title_contains(text))

    def execute_script(self, script, *args):
        """
        Executes JavaScript in the context of the current page.

        Args:
            script (str): The JavaScript code to execute.
            *args: Any arguments to pass into the script.
        """
        self.driver.execute_script(script, *args)

    def scroll_into_view(self, element):
        """
        Scrolls the provided element into the view using JavaScript.

        Args:
            element: The WebElement to scroll into view.
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def get_alert_text(self):
        """
        Retrieves the text from the alert dialog.

        Returns:
            The text displayed in the alert dialog.
        """
        return self.driver.switch_to.alert.text

    def scroll_to_element(self, element):
        """
        Scrolls to the specified element using ActionChains.

        Args:
            element: The WebElement to scroll to.
        """
        ActionChains(self.driver).scroll_to_element(element).perform()
