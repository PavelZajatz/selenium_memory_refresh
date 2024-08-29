from ..common.base_methods import BasePage


class CookiesPage(BasePage):
    """
    Page class for handling CookiesPage related actions.
    """

    def __init__(self, driver):
        """
        Initializes the CookiesPage with the WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        """
        super().__init__(driver)

    def get_cookies(self):
        """
        Retrieves all cookies from the browser.

        Returns:
            A list of dictionaries, each representing a cookie.
        """
        return self.driver.get_cookies()

    def add_cookies(self, cookies):
        """
        Adds a list of cookies to the browser session.

        Args:
            cookies (list): A list of dictionaries, where each dictionary represents a cookie with
                            'name' and 'value' keys.
        """
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def delete_all_cookies(self):
        """Deletes all cookies from the current browser session."""
        self.driver.delete_all_cookies()

    def add_cookie(self, cookie):
        """
        Adds a single cookie to the browser session.

        Args:
            cookie (dict): A dictionary representing a cookie with 'name' and 'value' keys.
        """
        self.driver.add_cookie(cookie)

    def sum_even_cookies(self):
        """
        Sums the values of cookies with even numbers in their names.

        Returns:
            The total sum of cookie values that meet the criteria.
        """
        total = 0
        cookies = self.get_cookies()
        for cookie in cookies:
            if int(cookie['name'].split("_")[-1]) % 2 == 0:
                total += int(cookie['value'])
        return total

    def find_max_expiry_cookie_url(self, urls):
        """
        Finds the URL with the cookie that has the maximum expiry value.

        Args:
            urls: A list of URLs to visit.

        Returns:
            The URL corresponding to the cookie with the maximum expiry value.
        """
        max_expiry_value = 0
        max_expiry_link = None

        for link in urls:
            self.open_url(link)
            cookies = self.get_cookies()
            for cookie in cookies:
                if 'expiry' in cookie:
                    expiry_value = cookie['expiry']
                    if expiry_value > max_expiry_value:
                        max_expiry_value = expiry_value
                        max_expiry_link = link

        return max_expiry_link

    def sum_secret_cookies(self):
        """
        Sums the values of cookies that contain 'secret_cookie_' in their names.

        Returns:
            The total sum of the values of these cookies.
        """
        total = 0
        cookies = self.get_cookies()
        for cookie in cookies:
            if 'secret_cookie_' in cookie['name']:
                total += int(cookie['value'])
        return total
