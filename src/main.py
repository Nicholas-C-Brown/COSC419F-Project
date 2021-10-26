import driverHelper
import validators
import gui


driver_path = 'assets/driver/chromedriver.exe'
is_headless = False

linkedin_profile_baseurl = "https://www.linkedin.com/in/"

# APPLICATION START

# Get url from user
while True:
    url = gui.prompt_for_url(linkedin_profile_baseurl)
    if validators.url(url):
        break
    else:
        gui.show_error_message(
            "Please enter a valid url.\nExample: https://www.linkedin.com/in/nicholas-c-brown")


# Start Chrome Webdriver
driver = driverHelper.configure_driver(driver_path, is_headless)
driver.get(url)
