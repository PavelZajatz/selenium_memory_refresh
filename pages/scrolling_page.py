from selenium.webdriver.common.by import By
from ..helpers.allure_helper import step
from ..common.base_methods import BasePage


class ScrollingLocators:
    """
    Contains locators and URLs for the scrolling test scenarios.
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


class ScrollingPage(BasePage):
    """
    Page Object Model (POM) for handling scrolling-related actions.
    """

    def __init__(self, driver):
        """
        Initializes the ScrollingPage with the WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        """
        super().__init__(driver)

    @step
    def click_even_checkboxes(self, container, checkboxes_locator):
        """
        Clicks checkboxes with even values within a specified container element.

        Args:
            container (WebElement): The WebElement container holding the checkboxes.
            checkboxes_locator (tuple): Locator for the checkboxes within the container.
        """
        checkboxes = container.find_elements(*checkboxes_locator)
        for checkbox in checkboxes:
            if int(checkbox.get_attribute('value')) % 2 == 0:
                checkbox.click()

    @step
    def get_next_span(self, current_span, next_span_locator):
        """
        Retrieves the next sibling span element in the DOM.

        Args:
            current_span (WebElement): The current WebElement span.
            next_span_locator (tuple): Locator for the next sibling span element.

        Returns:
            WebElement: The next sibling span element.
        """
        return current_span.find_element(*next_span_locator)

    @step
    def collect_spans(self, container_locator, span_locator, last_span_class, following_span):
        """
        Collects all span elements within a specified container until the last span is reached.

        Args:
            container_locator (tuple): Locator for the container holding the spans.
            span_locator (tuple): Locator for the spans.
            last_span_class (str): The class name that identifies the last span.
            following_span (tuple): Locator for the following span.

        Returns:
            list: A list of collected span WebElement objects.
        """
        spans = [self.find_element(container_locator).find_element(*span_locator)]
        while True:
            next_span = spans[-1].find_element(*following_span)
            self.scroll_to_element(next_span)
            spans.append(next_span)
            if next_span.get_attribute("class") == last_span_class:
                break
        return spans

    @step
    def collect_spans_until_last(self, container_locator, span_locator, last_span_class, following_sibling):
        """
        Collects all span elements within a scrollable container until the last span is reached.

        Args:
            container_locator (tuple): Locator for the container holding the spans.
            span_locator (tuple): Locator for the spans.
            last_span_class (str): The class name that identifies the last span.
            following_sibling (tuple): Locator for the following sibling span.

        Returns:
            list: A list of collected span WebElement objects.
        """
        spans = [self.find_element(container_locator).find_element(*span_locator)]
        while True:
            next_span = spans[-1].find_element(*following_sibling)
            self.scroll_into_view(next_span)
            spans.append(next_span)
            if next_span.get_attribute("class") == last_span_class:
                break
        return spans

    @step
    def find_all_loaded_divs(self):
        """
        Finds and returns all div elements loaded in the main container.

        Returns:
            list: A list of WebElement objects representing the loaded div elements.
        """
        return [self.find_element(ScrollingLocators.MAIN_CONTAINER).find_element(*ScrollingLocators.DIV)]

    @step
    def scroll_and_click_even_checkboxes(self, checkbox_rows, max_rows):
        """
        Scrolls through the rows and clicks checkboxes with even values.

        Args:
            checkbox_rows (list): A list of WebElement objects representing the rows of checkboxes.
            max_rows (int): The maximum number of rows to process.
        """
        counter = 0
        self.click_even_checkboxes(checkbox_rows[0], ScrollingLocators.CHECKBOX)
        while True:
            next_span = self.get_next_span(checkbox_rows[-1], ScrollingLocators.NEXT_DIV)
            self.click_even_checkboxes(next_span, ScrollingLocators.CHECKBOX)
            self.scroll_into_view(next_span)
            checkbox_rows.append(next_span)
            counter += 1
            if counter == max_rows:
                break

    @step
    def click_alert_btn(self):
        """
        Clicks the alert button on the page.

        Returns:
            WebElement: The alert button WebElement after it is clicked.
        """
        return self.click(ScrollingLocators.ALERT_BUTTON)

    @step
    def scroll_all_scrollbars_and_sum_numbers(self):
        """
        Scrolls through all the scrollbars on the page and sums the numbers in the span elements.

        Returns:
            int: The total sum of the numbers found in the span elements.
        """
        total_sum = 0
        for i in range(1, 6):
            container_locator = ScrollingLocators.SCROLL_CONTAINER(i)
            spans = self.collect_spans(
                container_locator, ScrollingLocators.SPAN,
                ScrollingLocators.LAST_SPAN_CLASS, ScrollingLocators.FOLLOWING_SPAN)
            sum_i = sum(int(span.text) for span in spans)
            total_sum += sum_i
        return total_sum

    @step
    def collect_all_paragraphs(self):
        """
        Collects all paragraph elements within the scrollable container.

        Returns:
            list: A list of WebElement objects representing the collected paragraph elements.
        """
        spans = self.collect_spans_until_last(
            ScrollingLocators.SCROLL_CONTAINER_ID,
            ScrollingLocators.PARAGRAPH_TAG,
            ScrollingLocators.LAST_SPAN_CLASS,
            ScrollingLocators.FOLLOWING_P
        )
        return spans

    @step
    def sum_span_text_in_scrollbox(self, spans):
        """
        Sums the text values of the collected span elements.

        Args:
            spans (list): A list of WebElement objects representing the spans to sum.

        Returns:
            int: The total sum of the text values in the spans.
        """
        return sum(int(span.text) for span in spans)
