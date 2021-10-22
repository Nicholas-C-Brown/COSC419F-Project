from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from linkedin_helper import linkedin_profile_baseurl as profile_baseurl, linkedin_exampleurl as example_url, login, validate_profile_url
from driver_helper import configure_driver as configure


driver_path = 'COSC419F-Project/assets/driver/chromedriver.exe'
is_headless = False

# APPLICATION START

# Get url from user
print("Enter your LinkedIn profile URL.")
url = profile_baseurl + input(profile_baseurl)

if(not validate_profile_url(url)):
    print("\nPlease enter a valid url.\nExample: " + example_url)
    exit


# Start Chrome Webdriver and Login
driver = configure(driver_path, is_headless)
login(driver)

# Go to user's profile page
driver.get(url)

# Get user's information
name_element = driver.find_element_by_class_name('text-heading-xlarge.inline.t-24.v-align-middle.break-words')

profile_element = driver.find_element_by_class_name('profile-detail')
bio_element = profile_element.find_element_by_class_name('inline-show-more-text.inline-show-more-text--is-collapsed.mt4.t-14')


print("\nThis is you: \n")
print("Name: " + name_element.text)
print("About: " + bio_element.text)
print("")

