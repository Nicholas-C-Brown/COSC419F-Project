import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

GET_WINDOW_YOFFSET_SCRIPT = "return window.pageYOffset;"


def configure_driver(path: str, is_headless: bool = True) -> WebDriver:
    """
    Creates a Chrome WebDriver instance.

    :param path: Path to the Chrome WebDriver executable
    :param is_headless: Specifies whether to run the driver in headless mode
    :return: A Chrome WebDriver instance
    """
    chrome_options = Options()
    chrome_options.headless = is_headless
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)

    return driver


def scroll_down(driver: WebDriver):
    """
    Scrolls the webpage down from the current Y position

    :param driver: The Chrome WebDriver instance
    """
    scroll_pos = driver.execute_script(GET_WINDOW_YOFFSET_SCRIPT)
    scroll = scroll_pos + 250
    driver.execute_script("window.scrollTo(0, " + str(scroll) + ");")

    # Wait for scroll to execute
    time.sleep(.5)


def scroll_until_find_by_class_name(class_name: str, driver: WebDriver, parent=None):
    """
    Looks for an WebElement object by class name by scrolling down the entire webpage.
    If a parent WebElement is provided it will only search through its children WebElements.

    :param class_name: The WebElement class name to search for.
    :param driver: The Chrome WebDriver instance
    :param parent: (Optional) A Parent WebElement object
    :return: A WebElement object matching the given class name or None if no WebElement was found.
    """
    # Start at top of screen
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    last_pos = driver.execute_script(GET_WINDOW_YOFFSET_SCRIPT)

    element = None
    while element is None:
        try:
            if parent is None:
                element = driver.find_element(By.CLASS_NAME, class_name)
            else:
                element = parent.find_element(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            scroll_down(driver)
            new_pos = driver.execute_script(GET_WINDOW_YOFFSET_SCRIPT)
            if last_pos != new_pos:
                last_pos = new_pos
            else:
                return None
    return element
