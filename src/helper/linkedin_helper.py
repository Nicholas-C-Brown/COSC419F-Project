
from selenium import webdriver
import time
import validators

# Dummy profile credentials
username = "cardiacexorcist+1@gmail.com"
password = "419CEpicStyle"

# New Credentials once linkedin is done being a dickhead
# username = "brown.nicholas360+1@gmail.com"
# password = "COSC419F-Project"

#LinkedIn URLs
linkedin_baseurl = "https://www.linkedin.com/"
linkedin_loginurl = linkedin_baseurl + "login"
linkedin_profile_baseurl = linkedin_baseurl + "in/"
linkedin_exampleurl = linkedin_profile_baseurl + "nicholas-c-brown"

def login(driver: webdriver):

    driver.get(linkedin_loginurl)

    usernamefield = driver.find_element_by_id("username")
    passwordfield = driver.find_element_by_id("password")

    passwordfield.send_keys(password)
    time.sleep(0.1)
    usernamefield.send_keys(username)
    time.sleep(0.1)

    log_in_button = driver.find_element_by_xpath("//*[@type='submit']")
    log_in_button.click()

    time.sleep(.2)


def validate_url(url: str) -> bool:
    if(not validators.url(url)):
        return False

    if(not url.startswith(linkedin_baseurl)):
        return False

    return True


def validate_profile_url(url: str) -> bool:
    if(not url.startswith(linkedin_profile_baseurl)):
        return False

    return validate_url(url)



