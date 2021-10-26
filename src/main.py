from helper_methods.driver_helper import configure_driver as configure
from helper_methods.linkedin_helper import linkedin_profile_baseurl as profile_baseurl, linkedin_exampleurl as example_url, \
    login, validate_profile_url
from models.user_profile import get_user_profile
import gui

driver_path = 'assets/driver/chromedriver.exe'
is_headless = False

# APPLICATION START

# Get url from user
while True:
    url = gui.prompt_for_url(linkedin_profile_baseurl)
    if validators.url(url):
        break
    else:
        gui.show_error_message(
            "Please enter a valid url.\nExample: https://www.linkedin.com/in/nicholas-c-brown")

# Start Chrome Webdriver and Login
driver = configure(driver_path, is_headless)
login(driver)

user_profile = get_user_profile(url, driver)

user_profile.print_profile()
