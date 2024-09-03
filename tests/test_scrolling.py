import pytest

from ..pages.scrolling_page import ScrollingPage, ScrollingLocators


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
        checkbox_rows = self.page.find_all_loaded_divs()
        self.page.scroll_and_click_even_checkboxes(checkbox_rows, 99)
        self.page.click_alert_btn()
        alert_text = self.page.get_alert_text()

        assert alert_text == '5402f04236450f263540jk406504l506'

    @pytest.mark.skip
    def test_collect_and_sum(self):
        """
        Tests the collection and summation of text values from spans within multiple scrollable containers.
        This test navigates to a specific URL and iterates through 5 scrollable containers.
        It collects all spans in each container, sums their text values, and asserts that the final sum matches
        the expected value.
        """
        self.page.open_url(ScrollingLocators.URL_2)
        total_sum = self.page.scroll_all_scrollbars_and_sum_numbers()

        assert total_sum == 159858750

    @pytest.mark.flaky(retries=2)
    def test_collect_and_sum_spans_v2(self):
        """
        Tests the collection and summation of text values from paragraph spans within a scrollable container.
        This test navigates to a specific URL, collects all paragraph spans inside a scrollable container,
        sums their text values, and asserts the total sum.
        """
        self.page.open_url(ScrollingLocators.URL_3)
        spans = self.page.collect_all_paragraphs()
        total_sum = self.page.sum_span_text_in_scrollbox(spans)

        assert total_sum == 499917600
