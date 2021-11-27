import sys
from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from selenium.common.exceptions import NoSuchElementException, WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from application_settings import ApplicationSettings
from helper_methods.driver_helper import configure_driver, scroll_until_find_by_class_name
from helper_methods.linkedin_helper import validate_profile_url, PROFILEURL as LINKEDIN_PROFILEURL, \
    EXAMPLEURL as LINKEDIN_EXAMPLEURL, login
from progress_bar import ProgressBar
from skillset_scraper import scrape_user_careers
from user_interfaces.ui_linkedin_input import Ui_LinkedInInput
from models.user_profile import UserProfile, normalize_weights
from models.work_experience import WorkExperience


class SubmissionThread(QThread):
    """
    A thread used to run the user data collection
    """
    change_value = pyqtSignal(str, int)
    result = pyqtSignal(UserProfile)
    finished = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        """
        Runs the user data collection method and emits the results
        """
        user_profile = get_user_profile(self.url, self.change_value)
        self.result.emit(user_profile)
        self.finished.emit()


class LinkedInInput:
    """
    A class for handling the data collection from LinkedIn
    """
    progress_bar: ProgressBar
    thread: SubmissionThread
    user_profile: UserProfile

    def __init__(self, application: QApplication):
        self.application = application

        self.window = window = QtWidgets.QMainWindow()
        self.interface = interface = Ui_LinkedInInput()
        interface.setupUi(window)

        interface.input_url.setText(LINKEDIN_PROFILEURL)
        interface.lbl_invalid.setVisible(False)
        interface.lbl_invalid.setText(f"Please enter a valid url.\nExample: {LINKEDIN_EXAMPLEURL}")
        interface.btn_submit.clicked.connect(self.submit)
        interface.btn_exit.clicked.connect(self.exit)

        window.show()

    def set_progress(self, info, step):
        """
        Sets the current progress bar's progress
        :param info: information on the current step
        :param step: the current step
        """
        self.progress_bar.set_progress(info, step)

    def set_profile(self, profile):
        """
        Sets the user profile
        :param profile: a user profile
        """
        self.user_profile = profile

    def scrape_careers(self):
        """
        Scrapes careers for the current user profile
        """

        self.user_profile.career_dict = scrape_user_careers(user=self.user_profile, all_careers=False, num_skills=5)
        normalize_weights(self.user_profile.career_dict)
        self.user_profile.print_career_dict()
        self.user_profile.predicted_jobs()

    def submit(self):
        """
        Handles the action of pressing the submit button
        """
        url = self.interface.input_url.text()
        print(f"User input url: {url}")

        if not validate_profile_url(url):
            self.interface.lbl_invalid.setVisible(True)
        else:
            # Disable submission screen

            # Create progress bar window
            self.progress_bar = progress_bar = ProgressBar(title="Collecting user information", num_steps=5)

            # Create thread for data collection
            self.thread = thread = SubmissionThread(url)

            # Init empty user profile
            self.user_profile = UserProfile("None", "None", [], [])

            # Setup thread connections
            thread.change_value.connect(self.set_progress)
            thread.result.connect(self.set_profile)
            thread.finished.connect(progress_bar.window.close)
            thread.finished.connect(self.scrape_careers)
            thread.finished.connect(thread.quit)
            thread.finished.connect(thread.deleteLater)

            # Start thread
            thread.start()

            # Reset
            self.window.setEnabled(False)
            thread.finished.connect(
                lambda: self.window.setEnabled(True)
            )

    def exit(self):
        """
        Handles the action of pressing the exit button
        """
        self.application.exit()


def get_user_profile(url: str, signal: pyqtSignal) -> UserProfile:
    """
    Scrapes LinkedIn for user information from a given profile URL
    :param url: The user's profile URL
    :param signal: Used to relay progress back to the main thread
    :return: A user profile object
    """

    signal.emit("Loading user's profile...", 0)

    # Init empty user profile
    user_profile = UserProfile("None", "None", [], [])

    # Start Chrome Webdriver and Login
    driver: WebDriver
    try:
        driver = configure_driver(ApplicationSettings.DRIVER_PATH, ApplicationSettings.IS_HEADLESS)
    except SessionNotCreatedException:
        print("ChromeDriver is out of date.")
        sys.exit(1)
    except WebDriverException:
        print("Web driver path is invalid.")
        signal.emit("Error :(", 5)
        sys.exit(1)

    login(driver)

    # Go to user's profile page
    driver.get(url)

    # Get user's name
    signal.emit("Scraping user's name...", 1)
    name = get_user_name(driver)

    if not name:
        print("Web page is not a valid LinkedIn user profile")
        signal.emit("Error :(", 5)
        driver.close()
        return user_profile

    profile_section = get_profile_section(driver)
    if not profile_section:
        print("User profile has no profile section")
        signal.emit("Error :(", 5)
        driver.close()
        return user_profile

    signal.emit("Scraping user's bio...", 2)
    bio = get_user_bio(profile_section)

    signal.emit("Scraping user's work experiences...", 3)
    work_experience = get_user_work_experiences(driver, profile_section)

    signal.emit("Scraping user's skills...", 4)
    skills = get_user_skills(driver, profile_section)

    # Make sure to close the driver
    driver.close()
    signal.emit("Finished!", 5)

    return UserProfile(name=name, bio=bio, work_experiences=work_experience, skills=skills)


