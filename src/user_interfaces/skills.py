# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skills.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LinkedInSkills(object):
    def setupUi(self, LinkedInSkills):
        LinkedInSkills.setObjectName("LinkedInSkills")
        LinkedInSkills.resize(260, 453)
        self.scrollArea = QtWidgets.QScrollArea(LinkedInSkills)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 241, 431))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 239, 429))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.skillTable = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.skillTable.setGeometry(QtCore.QRect(0, 0, 241, 431))
        self.skillTable.setObjectName("skillTable")
        self.skillTable.setColumnCount(2)
        self.skillTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.skillTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.skillTable.setHorizontalHeaderItem(1, item)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(LinkedInSkills)
        QtCore.QMetaObject.connectSlotsByName(LinkedInSkills)

    def retranslateUi(self, LinkedInSkills):
        _translate = QtCore.QCoreApplication.translate
        LinkedInSkills.setWindowTitle(_translate("LinkedInSkills", "Skills"))
        item = self.skillTable.horizontalHeaderItem(0)
        item.setText(_translate("LinkedInSkills", "Skill"))
        item = self.skillTable.horizontalHeaderItem(1)
        item.setText(_translate("LinkedInSkills", "Action"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LinkedInSkills = QtWidgets.QDialog()
    ui = Ui_LinkedInSkills()
    ui.setupUi(LinkedInSkills)
    LinkedInSkills.show()
    sys.exit(app.exec_())
