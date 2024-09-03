import pytest
from ..pages.checkboxes_page import Checkboxes, CheckboxesLocators


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
        containers = self.page.find_containers()
        for container in containers:
            if self.page.is_checkbox_highlighted(container):
                self.page.click_button_in_container(container)
        assert self.page.get_result_text() == 'GFD9-3SV0-3280-WEZC-23UN-Q921-3G5D'

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
        self.page.wait_for_checkbox_selection()
        self.page.click_flash_checkbox()
        assert self.page.get_result_text() == "34D0-3SCV-SCM0-654R-DVM9-42IU"

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
            self.page.click_dynamic_checkbox(position)
            self.page.close_advertisement()
            text = self.page.get_dynamic_checkbox_text(position)
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
        self.page.close_advertisement()
        self.page.click_box_button()
        assert self.page.get_result_text() == 'FS03-R9R3-SVV9-3P05-DSS1-01VI'

    @pytest.mark.flaky(retries=2)
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
        self.page.click_click_button()
        self.page.wait_for_page_title(partial_title)

    def test_interact_with_checkboxes(self):
        """
        Test method to interact with checkboxes, dropdowns, and buttons on the Checkbox Page.

        Steps:
        1. Open the specified URL.
        2. Iterate through each element in the main container.
        3. Select the dropdown option, click the associated button, check the checkbox, enter text, and submit the form.
        4. Click the 'Check All Elements' button.
        5. Verify the result by checking the alert text.
        """
        self.page.open_url(CheckboxesLocators.URL_6)
        self.page.interact_with_elements()
        self.page.click_check_all_elements_button()
        assert self.page.get_alert_text() == '532344023354423035345134503454510'
