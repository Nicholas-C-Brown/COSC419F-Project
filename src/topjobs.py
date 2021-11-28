import webbrowser
from typing import List

from PyQt5 import QtWidgets

from models.career import Career
from user_interfaces.ui_top_jobs import Ui_TopJobs


class TopJobs:
    """
    Handles the creation and logic for the Top Job list GUI
    """

    def __init__(self, data: List[Career], *args):
        self.window = window = QtWidgets.QDialog()
        self.interface = interface = Ui_TopJobs()
        interface.setupUi(window)

        self.interface.tableWidget.verticalHeader().setVisible(False)

        self.data = data

        self.set_data()

        window.show()

    def set_data(self):
        self.interface.tableWidget.setRowCount(len(self.data))
        index = 0
        for career in self.data:
            job = career.occupation
            newitem = QtWidgets.QTableWidgetItem(job)
            view_button = QtWidgets.QPushButton('View Online')
            view_button.clicked.connect(self.view_button_clicked)
            self.interface.tableWidget.setItem(index, 0, newitem)
            self.interface.tableWidget.setCellWidget(index, 1, view_button)
            index += 1

    def view_button_clicked(self):
        button = self.window.sender()
        index = self.interface.tableWidget.indexAt(button.pos())
        if index.isValid():
            url = "https://www.onetonline.org/link/summary/" + self.data[index.row()].code
            webbrowser.open(url)
