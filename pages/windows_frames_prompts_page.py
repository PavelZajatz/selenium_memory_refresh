from ..common.base_methods import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WindowsFramesPromptsPage(BasePage):
    """
    Page class for handling windows related actions.
    """

    def __init__(self, driver):
        """
        Initializes the WindowsFramesPromptsPage with the WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        """
        super().__init__(driver)

    def try_to_get_text_from_alert(self):
        """
        Attempts to retrieve text from a JavaScript alert and close it.

        This method switches the driver's context to a JavaScript alert,
        captures the text displayed in the alert, and then accepts (closes) the alert.
        If no alert is present, the method returns False.

        Returns:
            str: The text from the alert if present; otherwise, False.
        """
        try:
            prompt = self.driver.switch_to.alert
            secret = prompt.text
            prompt.accept()
        except:
            return False
        return secret

    def get_inner_size(self, width_locator, height_locator):
        """
        Retrieves the inner width and height of the browser window from specified elements.

        Args:
            width_locator (tuple): Locator for the width element.
            height_locator (tuple): Locator for the height element.

        Returns:
            tuple: (inner_width, inner_height)
        """
        inner_width = int(self.driver.find_element(*width_locator).text.split(": ")[1])
        inner_height = int(self.driver.find_element(*height_locator).text.split(": ")[1])
        return inner_width, inner_height

    def get_outer_size(self):
        """
        Retrieves the outer width and height of the browser window.

        Returns:
            tuple: (outer_width, outer_height)
        """
        size = self.driver.get_window_size()
        return size.get('width'), size.get('height')

    def set_window_size(self, width, height):
        """
        Sets the browser window size.

        Args:
            width (int): The width to set for the window.
            height (int): The height to set for the window.
        """
        self.driver.set_window_size(width, height)

    def wait_for_text_to_be_present_in_element(self, locator, text, timeout=10):
        """
        Waits for a specific text to be present in an element located by the given locator.

        Args:
            locator (tuple): Locator for the element.
            text (str): The text to wait for.
            timeout (int): Maximum time to wait for the text.

        Returns:
            str: The text from the element if present; otherwise, an empty string.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return self.driver.find_element(*locator).text
        except:
            return ""

    def switch_to_alert(self):
        """
        Switches the driver's context to the currently active alert.

        Returns:
            Alert: The active alert object to interact with.
        """
        return self.driver.switch_to.alert

    def switch_to_alert_and_send_keys(self, key):
        """
        Switches to the active alert, sends the specified keys, and accepts the alert.

        Args:
            key (str): The keys to send to the alert's input field.
        """
        prompt = self.switch_to_alert()
        prompt.send_keys(key)
        prompt.accept()

    def switch_to_iframe(self, iframe):
        """
        Switches the driver's context to the specified iframe.

        Args:
            iframe (str or WebElement): The iframe to switch to, identified by name, index, or WebElement.
        """
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        """
        Switches the driver's context back to the default content, i.e., the main document.

        Use this method to exit an iframe or other nested context and return to the main document.
        """
        self.driver.switch_to.default_content()

    def switch_to_window(self, window):
        """
        Switches the driver's context to the specified window or tab.

        Args:
            window (str): The handle of the window or tab to switch to.
        """
        self.driver.switch_to.window(window)

    def get_window_handles(self):
        """
        Retrieves a list of window handles currently opened by the WebDriver.

        Returns:
            list: A list of strings, each representing a handle to an open window or tab.
        """
        return self.driver.window_handles

    def get_page_title(self):
        """
        Retrieves the title of the current page.

        Returns:
            str: The title of the current page.
        """
        return self.driver.title
