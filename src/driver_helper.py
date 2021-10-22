# import web driver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

import time




def configure_driver(path: str, is_headless : bool = True) -> WebDriver:
    chrome_options = Options()
    chrome_options.headless = is_headless
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)

    return driver

def scroll_down(driver: WebDriver):
    scroll_pos = driver.execute_script("return window.pageYOffset;")
    scroll = scroll_pos + 250
    driver.execute_script("window.scrollTo(0, " + str(scroll) + ");")

    #Wait for scroll to execute
    time.sleep(.5)

def scroll_until_find_by_class_name(class_name: str, driver: WebDriver, parent=None):
    element = None
    while element == None:
        try:
            if(parent == None):
                element = driver.find_element_by_class_name(class_name)
            else:
                element = parent.find_element_by_class_name(class_name)
        except:
            scroll_down(driver)
    return element





