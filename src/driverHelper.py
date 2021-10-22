# import web driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def configure_driver(path, is_headless=True):
    chrome_options = Options()
    chrome_options.headless = is_headless
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    return driver


