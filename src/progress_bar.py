from PyQt5 import QtWidgets
from user_interfaces.ui_progress_bar import Ui_ProgressBar


class ProgressBar:
    """
    Handles the creation and logic for the Progress Bar GUI
    """

    def __init__(self, title: str, num_steps: int):
        self.window = window = QtWidgets.QDialog()
        self.interface = interface = Ui_ProgressBar()
        interface.setupUi(window)

        window.setWindowTitle(title)
        interface.bar_progress.setMaximum(num_steps)

        window.show()

    def set_progress(self, info: str, step: int):
        """
        Updates the Progress Bar UI to reflect the current progress
        :param info: information on the current step
        :param step: the current step
        """
        self.interface.bar_progress.setValue(step)
        self.interface.lbl_status.setText(info)
