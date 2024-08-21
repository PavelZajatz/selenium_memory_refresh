import pytest
from selenium.webdriver.common.by import By
from ..common.base_methods import BasePage

"""
Slider Movement and the Secret Code

Welcome to the world of sliders and precision, where every action you take impacts the outcome. This is not just a 
task of moving sliders; it’s a challenge that requires attention, precision, and an eye for detail.

Task:

World of Sliders: Enter the site using Selenium, and you’ll find yourself in a world where 10 sliders await your 
attention. They are like musicians in an orchestra, each needing to be tuned precisely to play a harmonious melody.

Precision Task: Your mission is to carefully and accurately move each slider to the position indicated in the right 
column.

Message Retrieval: Once all the sliders are in their correct positions, a message will appear on the screen. This 
message is the key to solving your task, a secret code that will open up new horizons for you.

Purpose of the Task: By obtaining the secret code, you won’t just complete the task. You will prove that you have the 
precision of a jeweler, the patience, and the ability to see things through to the end, despite any challenges.
"""

# URL of the webpage containing the sliders
URL = "https://parsinger.ru/selenium/5.10/6/index.html"

# Locator for the container that holds all the sliders
SLIDERS_CONTAINER = (By.CLASS_NAME, 'slider-container')

# Locator for the current position input element of each slider
CUR_POS_ELEMENT = (By.TAG_NAME, 'input')

# Locator for the element displaying the target position for each slider
NEW_POS = (By.CLASS_NAME, 'target-value')

# Locator for the element displaying the final message after sliders are correctly positioned
MESSAGE = (By.ID, 'message')


class TestSlidersMovement:
    """
    Test class for handling the slider movements on the webpage.
    The objective is to move each slider to its target position and retrieve the secret message.
    """

    @pytest.fixture(autouse=True)
    def driver_parse(self, driver):
        """
        Automatically sets up the driver for use in the test methods.

        Args:
            driver (WebDriver): The Selenium WebDriver instance for interacting with the browser.
        """
        self.page = BasePage(driver)

    def test_sliders_movement(self):
        """
        Test method to move all sliders to their target positions and verify the resulting message.

        Steps:
        1. Open the target URL.
        2. Identify all sliders on the page.
        3. For each slider, move it to the target position specified in the right column.
        4. Trigger the necessary events to ensure the position is updated.
        5. Verify that the displayed message matches the expected secret code.
        """
        self.page.open_url(URL)
        sliders = self.page.find_elements(SLIDERS_CONTAINER)

        for slider in sliders:
            cur_pos_element = slider.find_element(*CUR_POS_ELEMENT)
            new_pos = slider.find_element(*NEW_POS).text

            # Move the slider to the new position
            self.page.execute_script(
                "arguments[0].setAttribute('value', arguments[1]);", cur_pos_element, new_pos)
            self.page.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", cur_pos_element)
            self.page.execute_script(
                "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", cur_pos_element)

        # Verify the secret code is correct
        message = self.page.wait_for_element_to_be_present(MESSAGE)
        assert message.text == '3F9D-DVB0-EH46-96VB-JHJ5-34UK-2SSF-JKG0'
