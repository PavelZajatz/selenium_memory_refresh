from ..helpers.allure_helper import step
from ..common.base_methods import BasePage


class ScrollingPage(BasePage):
    """
    Page class for handling scrolling related actions.
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
        Helper method to click checkboxes with even values within a container element.

        Args:
            container: The WebElement container holding checkboxes.
            :param container:
            :param checkboxes_locator:
        """
        checkboxes = container.find_elements(*checkboxes_locator)
        for checkbox in checkboxes:
            if int(checkbox.get_attribute('value')) % 2 == 0:
                checkbox.click()

    @step
    def get_next_span(self, current_span, next_span_locator):
        """
        Finds the next sibling div element to continue the scrolling process.

        Args:
            current_span: The current WebElement span.
            next_span_locator: Locator for the next sibling div element.

        Returns:
            The next sibling WebElement.
        """
        return current_span.find_element(*next_span_locator)

    @step
    def collect_spans(self, container_locator, span_locator, last_span_class, following_span):
        """
        Collects all span elements within a specified container until the last span is reached.

        Args:
            container_locator: Locator for the container holding the spans.
            span_locator: Locator pattern for the spans.
            last_span_class: The class name that identifies the last span.
            following_span: Locator for following span

        Returns:
            List of collected span elements.
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
        Collects all spans within a scrollable container until the last span is reached.

        Args:
            container_locator: Locator for the container holding the spans.
            span_locator: Locator for the spans.
            last_span_class: The class name that identifies the last span.

        Returns:
            List of collected span elements.
        """
        spans = [self.find_element(container_locator).find_element(*span_locator)]
        while True:
            next_span = spans[-1].find_element(*following_sibling)
            self.scroll_into_view(next_span)
            spans.append(next_span)
            if next_span.get_attribute("class") == last_span_class:
                break
        return spans
