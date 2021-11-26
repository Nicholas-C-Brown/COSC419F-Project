import sys
from typing import List

from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from application_settings import ApplicationSettings
from helper_methods.driver_helper import configure_driver
from models.user_profile import UserProfile

SEARCH_URL = "https://www.onetonline.org/find/result?s=<skill>"


def scrape_skill(skill: str, all_careers: bool = False) -> List[str]:
    # Start Chrome Webdriver
    driver: WebDriver
    try:
        driver = configure_driver('assets/driver/chromedriver.exe', ApplicationSettings.IS_HEADLESS)
    except SessionNotCreatedException:
        print("ChromeDriver is out of date.")
        sys.exit(1)
    except WebDriverException:
        print("Web driver path is invalid.")
        sys.exit(1)

    careers_list: List[str] = []

    url = SEARCH_URL.replace("<skill>", skill)
    if all_careers:
        url += "&a=1"

    try:

        driver.get(url)
        content = driver.find_element(By.ID, 'content')

        try:
            table = content.find_element(By.CSS_SELECTOR, 'table')
            table_elements_list = table.find_elements(By.CLASS_NAME, 'report2ed')

            for list_element in table_elements_list:
                text_element = list_element.find_element(By.CSS_SELECTOR, 'a')
                careers_list.append(text_element.text)

        except WebDriverException:
            print("No careers available for this skill: " + skill)

    except WebDriverException:
        print("idk someting went booga")

    finally:
        driver.close()

    return careers_list


def scrape_user_skills(user: UserProfile, all_careers: bool = False) -> dict:
    career_dict = {}

    for skill in user.skills:
        print("Processing skill: " + skill)
        careers = scrape_skill(skill, all_careers)

        career_dict[skill] = careers

    return career_dict
