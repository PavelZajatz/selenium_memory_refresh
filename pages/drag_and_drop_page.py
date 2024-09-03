from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color

from ..helpers.allure_helper import step
from ..common.base_methods import BasePage


class DragAndDropLocators:
    """Locators for Drag and Drop tests."""
    URL_1 = "https://parsinger.ru/selenium/5.10/8/index.html"
    URL_2 = "https://parsinger.ru/selenium/5.10/6/index.html"
    URL_3 = "https://parsinger.ru/selenium/5.10/4/index.html"
    URL_4 = "https://parsinger.ru/selenium/5.10/3/index.html"
    URL_5 = "https://parsinger.ru/draganddrop/2/index.html"
    URL_6 = "https://parsinger.ru/selenium/5.10/2/index.html"
    URL_7 = "https://parsinger.ru/draganddrop/3/index.html"
    URL_8 = "https://parsinger.ru/draganddrop/1/index.html"

    PIECE = (By.CLASS_NAME, 'piece')
    RANGE = (By.CLASS_NAME, 'range')
    MESSAGE = (By.XPATH, '//*[@id="message"]|//*[@class="message"]|//*[@id="result"]')
    P_TAG = (By.TAG_NAME, 'p')

    SLIDERS_CONTAINER = (By.CLASS_NAME, 'slider-container')
    CUR_POS_ELEMENT = (By.TAG_NAME, 'input')
    NEW_POS = (By.CLASS_NAME, 'target-value')

    BALL = (By.CLASS_NAME, 'ball_color')
    BASKET = (By.CLASS_NAME, 'basket_color')

    DRAGGABLE = (By.CLASS_NAME, 'draganddrop')
    DROPPABLE = (By.CLASS_NAME, 'draganddrop_end')

    SQUARE = (By.ID, 'draggable')
    DROP_ZONE = (By.CSS_SELECTOR, 'div.box')

    GREEN_SQUARE = (By.CSS_SELECTOR, 'div.draganddrop')
    DROP_ZONE_SINGLE = (By.CLASS_NAME, 'draganddrop_end')

    VIRTUAL_DRAGGABLE = (By.CLASS_NAME, 'ui-draggable')
    CONTROL_POINTS = (By.CSS_SELECTOR, 'div.controlPoint')

    RED_BLOCK = (By.ID, "draggable")
    TARGET_ZONE = (By.ID, "field2")


