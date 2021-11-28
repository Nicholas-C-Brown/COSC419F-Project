import heapq

from typing import List
from models.career import Career
from models.work_experience import WorkExperience


class UserProfile:
    """
    Holds the information of a LinkedIn User
    """
    name: str
    bio: str
    skills = List[str]
    work_experiences = List[WorkExperience]
    career_dict: dict = {}

    def __init__(self, name: str, bio: str, work_experiences: List[WorkExperience], skills: List[str]):
        self.name = name
        self.bio = bio
        self.work_experiences = work_experiences
        self.skills = skills

    def experiences_to_string(self) -> str:
        """
        Converts the User's work experiences list to a string.

        :return: A string consisting all of the User's work experiences
        """
        string = ""
        for experience in self.work_experiences:
            string += "  -" + experience.title + "\n" + experience.desc + "\n\n"
        return string

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

    def print_career_dict(self):
        """
        Prints the User's career dictionary information to the console
        """
        for skill, career_list in self.career_dict.items():
            for career in career_list:
                print("Skill: " + skill + " - " + career.to_string())

    def predicted_jobs(self, number_predicts: int = 5, frequency_factor: int = 0.5):
        """
        Predicts relevant jobs for the user based off of their career dictionary
        :param number_predicts: The number of jobs to predict
        :param frequency_factor: The relative weighting factor for how many times a given career appears in the dictionary
        """
        occupation_dict = {}

        num_skills = len(self.career_dict)

        # Iterate through every occupation for each skill and calculates the total weighting based on frequency
        for career_list in self.career_dict.values():
            for career in career_list:
                if career.occupation in occupation_dict.keys():
                    occupation_dict[career.occupation] += frequency_factor * num_skills + career.weight
                else:
                    occupation_dict[career.occupation] = frequency_factor * num_skills + career.weight

        predictions = heapq.nlargest(number_predicts, occupation_dict, key=occupation_dict.get)
        for prediction in predictions:
            print(prediction)


def normalize_weights(career_dict: dict):
    """
    Normalizes all career weights in a career dictionary
    :param career_dict:
    """
    for value in career_dict.values():
        normalize_skill_weights(value)


def normalize_skill_weights(careers: List[Career]):
    """
    Normalizes the weights for the careers in a given list
    :param careers:
    """

    # Calculate the total weight
    total_weight = 0
    for career in careers:
        total_weight += career.weight

    # Average weight
    average_weight = total_weight / len(careers)

    # Normalize weights by dividing by the average weight
    for career in careers:
        career.weight /= average_weight