def get_user_name(driver) -> str | None:
    """
    Grabs the user's
    :param driver:
    :return:
    """
    try:
        name = driver.find_element(By.CLASS_NAME, 'text-heading-xlarge.inline.t-24.v-align-middle.break-words').text
        return name
    except NoSuchElementException:
        print("Invalid user profile page.")
        return None


def get_user_bio(profile_section) -> str:
    """
    Gets the user's bio from LinkedIn
    :param profile_section:
    :return: the user's bio
    """

    try:
        bio = profile_section.find_element(
            By.CLASS_NAME, 'inline-show-more-text.inline-show-more-text--is-collapsed.mt4.t-14').text
        bio = bio.replace('…\nsee more', '')
        return bio
    except NoSuchElementException:
        print("This user doesn't have a bio.")
        return "No bio."


def get_user_work_experiences(driver, profile_section) -> List[WorkExperience]:
    """
    Gets the user's work experiences from LinkedIn
    :param driver:
    :param profile_section:
    :return: A list of the user's work experiences
    """
    experiences_list: List[WorkExperience] = []

    experience_section = scroll_until_find_by_class_name(class_name='pv-profile-section.experience-section.ember-view',
                                                         driver=driver, parent=profile_section)
    if experience_section:
        experiences_list_element = experience_section.find_element(
            By.CLASS_NAME,
            'pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more')
        experiences_list_li_elements = experiences_list_element.find_elements(By.CSS_SELECTOR, 'li')

        for list_element in experiences_list_li_elements:
            title = list_element.find_element(By.CLASS_NAME, 't-16.t-black.t-bold').text
            description: str
            try:
                description = list_element.find_element(
                    By.CLASS_NAME,
                    'inline-show-more-text.inline-show-more-text--is-collapsed.pv-entity__description.t-14.t-black.t-normal').text
                description = description.replace('…\nsee more', '')
            except NoSuchElementException:
                description = "No description."

            experiences_list.append(WorkExperience(title, description))

        return experiences_list

    else:
        print("User doesn't have any work experiences")
        return []


def get_user_skills(driver, profile_section) -> List[str]:
    """
    Gets the user's skills from LinkedIn
    :param driver:
    :param profile_section:
    :return: A list of the user's skills
    """
    # Get user's skills
    skills_list: List[str] = []

    skills_section = scroll_until_find_by_class_name(
        class_name='pv-profile-section.pv-skill-categories-section.artdeco-card.mt4.p5.ember-view', driver=driver,
        parent=profile_section)

    if skills_section:
        skills_show_more_button = scroll_until_find_by_class_name(
            class_name='pv-profile-section__card-action-bar.pv-skills-section__additional-skills.artdeco-container-card-action-bar.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--fluid.artdeco-button--muted',
            driver=driver, parent=skills_section)
        skills_show_more_button.click()

        # Top 3 Skills listed
        skills_top_list_element = skills_section.find_element(
            By.CLASS_NAME, 'pv-skill-categories-section__top-skills.pv-profile-section__section-info.section-info.pb1')
        skills_top_list_li_elements = skills_top_list_element.find_elements(By.CSS_SELECTOR, 'li')
        # The rest of the skills
        skills_extra_list_element = skills_section.find_element(By.ID, 'skill-categories-expanded')
        skills_extra_list_li_elements = skills_extra_list_element.find_elements(By.CSS_SELECTOR, 'li')

        # Agglomerate all skill li elements
        all_skills_li_elements = []
        [all_skills_li_elements.append(s) for s in skills_top_list_li_elements]
        [all_skills_li_elements.append(s) for s in skills_extra_list_li_elements]

        # Store all skill text elements in a list
        all_skills_elements = []

        [
            [
                all_skills_elements.append(skill)
                if skill.get_attribute('class') == 'pv-skill-category-entity__name-text t-16 t-black t-bold'
                else None
                for skill in skills.find_elements(By.CSS_SELECTOR, '*')
            ]
            for skills in all_skills_li_elements
        ]

        [skills_list.append(s.text) for s in all_skills_elements]

        return skills_list

    else:
        print("User doesn't have any skills listed")
        return []


def get_profile_section(driver) -> WebElement | None:
    """
    Gets the profile section WebElement on a user's LinkedIn profile page
    :param driver:
    :return: The profile section WebElement object
    """
    section: WebElement
    try:
        section = driver.find_element(By.CLASS_NAME, 'profile-detail')
        return section
    except NoSuchElementException:
        print("No profile section found")
        return None