class DragAndDropPage(BasePage):
    """
    Page class for handling drag-and-drop related actions.

    This class provides methods for performing drag-and-drop operations, moving elements by offsets,
    and aligning elements based on their colors.
    """

    def __init__(self, driver):
        """
        Initializes the DragAndDropPage with the WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        """
        super().__init__(driver)
        self.action = ActionChains(driver)

    @step
    def drag_and_drop(self, source, target):
        """
        Drags a source element and drops it onto a target element.

        Args:
            source (WebElement): The element to be dragged.
            target (WebElement): The element where the source should be dropped.
        """
        self.action.drag_and_drop(source, target).perform()

    @step
    def click_and_drag_by_offset(self, element, x_offset, y_offset=0):
        """
        Clicks and holds an element, then drags it by a specified offset.

        Args:
            element (WebElement): The element to be dragged.
            x_offset (int): The horizontal offset by which to move the element.
            y_offset (int, optional): The vertical offset by which to move the element. Defaults to 0.
        """
        self.action.click_and_hold(element).move_by_offset(x_offset, y_offset).release().perform()

    @step
    def move_sliders_to_position(self, sliders, cur_pos_elem, new_positions):
        """
        Moves sliders to their target positions.

        Args:
            sliders (list): List of WebElements representing sliders.
            cur_pos_elem (tuple): Locator for the current position input element of each slider.
            new_positions (tuple): Locator for the element displaying the target position for each slider.
        """
        for slider in sliders:
            cur_pos_element = slider.find_element(*cur_pos_elem)
            new_pos = slider.find_element(*new_positions).text

            self.execute_script(
                "arguments[0].setAttribute('value', arguments[1]);", cur_pos_element, new_pos)
            self.execute_script(
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", cur_pos_element)
            self.execute_script(
                "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", cur_pos_element)

    @step
    def drag_and_drop_with_color_matching(self, draggables, droppables, color_property='background-color'):
        """
        Performs drag-and-drop actions by matching draggable elements with droppable targets based on a color property.

        Args:
            draggables (list): List of draggable WebElements.
            droppables (list): List of droppable WebElements.
            color_property (str, optional): The CSS property used for color comparison (e.g., 'border-color').
                                            Defaults to 'background-color'.

        Raises:
            ValueError: If no matching droppable is found for a given draggable element's color.
        """
        droppables_map = {
            Color.from_string(drop.value_of_css_property(color_property)): drop
            for drop in droppables
        }

        for draggable in draggables:
            draggable_color = Color.from_string(draggable.value_of_css_property('background-color'))
            matching_droppable = droppables_map.get(draggable_color)

            if matching_droppable:
                self.drag_and_drop(draggable, matching_droppable)
            else:
                raise ValueError(f"No matching droppable found for color: {draggable_color}")

    @step
    def drag_pieces_to_ranges(self, pieces, ranges, p_tag, color_property='background-color'):
        """
        Drags pieces to their corresponding ranges based on matching colors and verifies the result.

        Args:
            pieces (list): List of draggable piece WebElements.
            ranges (list): List of range WebElements.
            p_tag (tuple): Locator for the element within each range that indicates the target position
                       (e.g., the `<p>` tag element showing the offset).
            color_property (str, optional): The CSS property used for color comparison (e.g., 'border-color').
                                            Defaults to 'background-color'.
        """
        range_map = {
            Color.from_string(rng.value_of_css_property(color_property)): rng
            for rng in ranges
        }

        for piece in pieces:
            color = Color.from_string(piece.value_of_css_property(color_property))
            offset = range_map[color].find_element(*p_tag).text.split(': ')[1].replace("px", "")
            self.click_and_drag_by_offset(piece, int(offset))

    @step
    def locate_pieces_and_ranges(self):
        """
        Locates all draggable pieces and their corresponding target ranges on the page.

        This method finds the elements representing the pieces that need to be moved and
        the target areas (ranges) where these pieces should be placed.

        Returns:
            tuple: A tuple containing two lists:
                - pieces: List of draggable piece elements.
                - ranges: List of target range elements.
        """
        pieces = self.find_elements(DragAndDropLocators.PIECE)
        ranges = self.find_elements(DragAndDropLocators.RANGE)
        return pieces, ranges

    @step
    def drag_pieces_to_ranges_with_target(self, pieces, ranges):
        """
        Drags and drops each piece to its corresponding target range.

        This method calculates the required distance for each piece and moves it to the correct
        target range, ensuring the pieces are placed in the correct positions.

        Args:
            pieces (list): List of draggable piece elements.
            ranges (list): List of target range elements.
        """
        self.drag_pieces_to_ranges(pieces, ranges, DragAndDropLocators.P_TAG)

    @step
    def verify_success_message(self, expected_message):
        """
        Verifies that the success message (secret code) is displayed on the page.

        This method waits for the expected text to be present in the specified message element
        and returns whether the correct message is displayed.

        Args:
            expected_message (str): expected message text

        Returns:
            bool: True if the expected message is found, False otherwise.
        """
        return self.wait_for_text_to_be_present_in_element(DragAndDropLocators.MESSAGE, expected_message)

    @step
    def locate_sliders(self):
        """
        Locates all sliders on the page.

        This method finds the elements representing the sliders that need to be moved.

        Returns:
            list: A list of slider elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.SLIDERS_CONTAINER)

    @step
    def move_sliders_to_target_positions(self, sliders):
        """
        Moves each slider to the target position specified on the page.

        This method adjusts each slider's position based on the target value provided
        in the right column, triggering the necessary events to ensure the position is updated.

        Args:
            sliders (list): List of slider elements.
        """
        self.move_sliders_to_position(sliders,
                                      DragAndDropLocators.CUR_POS_ELEMENT,
                                      DragAndDropLocators.NEW_POS)

    @step
    def get_final_message(self):
        """
        Retrieves the final message (secret code) is displayed on the page.

        This method waits for the expected text to be present in the specified message element
        and returns text

        Returns:
            str: Text of found message
        """
        self.wait_for_element_to_be_present(DragAndDropLocators.MESSAGE)
        message = self.find_element(DragAndDropLocators.MESSAGE)
        return message.text

    @step
    def locate_balls(self):
        """
        Locates all ball elements on the page.

        This method finds and returns the elements representing the balls that need to be sorted.

        Returns:
            list: A list of ball elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.BALL)

    @step
    def locate_baskets(self):
        """
        Locates all basket elements on the page.

        This method finds and returns the elements representing the baskets that the balls need to be sorted into.

        Returns:
            list: A list of basket elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.BASKET)

    @step
    def locate_draggables(self):
        """
        Locates all draggable elements on the page.

        This method finds and returns the elements that can be dragged and need to be paired
        with corresponding droppable elements.

        Returns:
            list: A list of draggable elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.DRAGGABLE)

    @step
    def locate_droppables(self):
        """
        Locates all droppable elements on the page.

        This method finds and returns the elements that can receive draggable elements based on
        color matching.

        Returns:
            list: A list of droppable elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.DROPPABLE)

    @step
    def locate_draggable_square(self):
        """
        Locates the draggable square element on the page.

        This method finds and returns the draggable square that needs to be moved to different
        drop zones.

        Returns:
            WebElement: The draggable square element.
        """
        return self.find_element(DragAndDropLocators.SQUARE)

    @step
    def locate_drop_zones(self):
        """
        Locates all drop zone elements on the page.

        This method finds and returns the drop zones where the draggable square will be dropped.

        Returns:
            list: A list of drop zone elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.DROP_ZONE)

    @step
    def drag_square_through_zones(self, draggable, drop_zones):
        """
        Drags and drops the square element through each drop zone sequentially.

        This method performs the drag-and-drop operation for the draggable square, moving it into
        each drop zone in the provided list.

        Args:
            draggable (WebElement): The draggable square element.
            drop_zones (list): A list of drop zone elements where the square will be dropped.
        """
        for drop_zone in drop_zones:
            self.drag_and_drop(draggable, drop_zone)

    @step
    def locate_green_squares(self):
        """
        Locates all green square elements on the page.

        This method finds and returns a list of all draggable green square elements.

        Returns:
            list: A list of green square elements found on the page.
        """
        return self.find_elements(DragAndDropLocators.GREEN_SQUARE)

    @step
    def locate_single_drop_zone(self):
        """
        Locates the single drop zone element on the page.

        This method finds and returns the single drop zone where all green squares need to be dropped.

        Returns:
            WebElement: The drop zone element.
        """
        return self.find_element(DragAndDropLocators.DROP_ZONE_SINGLE)

    @step
    def drag_squares_to_drop_zone(self, green_squares, drop_zone):
        """
        Drags and drops each green square into the single drop zone.

        This method performs the drag-and-drop operation for each green square, moving them into
        the specified drop zone.

        Args:
            green_squares (list): A list of green square elements to be dragged.
            drop_zone (WebElement): The drop zone element where the squares will be dropped.
        """
        for square in green_squares:
            self.drag_and_drop(square, drop_zone)

    @step
    def get_draggable_element(self):
        """
        Retrieves the draggable element from the page.

        This method waits for the draggable element to be visible on the page and returns it.

        Returns:
            WebElement: The draggable element.
        """
        return self.wait_for_element_to_be_visible(DragAndDropLocators.VIRTUAL_DRAGGABLE)

    @step
    def get_control_points(self):
        """
        Retrieves all control points from the page.

        This method finds and returns all control points that the draggable element will move over.

        Returns:
            list: A list of control point elements.
        """
        return self.find_elements(DragAndDropLocators.CONTROL_POINTS)

    @step
    def drag_through_control_points(self, draggable, control_points):
        """
        Drags the element through all control points and returns to the first point.

        This method performs a click-and-hold action on the draggable element, then moves it
        through each control point sequentially and finally releases it back at the first control point.

        Args:
            draggable (WebElement): The draggable element.
            control_points (list): A list of control point elements to move over.
        """
        self.action.click_and_hold(draggable).perform()
        for point in control_points:
            self.action.move_to_element(point).perform()
        self.action.move_to_element(control_points[0]).release().perform()

    @step
    def get_red_block(self):
        """
        Retrieves the red block element from the page.

        This method waits for the red block to be visible on the page and returns it.

        Returns:
            WebElement: The red block element.
        """
        return self.wait_for_element_to_be_visible(DragAndDropLocators.RED_BLOCK)

    @step
    def get_target_zone(self):
        """
        Retrieves the target drop zone element from the page.

        This method finds and returns the target drop zone where the red block will be dropped.

        Returns:
            WebElement: The target drop zone element.
        """
        return self.find_element(DragAndDropLocators.TARGET_ZONE)

    @step
    def drag_red_block_to_target(self, red_block, target_zone):
        """
        Drags the red block and drops it into the target drop zone.

        This method performs a drag-and-drop operation with the red block element, moving it to the
        target drop zone element.

        Args:
            red_block (WebElement): The red block element to be dragged.
            target_zone (WebElement): The target drop zone where the red block will be dropped.
        """
        self.drag_and_drop(red_block, target_zone)
