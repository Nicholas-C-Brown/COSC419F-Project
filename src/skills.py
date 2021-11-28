from PyQt5 import QtWidgets
from user_interfaces.skills import Ui_LinkedInSkills


class Skills:
    """
    Handles the creation and logic for the Skill List GUI
    """

    def __init__(self, data: list, *args):
        self.window = window = QtWidgets.QDialog()
        self.interface = interface = Ui_LinkedInSkills()
        interface.setupUi(window)

        self.data = data

        self.setData()

        window.show()

    def setData(self):
        self.interface.skillTable.setRowCount(len(self.data))
        for n, key in enumerate(sorted(self.data.keys())):
            newitem = QtWidgets.QTableWidgetItem(key)
            viewButton = QtWidgets.QPushButton('View Jobs')
            viewButton.clicked.connect(self.view_button_clicked)
            self.interface.skillTable.setItem(n, 0, newitem)
            self.interface.skillTable.setCellWidget(n, 1, viewButton)

    def view_button_clicked(self):
        button = self.window.sender()
        index = self.interface.skillTable.indexAt(button.pos())
        if index.isValid():
            print(index.row())
