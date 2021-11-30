import webbrowser
from typing import List

from PyQt5 import QtWidgets

from models.career import Career
from user_interfaces.ui_jobs import Ui_Jobs


class SkillJobs:
    """
    Handles the creation and logic for the Skill Job UI
    """

    def __init__(self, data: List[Career], skill: str, *args):
        self.window = window = QtWidgets.QDialog()
        self.interface = interface = Ui_Jobs()
        interface.setupUi(window)

        self.interface.jobTable.verticalHeader().setVisible(False)
        self.interface.skill_label.setText(skill)
        self.interface.goBackButton.clicked.connect(self.go_back_button_clicked)

        self.data = data

        self.setData()

        window.show()

    def setData(self):
        self.interface.jobTable.setRowCount(len(self.data))
        index = 0
        for career in self.data:
            job = career.occupation
            newitem = QtWidgets.QTableWidgetItem(job)
            viewButton = QtWidgets.QPushButton('View Online')
            viewButton.clicked.connect(self.view_button_clicked)
            self.interface.jobTable.setItem(index, 0, newitem)
            self.interface.jobTable.setCellWidget(index, 1, viewButton)
            index += 1

    def view_button_clicked(self):
        button = self.window.sender()
        index = self.interface.jobTable.indexAt(button.pos())
        if index.isValid():
            url = "https://www.onetonline.org/link/summary/" + self.data[index.row()].code
            webbrowser.open(url)

    def go_back_button_clicked(self):
        self.window.close()
