import pytest
from selenium.webdriver.common.by import By

from ..pages.checkboxes_page import Checkboxes


class CheckboxesLocators:
    """
    Locators and URLs used for testing checkboxes and related elements on different pages.
    """

    URL_1 = "https://parsinger.ru/selenium/5.9/7/index.html"
    URL_2 = "https://parsinger.ru/selenium/5.9/6/index.html"
    URL_3 = "https://parsinger.ru/selenium/5.9/5/index.html"
    URL_4 = "https://parsinger.ru/selenium/5.9/4/index.html"
    URL_5 = "http://parsinger.ru/expectations/4/index.html"
    URL_6 = "https://parsinger.ru/selenium/5.5/5/1.html"

    CHECKBOX = (By.TAG_NAME, 'input')
    CONTAINERS = (By.CLASS_NAME, 'container')
    CHECK_BTN = (By.XPATH, 'button')
    RESULT = (By.XPATH, '//*[@id="result"]|//*[@class="message"]|//*[@id="message"]')
    CLOSE_ADD_BTN = (By.XPATH, "//*[@id='close_ad']|//*[@id='ad']//*[@class='close']")
    BOX_BTN = (By.CSS_SELECTOR, '.box button')
    CLICK_BTN = (By.ID, "btn")
    DIV_CONTAINERS = (By.XPATH, '//*[@id="main-container"]/div')
    SPAN = (By.XPATH, 'span')
    DROPDOWN = lambda x: (By.XPATH, f"span[contains(text(), '{x}')]/../select")
    OPTION = lambda x: (By.XPATH, f"span[contains(text(), '{x}')]/..//option[@value='{x}']")
    COLOR_BTN = lambda x: (By.XPATH, f"span[contains(text(), '{x}')]/..//button[@data-hex='{x}']")
    COLOR_CHECKBOX = (By.XPATH, "input[@type='checkbox']")
    INPUT_FIELD = (By.XPATH, "input[@type='text']")

    CHECK_ALL_ELS_BTN = (By.XPATH, "//button[contains(text(), 'Проверить все элементы')]")

    @staticmethod
    def dynamic_checkbox_locator(position):
        """
        Returns an XPath locator for a checkbox element based on the provided position.

        Args:
            position (int): The position index of the checkbox.

        Returns:
            tuple: A tuple containing the By.XPATH strategy and the dynamically generated XPath.
        """
        return By.XPATH, f'//div[@data-index="{position}"]'


