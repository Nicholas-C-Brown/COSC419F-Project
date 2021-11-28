import sys
from PyQt5 import QtWidgets
from linkedin_input import LinkedInInput

# APPLICATION START
app = QtWidgets.QApplication(sys.argv)
linkedin_input = LinkedInInput(app)
app.exec_()
print("Done")

