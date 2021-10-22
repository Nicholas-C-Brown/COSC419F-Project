from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import driverHelper
import validators


driver_path = 'COSC419F-Project/assets/driver/chromedriver.exe'
is_headless = False

# APPLICATION START

# Get url from user
url = input("Enter a URL: ")

if(not validators.url(url)):
    print("\nPlease enter a valid url.\nExample: 'https://google.com'")
    exit(1)

# Start Chrome Webdriver
driver = driverHelper.configure_driver(driver_path, is_headless)
driver.get(url)


