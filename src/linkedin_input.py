import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from models.application_settings import ApplicationSettings
from models.user_profile import get_user_profile
from helper_methods.linkedin_helper import validate_profile_url, PROFILEURL as LINKEDIN_PROFILEURL, EXAMPLEURL as LINKEDIN_EXAMPLEURL, login
from helper_methods.driver_helper import configure_driver
from user_interfaces.ui_linkedin_input import Ui_LinkedInInput


class LinkedInInput:

    def __init__(self, settings: ApplicationSettings, application: QApplication):
        self.settings = settings
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

    def submit(self):
        url = self.interface.input_url.text()
        print(url)

        if not validate_profile_url(url):
            self.interface.lbl_invalid.setVisible(True)
        else:
            # Start Chrome Webdriver and Login
            driver = configure_driver(self.settings.driver_path, self.settings.is_headless)
            login(driver)

            user_profile = get_user_profile(url, driver)

            user_profile.print_profile()

    def exit(self):
        self.application.exit()
