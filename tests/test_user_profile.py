import os.path
import unittest
import sys

sys.path.append(os.path.join(sys.path[0], '../src'))
from models.user_profile import UserProfile
from models.work_experience import WorkExperience


class TestUserProfile(unittest.TestCase):

    def setUp(self):
        skills = ["Python", "Unit Testing", "HTML"]
        work_experience_1 = WorkExperience("Software Developer", "Made Minecraft in it's entirety.")
        work_experience_2 = WorkExperience("Cashier", "Served burger.")
        work_experiences = [work_experience_1, work_experience_2]

        self.user_profile = UserProfile("Joe Doe", "Your average Joe.", work_experiences, skills)

    def test_experiences_to_string(self):
        expected = f"  -Software Developer\n" \
                   f"Made Minecraft in it's entirety.\n\n" \
                   f"  -Cashier\n" \
                   f"Served burger.\n\n"
        actual = self.user_profile.experiences_to_string()
        self.assertEqual(expected, actual)

    def test_skills_to_string(self):
        expected = "  -Python\n" \
                   "  -Unit Testing\n" \
                   "  -HTML\n"
        actual = self.user_profile.skills_to_string()
        self.assertEqual(expected, actual)


# Run tests by running the python file
if __name__ == '__main__':
    unittest.main()
