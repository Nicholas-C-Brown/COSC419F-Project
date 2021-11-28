from PyQt5 import QtWidgets
from user_interfaces.top_jobs import Ui_top_jobs


class Top_Jobs:
    """
    Handles the creation and logic for the Top Job list GUI
    """

    def __init__(self, data: list, *args):
        self.window = window = QtWidgets.QDialog()
        self.interface = interface = Ui_top_jobs()
        interface.setupUi(window)

        self.interface.tableWidget.verticalHeader().setVisible(False)

        self.data = data

        self.setData()

        window.show()

    def setData(self):
        self.interface.tableWidget.setRowCount(len(self.data))
        for n, key in enumerate(sorted(self.data.keys())):
            job = self.data[key][0]
            newitem = QtWidgets.QTableWidgetItem(job)
            viewButton = QtWidgets.QPushButton('View Online')
            viewButton.clicked.connect(self.view_button_clicked)
            self.interface.tableWidget.setItem(n, 0, newitem)
            self.interface.tableWidget.setCellWidget(n, 1, viewButton)

    def view_button_clicked(self):
        button = self.window.sender()
        index = self.interface.tableWidget.indexAt(button.pos())
        if index.isValid():
            print(self.data[index.row()])
