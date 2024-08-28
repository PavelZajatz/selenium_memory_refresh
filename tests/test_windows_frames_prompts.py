import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from ..pages.windows_frames_prompts_page import WindowsFramesPromptsPage
from selenium.webdriver.support import expected_conditions as EC


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


class TestWindowsFramesPromptsPage:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup fixture to initialize the WindowsFramesPromptsPage page object.

        Args:
            driver: WebDriver instance used for interacting with the browser.
        """
        self.page = WindowsFramesPromptsPage(driver)

    def test_iframe(self):
        """
            Test method to interact with iframes on the page and retrieve a secret code.

            Steps:
            1. Navigate to the URL defined in `WFPsPageLocators.URL_1`.
            2. Locate all iframes using the locator specified in `WFPsPageLocators.IFRAME`.
            3. For each iframe:
               - Switch to the iframe using `driver.switch_to.frame()`.
               - Click the button located by `WFPsPageLocators.PRESS_ME_BTN`.
               - Get the text from the iframe using `WFPsPageLocators.IFRAME_TXT`.
               - Switch back to the default content using `driver.switch_to.default_content()`.
               - Enter the retrieved text into the input field located by `WFPsPageLocators.INPUT`.
               - Click the button located by `WFPsPageLocators.CHECK_BTN`.
               - Try to get the text from any alert using `self.page.try_to_get_text_from_alert()`.
               - If a secret code is found, break the loop.
            4. Assert that the retrieved secret code equals `'FD79-32DJ-79XB-124S-P3DX-2456-DFB-DSA9'`.

            Asserts:
                - Asserts that the retrieved secret code is equal to `'FD79-32DJ-79XB-124S-P3DX-2456-DFB-DSA9'`.

            Raises:
                - AssertionError: If the retrieved secret code does not match the expected value.
            """
        self.page.open_url(WFPsPageLocators.URL_1)

        for iframe in self.page.find_elements(WFPsPageLocators.IFRAME):
            self.page.driver.switch_to.frame(iframe)
            self.page.click(WFPsPageLocators.PRESS_ME_BTN)
            pwd = self.page.get_text(WFPsPageLocators.IFRAME_TXT)
            self.page.driver.switch_to.default_content()
            self.page.enter_text(WFPsPageLocators.INPUT, pwd)
            self.page.click(WFPsPageLocators.CHECK_BTN)
            secret = self.page.try_to_get_text_from_alert()
            if secret:
                break
        assert secret == 'FD79-32DJ-79XB-124S-P3DX-2456-DFB-DSA9'

    def test_count_title_ints(self):
        """
        Test method to calculate the sum of integers from the titles of newly opened windows.

        Steps:
        1. Navigate to the URL defined in `WFPsPageLocators.URL_2`.
        2. Locate all input fields (buttons) using the locator specified in `WFPsPageLocators.INPUT_FLD`.
        3. For each button:
           - Click the button.
           - Switch to the newly opened window.
           - Convert the window title to an integer and add it to the total sum.
           - Switch back to the original window.
        4. Verify that the total sum of integers from the window titles equals the expected value.

        Asserts:
            - Asserts that the total sum of integers from the window titles is equal to `77725787998028643152187739088279`.

        Raises:
            - AssertionError: If the total sum does not match the expected value.
        """
        total = 0
        self.page.open_url(WFPsPageLocators.URL_2)
        buttons = self.page.find_elements(WFPsPageLocators.INPUT_FLD)
        for button in buttons:
            button.click()
            self.page.driver.switch_to.window(self.page.driver.window_handles[-1])
            total += int(self.page.driver.title)
            self.page.driver.switch_to.window(self.page.driver.window_handles[0])

        assert total == 77725787998028643152187739088279

    @pytest.mark.parametrize("x, y, expected_result",
                             [
                                 (516, 270, ''),
                                 (648, 300, ''),
                                 (680, 340, ''),
                                 (701, 388, ''),
                                 (730, 400, ''),
                                 (750, 421, ''),
                                 (805, 474, ''),
                                 (820, 505, ''),
                                 (855, 557, ''),
                                 (890, 600, ''),
                                 (955, 600, '9874163854135461654'),
                                 (1000, 1000, ''),
                             ])
    def test_window_size(self, x, y, expected_result):
        """
        Test method to validate the behavior of the page when resizing the browser window.

        This test:
        1. Opens the specified URL.
        2. Retrieves inner and outer dimensions of the window.
        3. Calculates target dimensions to set the browser window size.
        4. Sets the window size and checks if the result text matches the expected value.

        Args:
            x (int): The width to test.
            y (int): The height to test.
            expected_result (str): The expected result text to be present in the element.
        """
        self.page.open_url(WFPsPageLocators.URL_3)

        inner_width, inner_height = self.page.get_inner_size(WFPsPageLocators.WIDTH, WFPsPageLocators.HEIGHT)
        outer_width, outer_height = self.page.get_outer_size()

        target_width = outer_width - inner_width
        target_height = outer_height - inner_height

        self.page.set_window_size(x + target_width, y + target_height)

        result_text = self.page.wait_for_text_to_be_present_in_element(WFPsPageLocators.RESULT, expected_result)
        assert result_text == expected_result

    def test_find_correct_pin(self):
        """
        Tests the functionality of finding the correct PIN code on a webpage.

        This method navigates to the specified URL, retrieves all possible PIN codes from the page, and iteratively attempts
        to input each PIN code into a prompt until the correct one is found. The test asserts that the correct PIN is
        identified by comparing the extracted secret code with the expected value.

        Steps:
        1. Open the URL specified by `WFPsPageLocators.URL_4`.
        2. Find all elements representing PIN codes using the locator `WFPsPageLocators.PINS`.
        3. Iterate over each PIN code:
            - Click on the input field located by `WFPsPageLocators.INPUT_FLD`.
            - Enter the PIN code into the alert prompt.
            - Accept the alert.
            - Retrieve the text from the result field located by `WFPsPageLocators.RESULT`.
            - Break the loop if the result does not indicate an incorrect PIN code.
        4. Assert that the correct PIN code produces the expected secret value `'1261851212132345456274632'`.

        Raises:
            AssertionError: If the correct secret code is not found.
        """
        self.page.open_url(WFPsPageLocators.URL_4)
        pins = self.page.find_elements(WFPsPageLocators.PINS)
        for pin in pins:
            pin_code = pin.text
            self.page.click(WFPsPageLocators.INPUT_FLD)
            prompt = self.page.driver.switch_to.alert
            prompt.send_keys(pin_code)
            prompt.accept()
            secret = self.page.get_text(WFPsPageLocators.RESULT)
            if secret != 'Неверный пин-код':
                break

        assert secret == '1261851212132345456274632'