class TestCheckboxes:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup fixture to initialize the Checkboxes page object.

        Args:
            driver: WebDriver instance used for interacting with the browser.
        """
        self.page = Checkboxes(driver)

    def test_highlighted_world(self):
        """
        Test method to interact with checkboxes and buttons based on their highlighted state.

        Steps:
        1. Open the specified URL.
        2. Identify all container elements containing checkboxes.
        3. For each container, check if the checkbox text is highlighted.
        4. If highlighted, click the corresponding button.
        5. Assert the final message displayed on the page to verify success.
        """
        self.page.open_url(CheckboxesLocators.URL_1)
        containers = self.page.find_elements(CheckboxesLocators.CONTAINERS)
        for container in containers:
            if self.page.wait_element_to_be_selected(container.find_element(*CheckboxesLocators.CHECKBOX)):
                container.find_element(*CheckboxesLocators.CHECK_BTN).click()

        assert self.page.find_element(CheckboxesLocators.RESULT).text == 'GFD9-3SV0-3280-WEZC-23UN-Q921-3G5D'

    def test_flashing_checkbox(self):
        """
        Test method to interact with a flashing checkbox and verify the result.

        Steps:
        1. Open the specified URL.
        2. Wait until the checkbox is selected.
        3. Click the corresponding button.
        4. Assert the final message displayed on the page to verify success.
        """
        self.page.open_url(CheckboxesLocators.URL_2)
        self.page.wait_element_to_be_selected(self.page.find_element(CheckboxesLocators.CHECKBOX))
        self.page.find_element(CheckboxesLocators.CHECK_BTN).click()
        assert self.page.find_element(CheckboxesLocators.RESULT).text == "34D0-3SCV-SCM0-654R-DVM9-42IU"

    def test_annoying_add(self):
        """
        Test method to handle an annoying advertisement and interact with checkboxes.

        Steps:
        1. Open the specified URL.
        2. Iterate over all checkbox positions.
        3. For each position, click the checkbox and close the advertisement.
        4. Retrieve and store the text associated with each checkbox.
        5. Assert that the concatenated secret code matches the expected value.
        """
        self.page.open_url(CheckboxesLocators.URL_3)
        secret = []
        for position in range(9):
            self.page.click(CheckboxesLocators.dynamic_checkbox_locator(position))
            self.page.click(CheckboxesLocators.CLOSE_ADD_BTN)
            text = ''
            while text == '':
                text = self.page.find_element(CheckboxesLocators.dynamic_checkbox_locator(position)).text
            secret.append(text)
        assert '-'.join(secret) == 'F34S-FFS3-56FGH-LKJ0-2E9D-440D-4Q0D-230S-D120'

    def test_close_add(self):
        """
        Test method to close an advertisement and interact with elements on the page.

        Steps:
        1. Open the specified URL.
        2. Wait until the close button for the ad is clickable and then click it.
        3. Wait until the ad is invisible.
        4. Click the box button.
        5. Assert that the result message matches the expected value.
        """
        self.page.open_url(CheckboxesLocators.URL_4)
        self.page.wait_for_element_to_be_clickable(CheckboxesLocators.CLOSE_ADD_BTN).click()
        self.page.wait_for_element_to_be_invisible(CheckboxesLocators.CLOSE_ADD_BTN)
        self.page.wait_for_element_to_be_clickable(CheckboxesLocators.BOX_BTN).click()
        assert (self.page.wait_for_element_to_be_visible(CheckboxesLocators.RESULT).text ==
                'FS03-R9R3-SVV9-3P05-DSS1-01VI')

    def test_secret_title(self):
        """
        Test method to verify the secret title of the page.

        Steps:
        1. Open the specified URL.
        2. Click the button on the page.
        3. Assert that the page title contains the expected partial text.
        """
        partial_title = 'JK8HQ'
        self.page.open_url(CheckboxesLocators.URL_5)
        self.page.wait_for_element_to_be_clickable(CheckboxesLocators.CLICK_BTN).click()
        assert self.page.wait_title_contain_text(partial_title, poll_frequency=0.05)

    def test_interact_with_checkboxes(self):
        """
        Test method to interact with checkboxes, dropdowns, and buttons on the Checkbox Page.

        The test iterates through each element in the main container, selects the dropdown option,
        clicks the associated button, checks the checkbox, enters text, and submits the form.
        Finally, it verifies the result by checking the alert text.

        Asserts:
            N/A: This test is focused on output rather than assertions.
        """

        self.page.open_url(CheckboxesLocators.URL_6)
        elements = self.page.find_elements(CheckboxesLocators.DIV_CONTAINERS)

        for el in elements:
            text = el.find_element(*CheckboxesLocators.SPAN).text
            el.find_element(*CheckboxesLocators.DROPDOWN(text)).click()
            el.find_element(*CheckboxesLocators.OPTION(text)).click()
            el.find_element(*CheckboxesLocators.COLOR_BTN(text)).click()
            el.find_element(*CheckboxesLocators.COLOR_CHECKBOX).click()
            el.find_element(*CheckboxesLocators.INPUT_FIELD).send_keys(text)
            el.find_element(*CheckboxesLocators.CHECK_BTN).click()

        self.page.click(CheckboxesLocators.CHECK_ALL_ELS_BTN)

        assert self.page.get_alert_text() == '532344023354423035345134503454510'
