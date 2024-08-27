from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.color import Color
from ..common.base_methods import BasePage


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

    def drag_and_drop(self, source, target):
        """
        Drags a source element and drops it onto a target element.

        Args:
            source (WebElement): The element to be dragged.
            target (WebElement): The element where the source should be dropped.
        """
        self.action.drag_and_drop(source, target).perform()

    def click_and_drag_by_offset(self, element, x_offset, y_offset=0):
        """
        Clicks and holds an element, then drags it by a specified offset.

        Args:
            element (WebElement): The element to be dragged.
            x_offset (int): The horizontal offset by which to move the element.
            y_offset (int, optional): The vertical offset by which to move the element. Defaults to 0.
        """
        self.action.click_and_hold(element).move_by_offset(x_offset, y_offset).release().perform()

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

    def drag_pieces_to_ranges(self, pieces, ranges, p_tag, color_property='background-color'):
        """
        Drags pieces to their corresponding ranges based on matching colors and verifies the result.

        Args:
            pieces (list): List of draggable piece WebElements.
            ranges (list): List of range WebElements.
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
