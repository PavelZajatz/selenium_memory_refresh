from ..common.base_methods import BasePage
from ..helpers.allure_helper import step
from selenium.webdriver.common.by import By


class CheckboxesLocators:
    """
    Locators and URLs used for testing checkboxes and related elements on different pages.
    """

    URL_1 = "https://parsinger.ru/selenium/5.9/7/index.html"
    URL_2 = "https://parsinger.ru/selenium/5.9/6/index.html"
    URL_3 = "https://parsinger.ru/selenium/5.9/5/index.html"
    URL_4 = "https://parsinger.ru/selenium/5.9/4/index.html"
    URL_5 = "http://parsinger.ru/expectations/4/index.html"
    URL_6 = "https://parsinger.ru/selenium/5.5/5/1.html"

    CHECKBOX = (By.TAG_NAME, 'input')
    CONTAINERS = (By.CLASS_NAME, 'container')
    CHECK_BTN = (By.XPATH, 'button')
    FLASH_CHECKBOX = (By.TAG_NAME, 'button')
    RESULT = (By.XPATH, '//*[@id="result"]|//*[@class="message"]|//*[@id="message"]')
    CLOSE_ADD_BTN = (By.XPATH, "//*[@id='close_ad']|//*[@id='ad']//*[@class='close']")
    BOX_BTN = (By.CSS_SELECTOR, '.box button')
    CLICK_BTN = (By.ID, "btn")
    DIV_CONTAINERS = (By.XPATH, '//*[@id="main-container"]/div')
    SPAN = (By.XPATH, 'span')
    DROPDOWN = lambda x: (By.XPATH, f"span[contains(text(), '{x}')]/../select")
    OPTION = lambda x: (By.XPATH, f"span[contains(text(), '{x}')]/..//option[@value='{x}']")
    COLOR_BTN = lambda x: (By.XPATH, f"span[contains(text(), '{x}')]/..//button[@data-hex='{x}']")
    COLOR_CHECKBOX = (By.XPATH, "input[@type='checkbox']")
    INPUT_FIELD = (By.XPATH, "input[@type='text']")
    CHECK_ALL_ELS_BTN = (By.XPATH, "//button[contains(text(), 'Проверить все элементы')]")
    DYNAMIC_CHECKBOX = lambda x: (By.XPATH, f'//div[@data-index="{x}"]')


class Checkboxes(BasePage):
    """
    Page class for handling checkboxes related actions.
    """

    @step
    def __init__(self, driver):
        """
        Initializes the Checkboxes page object with the WebDriver instance.

        Args:
            driver (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        """
        super().__init__(driver)

    @step
    def open_url(self, url):
        """
        Opens the specified URL.

        Args:
            url (str): The URL to open.
        """
        self.driver.get(url)

    @step
    def find_containers(self):
        """
        Finds all container elements containing checkboxes.

        Returns:
            list: A list of WebElement representing the container elements.
        """
        return self.find_elements(CheckboxesLocators.CONTAINERS)

    @step
    def is_checkbox_highlighted(self, container):
        """
        Checks if the checkbox within the given container is highlighted.

        Args:
            container (WebElement): The container element containing the checkbox.

        Returns:
            bool: True if the checkbox is highlighted, False otherwise.
        """
        return self.wait_element_to_be_selected(container.find_element(*CheckboxesLocators.CHECKBOX))

    @step
    def click_button_in_container(self, container):
        """
        Clicks the button inside the given container.

        Args:
            container (WebElement): The container element containing the button.
        """
        container.find_element(*CheckboxesLocators.CHECK_BTN).click()

    @step
    def get_result_text(self):
        """
        Retrieves the text of the result element.

        Returns:
            str: The text of the result element.
        """
        return self.find_element(CheckboxesLocators.RESULT).text

    @step
    def wait_for_checkbox_selection(self):
        """
        Waits until the checkbox is selected.

        Returns:
            WebElement: The selected checkbox element.
        """
        return self.wait_element_to_be_selected(self.find_element(CheckboxesLocators.CHECKBOX))

    @step
    def click_flash_checkbox(self):
        """
        Clicks the flashing checkbox.
        """
        self.find_element(CheckboxesLocators.FLASH_CHECKBOX).click()

    @step
    def close_advertisement(self):
        """
        Closes the advertisement by clicking the close button.
        """
        self.wait_for_element_to_be_clickable(CheckboxesLocators.CLOSE_ADD_BTN).click()
        self.wait_for_element_to_be_invisible(CheckboxesLocators.CLOSE_ADD_BTN)

    @step
    def click_box_button(self):
        """
        Clicks the box button on the page.
        """
        self.wait_for_element_to_be_clickable(CheckboxesLocators.BOX_BTN).click()

    @step
    def get_dynamic_checkbox_text(self, position):
        """
        Retrieves the text associated with a dynamic checkbox.

        Args:
            position (int): The position of the dynamic checkbox.

        Returns:
            str: The text associated with the checkbox.
        """
        text = ''
        while text == '':
            text = self.find_element(CheckboxesLocators.DYNAMIC_CHECKBOX(position)).text
        return text

    @step
    def click_dynamic_checkbox(self, position):
        """
        Clicks a dynamic checkbox at the given position.

        Args:
            position (int): The position of the dynamic checkbox.
        """
        self.click(CheckboxesLocators.DYNAMIC_CHECKBOX(position))

    @step
    def click_close_add_button(self):
        """
        Clicks the close ad button on the page.
        """
        self.click(CheckboxesLocators.CLOSE_ADD_BTN)

    @step
    def wait_for_page_title(self, partial_title, poll_frequency=0.05):
        """
        Waits until the page title contains the specified partial text.

        Args:
            partial_title (str): The partial title text to wait for.
            poll_frequency (float): The frequency in seconds to poll for the title. Default is 0.05 seconds.
        """
        return self.wait_title_contain_text(partial_title, timeout=60, poll_frequency=poll_frequency)

    @step
    def click_click_button(self):
        """
        Waits for the "Click" button to be clickable and then clicks it.
        """
        button = self.wait_for_element_to_be_clickable(CheckboxesLocators.CLICK_BTN)
        button.click()

    @step
    def interact_with_elements(self):
        """
        Interacts with elements in the main container by selecting dropdown options, clicking buttons,
        checking checkboxes, entering text, and submitting the form.
        """
        elements = self.find_elements(CheckboxesLocators.DIV_CONTAINERS)
        for el in elements:
            text = el.find_element(*CheckboxesLocators.SPAN).text
            el.find_element(*CheckboxesLocators.DROPDOWN(text)).click()
            el.find_element(*CheckboxesLocators.OPTION(text)).click()
            el.find_element(*CheckboxesLocators.COLOR_BTN(text)).click()
            el.find_element(*CheckboxesLocators.COLOR_CHECKBOX).click()
            el.find_element(*CheckboxesLocators.INPUT_FIELD).send_keys(text)
            el.find_element(*CheckboxesLocators.CHECK_BTN).click()

    @step
    def click_check_all_elements_button(self):
        """
        Clicks the 'Check All Elements' button on the page.
        """
        self.click(CheckboxesLocators.CHECK_ALL_ELS_BTN)

    @step
    def get_alert_text(self):
        """
        Retrieves the text from an alert popup.

        Returns:
            str: The text of the alert popup.
        """
        return self.driver.switch_to.alert.text
