import sys
from typing import List

from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from application_settings import ApplicationSettings
from models.career import Career
from models.user_profile import UserProfile
from helper_methods.driver_helper import configure_driver

CAREER_URL = "https://www.onetonline.org/find/result?s=<skill>"
WEIGHT_URL = "https://www.onetonline.org/find/score/<code>?s=<skill>"


def scrape_career(skill: str, all_careers: bool = False) -> List[Career]:
    """
    Collects potential careers information for the provided skill
    :param skill:
    :param all_careers: Collect all potential careers (As opposed to top 20)
    :return: A list of potential careers
    """
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

    careers_list: List[Career] = []

    url = CAREER_URL.replace("<skill>", skill)
    if all_careers:
        url += "&a=1"

    try:

        driver.get(url)
        content = driver.find_element(By.ID, 'content')

        try:
            table = content.find_element(By.CSS_SELECTOR, 'table')
            table_elements_list = table.find_elements(By.CSS_SELECTOR, 'tr')

            first = True
            for list_element in table_elements_list:

                # Skip header table row
                if first:
                    first = False
                    continue

                occupation_element = list_element.find_element(By.CLASS_NAME, 'report2ed')
                occupation_anchor_element = occupation_element.find_element(By.CSS_SELECTOR, 'a')
                occupation = occupation_anchor_element.text

                code_element = list_element.find_elements(By.CLASS_NAME, 'reportrtd')[1]
                code = code_element.text

                career = Career(occupation, code, 1)

                careers_list.append(career)

            for career in careers_list:
                career.weight = get_weight(code=career.code, skill=skill, driver=driver)

        except WebDriverException:
            print("No careers available for this skill: " + skill)

    except WebDriverException:
        print("Error :(")

    finally:
        driver.close()

    return careers_list


def scrape_user_careers(user: UserProfile, all_careers: bool = False, num_skills: int = -1) -> dict[str, List[Career]]:
    """
    Collects all potential careers for each skill of a given user
    :param user:
    :param all_careers: Collect all potential careers (As opposed to top 20)
    :param num_skills: The number of skills to process for the user
    :return: A dictionary containing potential careers related to each of the user's skills
    """
    career_dict = {}

    index = 0
    for skill in user.skills:
        if index == num_skills:
            break

        print("Processing skill: " + skill)
        careers = scrape_career(skill, all_careers)

        career_dict[skill] = careers
        index += 1

    return career_dict


def get_weight(code: str, skill: str, driver: WebDriver) -> int:
    """
    Collects the weighting of a given career relative to a given skill
    :param code: The career code
    :param skill:
    :param driver:
    :return: The weighting of the career
    """
    matches = 0

    try:
        url = WEIGHT_URL.replace("<code>", code).replace("<skill>", skill)
        driver.get(url)

        matches_element = driver.find_element(By.CLASS_NAME, "titleb")
        matches_text = matches_element.text

        matches = int(matches_text[0:matches_text.index(" ")])

    except WebDriverException:
        print("Couldn't find weight for this skill: ", skill)

    return matches
