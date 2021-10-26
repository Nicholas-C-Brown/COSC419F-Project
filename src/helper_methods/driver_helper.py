# import web driver
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

import time

from selenium.webdriver.common.by import By

get_window_y_script = "return window.pageYOffset;"


def configure_driver(path: str, is_headless: bool = True) -> WebDriver:
    chrome_options = Options()
    chrome_options.headless = is_headless
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)

    return driver


def scroll_down(driver: WebDriver, start_pos: int = None):
    scroll_pos = driver.execute_script(get_window_y_script)
    scroll = scroll_pos + 250
    driver.execute_script("window.scrollTo(0, " + str(scroll) + ");")

    # Wait for scroll to execute
    time.sleep(.5)


def scroll_until_find_by_class_name(class_name: str, driver: WebDriver, parent=None):
    # Start at top of screen
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    last_pos = driver.execute_script(get_window_y_script)

    element = None
    while element is None:
        try:
            if parent is None:
                element = driver.find_element(By.CLASS_NAME, class_name)
            else:
                element = parent.find_element(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            scroll_down(driver)
            new_pos = driver.execute_script(get_window_y_script)
            if last_pos == new_pos:
                return None
            else:
                last_pos = new_pos
    return element
