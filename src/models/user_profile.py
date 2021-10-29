
from typing import List
from models.work_experience import WorkExperience


class UserProfile:
    """
    Holds the information of a LinkedIn User
    """
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
        """
        Converts the User's work experiences list to a string.

        :return: A string consisting all of the User's work experiences
        """
        string = ""
        for experience in self.work_experiences:
            string += "  -" + experience.title + "\n" + experience.desc + "\n\n"
        return string

    # TODO Needs unit test
    def skills_to_string(self) -> str:
        """
        Converts the User's skills list to a string.

        :return: A string consisting all of the User's skills
        """
        string = ""
        for skill in self.skills:
            string += "  -" + skill + "\n"
        return string

    def print_profile(self):
        """
        Prints the User's information to the console.
        """
        print("-----------------------------------\n")
        print("Name: " + self.name)
        print("About: " + self.bio)
        print("Work Experience:")
        print(self.experiences_to_string())
        print("Skills: ")
        print(self.skills_to_string())
        print("-----------------------------------\n")
