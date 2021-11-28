from PyQt5 import QtWidgets
from user_interfaces.ui_skills import Ui_LinkedInSkills
from skilljobs import SkillJobs

class Skills:
    """
    Handles the creation and logic for the Skill List GUI
    """

    def __init__(self, data: dict, *args):
        self.window = window = QtWidgets.QDialog()
        self.interface = interface = Ui_LinkedInSkills()
        interface.setupUi(window)

        self.interface.skillTable.verticalHeader().setVisible(False)

        self.data = data

        self.set_data()

        window.show()

    def set_data(self):
        self.interface.skillTable.setRowCount(len(self.data))
        for n, key in enumerate(sorted(self.data.keys())):
            newitem = QtWidgets.QTableWidgetItem(key)
            view_button = QtWidgets.QPushButton('View Jobs')
            view_button.clicked.connect(self.view_button_clicked)
            self.interface.skillTable.setItem(n, 0, newitem)
            self.interface.skillTable.setCellWidget(n, 1, view_button)

    def view_button_clicked(self):
        button = self.window.sender()
        index = self.interface.skillTable.indexAt(button.pos())
        if index.isValid():
            key = list(self.data)[index.row()]
            self.skill_jobs = SkillJobs(data=self.data[key], skill=key)
