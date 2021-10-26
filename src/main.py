import driverHelper
import validators


driver_path = '../assets/driver/chromedriver.exe'
is_headless = False

linkedin_profile_baseurl = "https://www.linkedin.com/in/"

# APPLICATION START

# Get url from user
print("Enter your LinkedIn profile URL.")
url = linkedin_profile_baseurl + input(linkedin_profile_baseurl)

if not validators.url(url):
    print("\nPlease enter a valid url.\nExample: https://www.linkedin.com/in/nicholas-c-brown")
    exit(1)


# Start Chrome Webdriver
driver = driverHelper.configure_driver(driver_path, is_headless)
driver.get(url)


