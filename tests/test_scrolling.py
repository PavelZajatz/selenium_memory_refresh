import pytest
from ..pages.cookies_page import CookiesPage


class CookiesLocators:
    """
    Locators and URLs used for testing Cookies.
    """

    URL_1 = "https://parsinger.ru/methods/3/index.html"


class TestCookies:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup fixture to initialize the CookiesPage object.

        Args:
            driver: WebDriver instance used for interacting with the browser.
        """
        self.page = CookiesPage(driver)

    def test_cookies_collect(self):
        """
        Tests the collection and summation of specific cookies based on their names.

        This test navigates to the specified URL and collects all cookies set by the webpage.
        It then filters the cookies to find those whose names end with an even number, sums their values,
        and asserts that the total sum matches the expected value.

        Steps:
        1. Open the URL specified by `CookiesLocators.URL_1`.
        2. Retrieve all cookies set by the webpage.
        3. Filter cookies based on whether their names end with an even number.
        4. Sum the values of the filtered cookies.
        5. Assert that the total sum matches the expected value.

        Raises:
            AssertionError: If the total sum does not match the expected value.
        """
        self.page.open_url(CookiesLocators.URL_1)
        total = self.page.sum_even_cookies()
        assert total == 1962101
