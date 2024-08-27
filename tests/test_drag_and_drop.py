import pytest
from selenium.webdriver.common.by import By

from ..pages.drag_and_drop_page import DragAndDropPage


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
    MESSAGE = (By.XPATH, '//*[@id="message"]|//*[@class="message"]')
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
    RESULT = (By.ID, 'result')


class TestDragAndDrop:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Setup fixture to initialize the Checkboxes page object.

        Args:
            driver: WebDriver instance used for interacting with the browser.
        """
        self.page = DragAndDropPage(driver)

    @pytest.mark.flaky(retries=2)
    def test_throw_at_the_right_distance(self):
        """
        Test method to automate the placement of all pieces into their respective plots on the webpage.

        The process involves:
        1. Opening the specified URL.
        2. Locating all the pieces and their corresponding target plots on the page.
        3. Calculating the required distance for each piece to reach its target.
        4. Move each piece to its correct position.
        5. Verifying that a success message (secret code) is displayed once all pieces are correctly placed.

        The test is considered successful if the expected message is displayed.
        """
        self.page.open_url(DragAndDropLocators.URL_1)
        pieces = self.page.find_elements(DragAndDropLocators.PIECE)
        ranges = self.page.find_elements(DragAndDropLocators.RANGE)

        self.page.drag_pieces_to_ranges(pieces, ranges, DragAndDropLocators.P_TAG)

        message = self.page.wait_for_text_to_be_present_in_element(DragAndDropLocators.MESSAGE,
                                                                   'GD60-34JX-354F-3HJC-NXC0-54KO-W3B1-2DFH-23JG')
        assert message

    def test_sliders_movement(self):
        """
        Test method to move all sliders to their target positions and verify the resulting message.

        Steps:
        1. Open the target URL.
        2. Identify all sliders on the page.
        3. For each slider, move it to the target position specified in the right column.
        4. Trigger the necessary events to ensure the position is updated.
        5. Verify that the displayed message matches the expected secret code.
        """
        self.page.open_url(DragAndDropLocators.URL_2)
        sliders = self.page.find_elements(DragAndDropLocators.SLIDERS_CONTAINER)
        self.page.move_sliders_to_position(sliders,
                                           DragAndDropLocators.CUR_POS_ELEMENT,
                                           DragAndDropLocators.NEW_POS)

        message = self.page.wait_for_element_to_be_present(DragAndDropLocators.MESSAGE)
        assert message.text == '3F9D-DVB0-EH46-96VB-JHJ5-34UK-2SSF-JKG0'

    def test_balls_auto_sort(self):
        """
        Tests the functionality of automatically sorting balls into their corresponding baskets on a webpage.

        Steps:
        1. Opens the specified URL containing the balls and baskets.
        2. Finds all ball elements on the page using their CSS class.
        3. Maps each basket to its corresponding color based on the CSS property 'background-color'.
        4. Drags and drops each ball into the basket that matches its color.
        5. Asserts that a message indicating success appears on the page, verifying that all balls were
        correctly sorted.
        """
        self.page.open_url(DragAndDropLocators.URL_3)
        balls = self.page.find_elements(DragAndDropLocators.BALL)
        baskets = self.page.find_elements(DragAndDropLocators.BASKET)
        self.page.drag_and_drop_with_color_matching(balls, baskets)

        assert self.page.find_element(DragAndDropLocators.MESSAGE).text == 'ER96-SVN0-34HX-ER3W-WHJ5-WHG4-SNJ1-12LO'

    def test_find_pairs(self):
        """
        Tests the functionality of finding and pairing draggable elements with their corresponding droppable
        targets based on color.

        Steps:
        1. Opens the specified URL containing draggable and droppable elements.
        2. Finds all draggable elements on the page using their CSS class.
        3. Maps each droppable target to its corresponding color based on the CSS property 'border-color'.
        4. For each draggable element, finds the matching droppable target based on color and performs
        a drag-and-drop operation.
        5. Assert the message displayed on the page after all pairs are matched.
        """
        self.page.open_url(DragAndDropLocators.URL_4)
        draggables = self.page.find_elements(DragAndDropLocators.DRAGGABLE)
        droppables = self.page.find_elements(DragAndDropLocators.DROPPABLE)
        self.page.drag_and_drop_with_color_matching(draggables, droppables, 'border-color')

        assert self.page.find_element(DragAndDropLocators.MESSAGE).text == 'F934-3902-2FH4-DV02-3454-9HCX-4F53-12FS'

    def test_square_journey(self):
        """
        Tests the drag-and-drop functionality by moving a single draggable square through a series of drop zones.

        Steps:
        1. Opens the specified URL containing a draggable square and multiple drop zones.
        2. Identifies the draggable element and the drop zones on the page.
        3. Drags and drops the square into each of the drop zones sequentially.
        4. Asserts that the expected success message appears on the page after completing the journey.
        """
        self.page.open_url(DragAndDropLocators.URL_5)
        draggable = self.page.find_element(DragAndDropLocators.SQUARE)
        drop_zones = self.page.find_elements(DragAndDropLocators.DROP_ZONE)

        for drop in drop_zones:
            self.page.drag_and_drop(draggable, drop)

        assert self.page.find_element(DragAndDropLocators.MESSAGE).text == 'NS4zNDUzMzU0NTQ2MzU0NDVlKzIx'

    def test_movements_of_green_squares(self):
        """
        Tests the functionality of dragging multiple green squares into a single drop zone.

        Steps:
        1. Opens the specified URL containing multiple draggable green squares and a single drop zone.
        2. Identifies all draggable elements and the drop zone on the page.
        3. Drags and drops each green square into the drop zone.
        4. Asserts that the expected success message appears on the page after all squares are moved.
        """
        self.page.open_url(DragAndDropLocators.URL_6)
        green_squares = self.page.find_elements(DragAndDropLocators.GREEN_SQUARE)
        drop_zone = self.page.find_element(DragAndDropLocators.DROP_ZONE_SINGLE)

        for square in green_squares:
            self.page.drag_and_drop(square, drop_zone)

        assert self.page.find_element(DragAndDropLocators.MESSAGE).text == '39FG-3490-34F0-944S-34FV-80VX-F3GJ-349B'

    def test_open_virtual_space(self):
        """
        Tests the interaction with a virtual space by clicking and holding a draggable element and moving
        it through multiple control points.

        Steps:
        1. Opens the specified URL containing a draggable element and multiple control points.
        2. Clicks and holds the draggable element.
        3. Moves the draggable element sequentially over each control point, returning to the first control point.
        4. Asserts that the expected success message appears on the page after the virtual space is fully explored.
        """
        self.page.open_url(DragAndDropLocators.URL_7)
        draggable = self.page.wait_for_element_to_be_visible(DragAndDropLocators.VIRTUAL_DRAGGABLE)
        self.page.action.click_and_hold(draggable).perform()

        control_points = self.page.find_elements(DragAndDropLocators.CONTROL_POINTS)
        for point in control_points:
            self.page.action.move_to_element(point).perform()
        self.page.action.move_to_element(control_points[0]).release().perform()

        assert self.page.find_element(DragAndDropLocators.MESSAGE).text == 'Ni44NTc4MTk2NzY4NTQ0NTZlKzIz'

    def test_red_block_moves(self):
        """
        Tests the drag-and-drop functionality by moving a red block from its starting position to a specified drop zone.

        Steps:
        1. Opens the specified URL containing a draggable red block and a target drop zone.
        2. Identifies the draggable red block and the target drop zone on the page.
        3. Drags and drops the red block into the target drop zone.
        4. Asserts that the expected result message appears on the page after completing the drag-and-drop action.
        """
        self.page.open_url(DragAndDropLocators.URL_8)
        red_block = self.page.wait_for_element_to_be_visible(DragAndDropLocators.RED_BLOCK)
        target_zone = self.page.find_element(DragAndDropLocators.TARGET_ZONE)

        self.page.drag_and_drop(red_block, target_zone)

        assert self.page.find_element(DragAndDropLocators.RESULT).text == 'ODYzNDQ1MzM0NTE0MzQ2OTAwMA=='
