import sys
from PyQt5 import QtWidgets

from models.application_settings import ApplicationSettings
from linkedin_input import LinkedInInput

DRIVER_PATH = 'assets/driver/chromedriver.exe'
IS_HEADLESS = True

# APPLICATION START
app = QtWidgets.QApplication(sys.argv)
settings = ApplicationSettings(DRIVER_PATH, IS_HEADLESS)

linkedin_input = LinkedInInput(settings, app)
app.exec_()
