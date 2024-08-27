from ..common.base_methods import BasePage


class Checkboxes(BasePage):
    """
    Page class for handling checkboxes related actions.
    """

    def __init__(self, driver):
        """
        Initializes the Checkboxes with the WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        """
        super().__init__(driver)
