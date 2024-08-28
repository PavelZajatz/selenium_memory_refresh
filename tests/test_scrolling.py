import pytest
from selenium.webdriver.common.by import By

from ..pages.scrolling_page import ScrollingPage


class ScrollingLocators:
    """
    Locators and URLs used for scrolling testing.
    """
    URL_1 = "https://parsinger.ru/selenium/5.7/4/index.html"
    CHECKBOX = (By.TAG_NAME, 'input')
    MAIN_CONTAINER = (By.ID, "main_container")
    NEXT_DIV = (By.XPATH, "./following-sibling::div")
    DIV = (By.TAG_NAME, "div")
    ALERT_BUTTON = (By.CLASS_NAME, 'alert_button')

    URL_2 = "http://parsinger.ru/infiniti_scroll_3/"
    SCROLL_CONTAINER = lambda i: (By.XPATH, f"//div[@class='scroll-container_{i}']")
    SPAN = (By.XPATH, "span[starts-with(@id, '__InfiScroll_')]")
    LAST_SPAN_CLASS = "last-of-list"
    FOLLOWING_SPAN = (By.XPATH, "./following-sibling::span")

    URL_3 = "http://parsinger.ru/infiniti_scroll_2/"
    SCROLL_CONTAINER_ID = (By.ID, "scroll-container")
    PARAGRAPH_TAG = (By.TAG_NAME, "p")
    FOLLOWING_P = (By.XPATH, "./following-sibling::p")


class TestScrolling:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup fixture to initialize the ScrollingPage object.

        Args:
            driver: WebDriver instance used for interacting with the browser.
        """
        self.page = ScrollingPage(driver)

    def test_infinity_scrolling(self):
        """
        Tests the functionality of infinite scrolling and interaction with dynamically loaded elements on the webpage.

        This test navigates to the specified URL and interacts with checkboxes inside a scrolling container.
        It iterates over checkboxes in each dynamically loaded div, clicking only those with even values.
        The process continues until 99 div elements have been loaded, after which the test asserts that the
        correct alert text is displayed.
        """
        self.page.open_url(ScrollingLocators.URL_1)

        counter = 0
        spans = [self.page.find_element(ScrollingLocators.MAIN_CONTAINER).find_element(*ScrollingLocators.DIV)]

        # Process the checkboxes in the first div
        self.page.click_even_checkboxes(spans[0], ScrollingLocators.CHECKBOX)

        # Continue scrolling and interacting with elements
        while True:
            next_span = self.page.get_next_span(spans[-1], ScrollingLocators.NEXT_DIV)
            self.page.click_even_checkboxes(next_span, ScrollingLocators.CHECKBOX)
            self.page.scroll_into_view(next_span)
            spans.append(next_span)
            counter += 1

            if counter == 99:
                break

        # Click the alert button and verify the alert text
        self.page.click(ScrollingLocators.ALERT_BUTTON)
        alert_text = self.page.get_alert_text()
        assert alert_text == '5402f04236450f263540jk406504l506'

    @pytest.mark.skip
    def test_collect_and_sum_spans(self):
        """
        Tests the collection and summation of text values from spans within multiple scrollable containers.

        This test navigates to a specific URL and iterates through 5 scrollable containers.
        It collects all spans in each container, sums their text values, and asserts that the final sum matches the expected value.
        """
        self.page.open_url(ScrollingLocators.URL_2)

        total_sum = 0

        for i in range(1, 6):
            container_locator = ScrollingLocators.SCROLL_CONTAINER(i)
            spans = self.page.collect_spans(container_locator, ScrollingLocators.SPAN,
                                            ScrollingLocators.LAST_SPAN_CLASS, ScrollingLocators.FOLLOWING_SPAN)
            sum_i = sum(int(span.text) for span in spans)
            total_sum += sum_i

        assert total_sum == 159858750

    @pytest.mark.flaky(retries=3)
    def test_collect_and_sum_spans_v2(self):
        """
        Tests the collection and summation of text values from paragraph spans within a scrollable container.

        This test navigates to a specific URL, collects all paragraph spans inside a scrollable container,
        sums their text values, and asserts the total sum.
        """
        self.page.open_url(ScrollingLocators.URL_3)

        # Collect all paragraph spans
        spans = self.page.collect_spans_until_last(
            ScrollingLocators.SCROLL_CONTAINER_ID,
            ScrollingLocators.PARAGRAPH_TAG,
            ScrollingLocators.LAST_SPAN_CLASS,
            ScrollingLocators.FOLLOWING_P
        )

        # Calculate the sum of the span text values
        total_sum = sum(int(span.text) for span in spans)

        # Optionally, add an assertion if you know the expected sum
        assert total_sum == 499917600
