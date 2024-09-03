from selenium.webdriver.common.by import By

from ..common.base_methods import BasePage
from ..helpers.allure_helper import step


class CookiesLocators:
    """
    Locators and URLs used for testing Cookies.
    """

    URL_1 = "https://parsinger.ru/methods/3/index.html"
    URL_2 = "https://parsinger.ru/methods/5/index.html"
    URL_3 = "https://parsinger.ru/selenium/5.6/1/index.html"
    A_TAG = (By.TAG_NAME, 'a')
    RESULT = (By.ID, 'result')
    HACKERS = (By.CSS_SELECTOR, '.hackers')
    AGE = (By.ID, 'age')
    LANGUAGES = (By.CSS_SELECTOR, '#skillsList li')


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

    @step
    def get_cookies(self):
        """
        Retrieves all cookies from the browser.

        Returns:
            A list of dictionaries, each representing a cookie.
        """
        return self.driver.get_cookies()

    @step
    def add_cookies(self, cookies):
        """
        Adds a list of cookies to the browser session.

        Args:
            cookies (list): A list of dictionaries, where each dictionary represents a cookie with
                            'name' and 'value' keys.
        """
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    @step
    def delete_all_cookies(self):
        """Deletes all cookies from the current browser session."""
        self.driver.delete_all_cookies()

    @step
    def add_cookie(self, cookie):
        """
        Adds a single cookie to the browser session.

        Args:
            cookie (dict): A dictionary representing a cookie with 'name' and 'value' keys.
        """
        self.driver.add_cookie(cookie)

    @step
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

    @step
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

    @step
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

    @step
    def set_and_refresh(self, cookie):
        """
        Sets a cookie, refreshes the page, and updates the page state.

        This method first deletes all existing cookies in the browser, adds a new cookie provided
        as a parameter, and then refreshes the page to reflect the changes.

        Args:
            cookie (dict): A dictionary containing the cookie information to be added.

        Returns:
            None
        """
        self.delete_all_cookies()
        self.add_cookie(cookie)
        self.refresh_page()

    @step
    def get_hacker_info(self):
        """
        Retrieves the hacker's age and the number of programming languages listed on the page.

        This method extracts the text indicating the hacker's age and counts the number of elements
        representing programming languages.

        Returns:
            tuple: A tuple containing the age of the hacker (int) and the number of programming languages (int).
        """
        age_text = self.get_text_from_element(CookiesLocators.AGE)
        age = int(age_text.replace('Age: ', ''))
        languages_count = len(self.find_elements(CookiesLocators.LANGUAGES))
        return age, languages_count

    @step
    def find_youngest_hacker(self, cookies):
        """
        Identifies the cookie value of the youngest hacker with the most programming languages.

        This method iterates through a list of cookies, setting each one, and refreshing the page.
        It collects information on the hacker's age and the number of programming languages.
        Finally, it determines the youngest hacker and, among them, the one with the most languages.

        Args:
            cookies (list): A list of dictionaries, each representing a cookie to be added.

        Returns:
            str: The value of the cookie corresponding to the youngest hacker with the most programming languages.
        """
        hackers = []

        for cookie in cookies:
            self.set_and_refresh(cookie)
            age, languages = self.get_hacker_info()
            hackers.append({'age': age, 'languages': languages, 'value': cookie['value']})

        # Sort hackers by age
        sorted_hackers = sorted(hackers, key=lambda x: x['age'])
        # Filter out the youngest hackers
        youngest_hackers = [hacker for hacker in hackers if hacker['age'] == sorted_hackers[0]['age']]
        # Find the youngest hacker with the most languages
        result_value = sorted(youngest_hackers, key=lambda x: x['languages'], reverse=True)[0]['value']

        return result_value

    @step
    def get_all_urls(self):
        """
        Retrieves all URLs from anchor elements (`<a>`) on the page.

        This method finds all anchor tags on the page and extracts the `href` attribute
        to compile a list of URLs that will be checked for cookies with maximum expiry.

        Returns:
            list: A list of URLs found on the page.
        """
        hrefs = self.find_elements(CookiesLocators.A_TAG)
        return [item.get_attribute('href') for item in hrefs]

    @step
    def find_max_expiry_url(self, urls):
        """
        Finds the URL with the cookie that has the maximum expiry value.

        This method iterates through the provided URLs, visiting each one to check the
        cookies and identifying the URL associated with the cookie that has the highest expiry value.

        Args:
            urls (list): A list of URLs to be checked for cookies.

        Returns:
            str: The URL that corresponds to the cookie with the maximum expiry value.
        """
        return self.find_max_expiry_cookie_url(urls)

    @step
    def retrieve_result_text(self):
        """
        Retrieves the text from the 'result' element on the page.

        After navigating to the page with the maximum expiry cookie, this method extracts
        the text from the specified element, which is the final step in the test.

        Returns:
            str: The text contained within the 'result' element on the page.
        """
        return self.get_text_from_element(CookiesLocators.RESULT)
