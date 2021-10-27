from helper_methods.driver_helper import configure_driver as configure
from helper_methods.linkedin_helper import login, PROFILEURL, validate_profile_url
from models.user_profile import get_user_profile
import gui

DRIVER_PATH = 'assets/driver/chromedriver.exe'
IS_HEADLESS = False

# APPLICATION START

# Get url from user
url = gui.prompt_for_url(PROFILEURL)

while not validate_profile_url(url):
    gui.show_error_message(
        "Please enter a valid url.\nExample: https://www.linkedin.com/in/nicholas-c-brown")
    url = gui.prompt_for_url(PROFILEURL)

# Start Chrome Webdriver and Login
driver = configure(DRIVER_PATH, IS_HEADLESS)
login(driver)

user_profile = get_user_profile(url, driver)
driver.close()

user_profile.print_profile()
