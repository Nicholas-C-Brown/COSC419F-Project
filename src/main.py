from helper.linkedin_helper import linkedin_profile_baseurl as profile_baseurl, linkedin_exampleurl as example_url, login, validate_profile_url
from helper.driver_helper import configure_driver as configure
from models.user_profile import UserProfile, get_user_profile

driver_path = 'COSC419F-Project/assets/driver/chromedriver.exe'
is_headless = True

# APPLICATION START

# Get url from user
print("Enter your LinkedIn profile URL.")
url = profile_baseurl + input(profile_baseurl)

if(not validate_profile_url(url)):
    print("\nPlease enter a valid url.\nExample: " + example_url)
    exit(1)

# Start Chrome Webdriver and Login
driver = configure(driver_path, is_headless)
login(driver)

user_profile = get_user_profile(url, driver)

user_profile.print_profile()

