from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from ..helpers.allure_helper import step
from ..common.base_methods import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WFPsPageLocators:
    """
    Locators and URLs used for testing windows and related elements on different pages.
    """

    URL_1 = "https://parsinger.ru/selenium/5.8/5/index.html"
    URL_2 = "http://parsinger.ru/blank/3/index.html"
    URL_3 = "http://parsinger.ru/window_size/2/index.html"
    URL_4 = "https://parsinger.ru/selenium/5.8/3/index.html"
    IFRAME = (By.XPATH, "//iframe[contains(@id, 'iframe')]")
    PRESS_ME_BTN = (By.TAG_NAME, 'button')
    IFRAME_TXT = (By.TAG_NAME, 'p')
    INPUT = (By.XPATH, '//input[@id="guessInput"]')
    INPUT_FLD = (By.TAG_NAME, 'input')
    CHECK_BTN = (By.XPATH, '//button[@id="checkBtn"]')
    RESULT = (By.ID, 'result')
    WIDTH = (By.ID, 'width')
    HEIGHT = (By.ID, 'height')
    PINS = (By.XPATH, "//span[@class='pin']")


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

    @step
    def get_secret_from_alert(self):
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

    @step
    def get_inner_size(self):
        """
        Retrieves the inner width and height of the browser window from specified elements.

        Returns:
            tuple: (inner_width, inner_height)
        """
        inner_width = int(self.driver.find_element(*WFPsPageLocators.WIDTH).text.split(": ")[1])
        inner_height = int(self.driver.find_element(*WFPsPageLocators.HEIGHT).text.split(": ")[1])
        return inner_width, inner_height

    @step
    def get_outer_size(self):
        """
        Retrieves the outer width and height of the browser window.

        Returns:
            tuple: (outer_width, outer_height)
        """
        size = self.driver.get_window_size()
        return size.get('width'), size.get('height')

    @step
    def set_window_size(self, width, height):
        """
        Sets the browser window size.

        Args:
            width (int): The width to set for the window.
            height (int): The height to set for the window.
        """
        self.driver.set_window_size(width, height)

    @step
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

    @step
    def switch_to_alert(self):
        """
        Switches the driver's context to the currently active alert.

        Returns:
            Alert: The active alert object to interact with.
        """
        return self.driver.switch_to.alert

    @step
    def switch_to_alert_and_send_keys(self, key):
        """
        Switches to the active alert, sends the specified keys, and accepts the alert.

        Args:
            key (str): The keys to send to the alert's input field.
        """
        prompt = self.switch_to_alert()
        prompt.send_keys(key)
        prompt.accept()

    @step
    def switch_to_iframe(self, iframe):
        """
        Switches the driver's context to the specified iframe.

        Args:
            iframe (str or WebElement): The iframe to switch to, identified by name, index, or WebElement.
        """
        self.driver.switch_to.frame(iframe)

    @step
    def switch_to_default_content(self):
        """
        Switches the driver's context back to the default content, i.e., the main document.

        Use this method to exit an iframe or other nested context and return to the main document.
        """
        self.driver.switch_to.default_content()

    @step
    def switch_to_window(self, window):
        """
        Switches the driver's context to the specified window or tab.

        Args:
            window (str): The handle of the window or tab to switch to.
        """
        self.driver.switch_to.window(window)

    @step
    def get_window_handles(self):
        """
        Retrieves a list of window handles currently opened by the WebDriver.

        Returns:
            list: A list of strings, each representing a handle to an open window or tab.
        """
        return self.driver.window_handles

    @step
    def get_page_title(self):
        """
        Retrieves the title of the current page.

        Returns:
            str: The title of the current page.
        """
        return self.driver.title

    @step
    def click_press_me_button(self):
        """
        Click the 'Press Me' button inside the iframe.
        """
        self.click(WFPsPageLocators.PRESS_ME_BTN)

    @step
    def get_password_from_iframe(self):
        """
        Retrieve the text from the element inside the iframe.

        Returns:
            str: The text retrieved from the iframe element.
        """
        return self.get_text_from_element(WFPsPageLocators.IFRAME_TXT)

    @step
    def enter_password(self, password):
        """
        Enter the specified password into the input field.

        Args:
            password (str): The password to enter.
        """
        self.enter_text(WFPsPageLocators.INPUT, password)

    @step
    def click_check_button(self):
        """
        Click the 'Check' button to validate the entered password.
        """
        self.click(WFPsPageLocators.CHECK_BTN)

    @step
    def find_iframes(self):
        """
        Find all iframe elements on the page.

        Returns:
            list: A list of WebElement representing iframes.

        Raises:
            NoSuchElementException: If no iframes are found on the page.
        """
        iframes = self.find_elements(WFPsPageLocators.IFRAME)
        if not iframes:
            raise NoSuchElementException("No iframes found on the page.")
        return iframes

    @step
    def find_buttons(self):
        """
        Find all input fields (buttons) on the page.

        Returns:
            list: A list of WebElement objects representing the buttons.
        """
        return self.find_elements(WFPsPageLocators.INPUT_FLD)

    @step
    def click_button(self, button):
        """
        Click on the specified button.

        Args:
            button (WebElement): The WebElement representing the button to click.
        """
        button.click()

    @step
    def get_current_window_handle(self):
        """
        Get the handle of the current window.

        Returns:
            str: The handle of the current window.
        """
        return self.get_window_handles()[0]

    @step
    def get_new_window_handle(self, original_window_handle):
        """
        Get the handle of the newly opened window.

        Args:
            original_window_handle (str): The handle of the original window.

        Returns:
            str: The handle of the newly opened window.
        """
        handles = self.get_window_handles()
        new_window_handle = [handle for handle in handles if handle != original_window_handle][-1]
        return new_window_handle

    @step
    def switch_back_to_original_window(self, original_window_handle):
        """
        Switch back to the original window.

        Args:
            original_window_handle (str): The handle of the original window.
        """
        self.switch_to_window(original_window_handle)

    @step
    def get_result_text(self, expected_text, timeout=10):
        """
        Retrieve the result text from the result element on the page after waiting for the specified text to be present.

        Args:
            expected_text (str): The text to wait for before retrieving the result.
            timeout (int): The maximum time to wait for the text to appear (default is 10 seconds).

        Returns:
            str: The result text that is present in the result element.

        Raises:
            TimeoutException: If the expected text is not found within the timeout period.
        """
        return self.wait_for_text_to_be_present_in_element(WFPsPageLocators.RESULT, expected_text, timeout)

    @step
    def get_all_pin_elements(self):
        """
        Retrieves all elements representing PIN codes on the page.

        :return: A list of WebElements representing PIN codes.
        """
        return self.driver.find_elements(*WFPsPageLocators.PINS)

    @step
    def enter_pin_in_alert(self, pin_code):
        """
        Enters the given PIN code into the alert prompt and accepts it.

        :param pin_code: The PIN code to be entered.
        """
        alert = self.driver.switch_to.alert
        alert.send_keys(pin_code)
        alert.accept()

    @step
    def find_correct_pin(self):
        """
        Iterates through the PIN codes and returns the correct one.

        :return: The correct PIN code or None if not found.
        """
        pins = self.get_all_pin_elements()
        for pin in pins:
            pin_code = pin.text
            self.click(WFPsPageLocators.INPUT_FLD)
            self.switch_to_alert_and_send_keys(pin_code)
            secret = self.get_text_from_element(WFPsPageLocators.RESULT)
            if secret != 'Неверный пин-код':
                return secret
        return None
