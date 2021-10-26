from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from helper_methods.driver_helper import scroll_until_find_by_class_name
from models.work_experience import WorkExperience


class UserProfile:
    name: str
    bio: str
    skills = List[str]
    work_experiences = List[WorkExperience]

    def __init__(self, name: str, bio: str, work_experiences: List[WorkExperience], skills: List[str]):
        self.name = name
        self.bio = bio
        self.work_experiences = work_experiences
        self.skills = skills

# TODO Needs unit test
    def experiences_to_string(self) -> str:
        s = ""
        for experience in self.work_experiences:
            s += "  -" + experience.title + "\n" + experience.desc + "\n\n"
        return s

# TODO Needs unit test
    def skills_to_string(self) -> str:
        s = ""
        for skill in self.skills:
            s += "  -" + skill + "\n"
        return s

    def print_profile(self):
        print("-----------------------------------\n")
        print("Name: " + self.name)
        print("About: " + self.bio)
        print("Work Experience:")
        print(self.experiences_to_string())
        print("Skills: ")
        print(self.skills_to_string())
        print("-----------------------------------\n")


def get_user_profile(url: str, driver: WebDriver) -> UserProfile:
    # Go to user's profile page
    driver.get(url)

    # Get user's name
    name = driver.find_element(By.CLASS_NAME('text-heading-xlarge.inline.t-24.v-align-middle.break-words')).text

    # Get user's bio
    profile_section = driver.find_element(By.CLASS_NAME('profile-detail'))
    bio: str = ""
    try:
        bio = profile_section.find_element(
            By.CLASS_NAME('inline-show-more-text.inline-show-more-text--is-collapsed.mt4.t-14')).text
        bio = bio.replace('…\nsee more', '')
    except NoSuchElementException:
        print("This user doesn't have a bio.")

    # Get user's work experiences
    experiences_list: List[WorkExperience] = []

    experience_section = scroll_until_find_by_class_name(class_name='pv-profile-section.experience-section.ember-view',
                                                         driver=driver, parent=profile_section)
    if experience_section:
        experiences_list_element = experience_section.find_element(
            By.CLASS_NAME('pv-profile-section__section-info.section-info.pv-profile-section__section-info--has-no-more'))
        experiences_list_li_elements = experiences_list_element.find_elements(By.CSS_SELECTOR('li'))

        for li in experiences_list_li_elements:
            title = li.find_element(By.CLASS_NAME('t-16.t-black.t-bold')).text
            description: str
            try:
                description = li.find_element(
                    By.CLASS_NAME('inline-show-more-text.inline-show-more-text--is-collapsed.pv-entity__description.t-14.t-black.t-normal')).text
                description = description.replace('…\nsee more', '')
            except NoSuchElementException:
                description = "No description."

            experiences_list.append(WorkExperience(title, description))

    else:
        print("User doesn't have any work experiences")

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
            By.CLASS_NAME('pv-skill-categories-section__top-skills.pv-profile-section__section-info.section-info.pb1'))
        skills_top_list_li_elements = skills_top_list_element.find_elements(By.CSS_SELECTOR('li'))
        # The rest of the skills
        skills_extra_list_element = skills_section.find_element(By.ID('skill-categories-expanded'))
        skills_extra_list_li_elements = skills_extra_list_element.find_elements(By.CSS_SELECTOR('li'))

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
                for skill in skills.find_elements(By.CSS_SELECTOR('*'))
            ]
            for skills in all_skills_li_elements
        ]

        [skills_list.append(s.text) for s in all_skills_elements]

    else:
        print("User doesn't have any skills listed")

    return UserProfile(name=name, bio=bio, work_experiences=experiences_list, skills=skills_list)
