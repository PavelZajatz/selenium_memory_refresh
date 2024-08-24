"""
A Throw at the Right Distance

Welcome to a virtual garden of wonders, filled with colorful plots and mysterious pieces, each searching for its
place in this world. Here, in this digital paradise, the laws of physics and space play by their own rules, and only
those who can understand their language will achieve success.

**World Unveiling:** Use Selenium to open the website.

**Mission of the Throw:** You have 8 pieces and 8 colorful plots at your disposal. Each plot has a unique
characteristic—the distance required to throw a piece so that it lands in its plot. Your task is to write a script
that will execute these throws with precision and attention to detail.

**Victory Code:** Once all the pieces are in their plots, a code will appear—a symbol of your success and task
completion. This code must be entered in the answer field to confirm your victory.
"""
import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from ..common.base_methods import BasePage

# URL of the target webpage
URL = "https://parsinger.ru/selenium/5.10/8/index.html"

# Locators for the pieces and ranges on the webpage
PIECE = (By.CLASS_NAME, 'piece')
RANGE = (By.CLASS_NAME, 'range')

# Locator for the message element that appears after all pieces are correctly placed
MESSAGE = (By.ID, 'message')


class TestThrowAtTheRightDistance:
    """
    Test class for automating the process of moving pieces to their designated plots on a webpage.
    The objective is to ensure that all pieces are correctly placed, triggering a secret message display.
    """

    @pytest.fixture(autouse=True)
    def driver_parse(self, driver):
        """
        Fixture to automatically set up the Selenium WebDriver instance for the test methods.

        This method initializes the `BasePage` instance with the provided WebDriver.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used for interacting with the browser.
        """
        self.page = BasePage(driver)

    def test_throw_at_the_right_distance(self):
        """
        Test method to automate the placement of all pieces into their respective plots on the webpage.

        The process involves:
        1. Opening the specified URL.
        2. Locating all the pieces and their corresponding target plots on the page.
        3. Calculating the required distance for each piece to reach its target.
        4. Move each piece to its correct position.
        5. Verifying that a success message (secret code) is displayed once all pieces are correctly placed.

        The test is considered successful if the expected message is displayed.
        """
        self.page.open_url(URL)
        action = ActionChains(self.page.driver)
        pieces = self.page.find_elements(PIECE)
        ranges = {Color.from_string(
            i.value_of_css_property('background-color')): i for i in self.page.find_elements(RANGE)}

        for i in range(1, len(pieces) + 1):
            offset_el = ranges[Color.from_string(pieces[-i].value_of_css_property('background-color'))]
            offset = offset_el.find_element(By.TAG_NAME, 'p').text
            offset = offset.split(': ')[1].replace("px", "")
            action.click_and_hold(pieces[-i]).move_by_offset(offset, 0).perform()
        time.sleep(2)
        message = self.page.wait_for_text_to_be_present_in_element(MESSAGE,
                                                                   'GD60-34JX-354F-3HJC-NXC0-54KO-W3B1-2DFH-23JG')
        assert message
