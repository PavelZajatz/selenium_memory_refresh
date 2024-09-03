import pytest

from ..pages.windows_frames_prompts_page import WindowsFramesPromptsPage, WFPsPageLocators


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
            """
        self.page.open_url(WFPsPageLocators.URL_1)

        secret_code = None
        for iframe in self.page.find_iframes():
            self.page.switch_to_iframe(iframe)
            self.page.click_press_me_button()
            pwd = self.page.get_password_from_iframe()
            self.page.switch_to_default_content()
            self.page.enter_password(pwd)
            self.page.click_check_button()
            secret_code = self.page.get_secret_from_alert()
            if secret_code:
                break
        assert secret_code == 'FD79-32DJ-79XB-124S-P3DX-2456-DFB-DSA9', \
            f"Expected secret code be 'FD79-32DJ-79XB-124S-P3DX-2456-DFB-DSA9', but got {secret_code}"''

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
        """
        expected_total = 77725787998028643152187739088279
        total = 0
        self.page.open_url(WFPsPageLocators.URL_2)
        buttons = self.page.find_buttons()
        original_window_handle = self.page.get_current_window_handle()

        for button in buttons:
            self.page.click_button(button)
            new_window_handle = self.page.get_new_window_handle(original_window_handle)
            self.page.switch_to_window(new_window_handle)
            total += int(self.page.get_page_title())
            self.page.switch_back_to_original_window(original_window_handle)

        assert total == expected_total, f"Expected total: {expected_total}, but got: {total}"

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
        """
        self.page.open_url(WFPsPageLocators.URL_3)

        inner_width, inner_height = self.page.get_inner_size()
        outer_width, outer_height = self.page.get_outer_size()

        target_width = outer_width - inner_width
        target_height = outer_height - inner_height

        self.page.set_window_size(x + target_width, y + target_height)

        result_text = self.page.get_result_text(expected_result)
        assert result_text == expected_result, f"Expected result: {expected_result}, but got: {result_text}"

    def test_find_correct_pin(self):
        """
        Tests the functionality of finding the correct PIN code on a webpage.

        This method navigates to the specified URL, retrieves all possible PIN codes from the page,
        and iteratively attempts
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
        secret = self.page.find_correct_pin()

        assert secret == '1261851212132345456274632', f"Failed to find the correct PIN code, found - {secret}"
