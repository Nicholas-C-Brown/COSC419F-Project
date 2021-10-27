import time
import validators
from selenium import webdriver
from selenium.webdriver.common.by import By


# Dummy profile credentials
USERNAME = "COSC419F.Project@gmail.com"
PASSWORD = "%COSC419F-Project%"

# LinkedIn URLs
BASEURL = "https://www.linkedin.com/"
LOGINURL = BASEURL + "login"
PROFILEURL = BASEURL + "in/"
EXAMPLEURL = PROFILEURL + "nicholas-c-brown"


def login(driver: webdriver):
    """
    Logs into LinkedIn with a dummy account

    :param driver: The Chrome WebDriver instance
    """
    driver.get(LOGINURL)

    usernamefield = driver.find_element(By.ID, "username")
    passwordfield = driver.find_element(By.ID, "password")

    passwordfield.send_keys(PASSWORD)
    time.sleep(0.1)
    usernamefield.send_keys(USERNAME)
    time.sleep(0.1)

    log_in_button = driver.find_element_by_xpath("//*[@type='submit']")
    log_in_button.click()

    time.sleep(.2)


def validate_url(url: str) -> bool:
    """
    Validates the given URL is a valid LinkedIn URL

    :param url: The URL to validate
    :return: The URL's validity status
    """
    if not validators.url(url):
        return False

    if not url.startswith(BASEURL):
        return False

    return True


def validate_profile_url(url: str) -> bool:
    """
        Validates the given URL is a valid LinkedIn Profile URL

        :param url: The URL to validate
        :return: The URL's validity status
        """
    if not url.startswith(PROFILEURL):
        return False

    return validate_url(url)
