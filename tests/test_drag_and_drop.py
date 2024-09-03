import pytest

from ..pages.drag_and_drop_page import DragAndDropPage, DragAndDropLocators


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
        expected_result = 'GD60-34JX-354F-3HJC-NXC0-54KO-W3B1-2DFH-23JG'
        self.page.open_url(DragAndDropLocators.URL_1)

        pieces, ranges = self.page.locate_pieces_and_ranges()
        self.page.drag_pieces_to_ranges_with_target(pieces, ranges)
        message_displayed = self.page.verify_success_message(expected_result)

        assert message_displayed, f" Message '{expected_result}' is not shown"

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
        expected = '3F9D-DVB0-EH46-96VB-JHJ5-34UK-2SSF-JKG0'
        self.page.open_url(DragAndDropLocators.URL_2)
        sliders = self.page.locate_sliders()
        self.page.move_sliders_to_target_positions(sliders)
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"

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
        expected = 'ER96-SVN0-34HX-ER3W-WHJ5-WHG4-SNJ1-12LO'
        self.page.open_url(DragAndDropLocators.URL_3)
        balls = self.page.locate_balls()
        baskets = self.page.locate_baskets()
        self.page.drag_and_drop_with_color_matching(balls, baskets)
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"

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
        expected = 'F934-3902-2FH4-DV02-3454-9HCX-4F53-12FS'
        self.page.open_url(DragAndDropLocators.URL_4)
        draggables = self.page.locate_draggables()
        droppables = self.page.locate_droppables()
        self.page.drag_and_drop_with_color_matching(draggables, droppables, 'border-color')
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"

    def test_square_journey(self):
        """
        Tests the drag-and-drop functionality by moving a single draggable square through a series of drop zones.

        Steps:
        1. Opens the specified URL containing a draggable square and multiple drop zones.
        2. Identifies the draggable element and the drop zones on the page.
        3. Drags and drops the square into each of the drop zones sequentially.
        4. Asserts that the expected success message appears on the page after completing the journey.
        """
        expected = 'NS4zNDUzMzU0NTQ2MzU0NDVlKzIx'
        self.page.open_url(DragAndDropLocators.URL_5)
        draggable_square = self.page.locate_draggable_square()
        drop_zones = self.page.locate_drop_zones()
        self.page.drag_square_through_zones(draggable_square, drop_zones)
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"

    def test_movements_of_green_squares(self):
        """
        Tests the functionality of dragging multiple green squares into a single drop zone.

        Steps:
        1. Opens the specified URL containing multiple draggable green squares and a single drop zone.
        2. Identifies all draggable elements and the drop zone on the page.
        3. Drags and drops each green square into the drop zone.
        4. Asserts that the expected success message appears on the page after all squares are moved.
        """
        expected = '39FG-3490-34F0-944S-34FV-80VX-F3GJ-349B'
        self.page.open_url(DragAndDropLocators.URL_6)
        green_squares = self.page.locate_green_squares()
        drop_zone = self.page.locate_single_drop_zone()
        self.page.drag_squares_to_drop_zone(green_squares, drop_zone)
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"

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
        expected = 'Ni44NTc4MTk2NzY4NTQ0NTZlKzIz'
        self.page.open_url(DragAndDropLocators.URL_7)
        draggable = self.page.get_draggable_element()
        control_points = self.page.get_control_points()
        self.page.drag_through_control_points(draggable, control_points)
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"

    def test_red_block_moves(self):
        """
        Tests the drag-and-drop functionality by moving a red block from its starting position to a specified drop zone.

        Steps:
        1. Opens the specified URL containing a draggable red block and a target drop zone.
        2. Identifies the draggable red block and the target drop zone on the page.
        3. Drags and drops the red block into the target drop zone.
        4. Asserts that the expected result message appears on the page after completing the drag-and-drop action.
        """
        expected = 'ODYzNDQ1MzM0NTE0MzQ2OTAwMA=='
        self.page.open_url(DragAndDropLocators.URL_8)
        red_block = self.page.get_red_block()
        target_zone = self.page.get_target_zone()
        self.page.drag_red_block_to_target(red_block, target_zone)
        message = self.page.get_final_message()

        assert message == expected, \
            f"Expected message to be {expected}, but got '{message}'"
