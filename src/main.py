import sys
from PyQt5 import QtWidgets
from linkedin_input import LinkedInInput

# APPLICATION START
app = QtWidgets.QApplication(sys.argv)
linkedin_input = LinkedInInput(app)
app.exec_()
print("Done")


# from skillset_scraper import scrape_user_skills
# from user_profile import UserProfile, normalize_weights
# from work_experience import WorkExperience
#
# name = "John"
# bio = "A dude."
# skills = ["java", "php", "construction"]
# work_experiences = [WorkExperience("Software Developer", "None")]
#
# user = UserProfile(name, bio, work_experiences, skills)
#
# user.career_dict = scrape_user_skills(user)
# normalize_weights(user.career_dict)
# user.print_career_dict()
# user.predicted_jobs()
