from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from application_settings import ApplicationSettings
from helper_methods.driver_helper import configure_driver, scroll_until_find_by_class_name
from helper_methods.linkedin_helper import validate_profile_url, PROFILEURL as LINKEDIN_PROFILEURL, \
    EXAMPLEURL as LINKEDIN_EXAMPLEURL, login
from progress_bar import ProgressBar
from user_interfaces.ui_linkedin_input import Ui_LinkedInInput
from models.user_profile import UserProfile
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

    def print_profile(self):
        """
        Prints the current user profile
        """
        self.user_profile.print_profile()

    def submit(self):
        """
        Handles the action of pressing the submit button
        """
        url = self.interface.input_url.text()
        print(f"User input url: {url}")

        if not validate_profile_url(url):
            self.interface.lbl_invalid.setVisible(True)
        else:
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
            thread.finished.connect(self.print_profile)
            thread.finished.connect(thread.quit)
            thread.finished.connect(thread.deleteLater)

            # Start thread
            thread.start()

    def exit(self):
        """
        Handles the action of pressing the exit button
        """
        self.application.exit()


# TODO Refactor to use helper methods
def get_user_profile(url: str, signal: pyqtSignal) -> UserProfile:
    signal.emit("Loading user's profile...", 1)

    # Start Chrome Webdriver and Login
    driver = configure_driver(ApplicationSettings.DRIVER_PATH, ApplicationSettings.IS_HEADLESS)

    user_profile = UserProfile("None", "None", [], [])

    try:
        login(driver)
        # Go to user's profile page
        driver.get(url)

        signal.emit("Scraping user's name...", 2)
        # Get user's name
        name = driver.find_element(By.CLASS_NAME, 'text-heading-xlarge.inline.t-24.v-align-middle.break-words').text

        signal.emit("Scraping user's bio...", 3)
        # Get user's bio
        profile_section = driver.find_element(By.CLASS_NAME, 'profile-detail')
        bio: str = ""
        try:
            bio = profile_section.find_element(
                By.CLASS_NAME, 'inline-show-more-text.inline-show-more-text--is-collapsed.mt4.t-14').text
            bio = bio.replace('…\nsee more', '')
        except NoSuchElementException:
            print("This user doesn't have a bio.")

        signal.emit("Scraping user's work experiences...", 3)
        # Get user's work experiences
        experiences_list: List[WorkExperience] = []

        experience_section = scroll_until_find_by_class_name(
            class_name='pv-profile-section.experience-section.ember-view',
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

        else:
            print("User doesn't have any work experiences")

        signal.emit("Scraping user's skills...", 4)
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
                By.CLASS_NAME,
                'pv-skill-categories-section__top-skills.pv-profile-section__section-info.section-info.pb1')
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

        else:
            print("User doesn't have any skills listed")

        user_profile = UserProfile(name=name, bio=bio, work_experiences=experiences_list, skills=skills_list)

    except NoSuchElementException:
        print("User page doesn't exist.")
    finally:
        # Make sure to close the driver
        driver.close()
        signal.emit("Finished!", 5)

    return user_profile
