# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from old_uiform import Ui_test_window
from main_window import TrackControllerWindow

class test_window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        w = QWidget()
        main_window = TrackControllerWindow()
        main_window.setupUi(w)
        w.show()

        self.ui = Ui_test_window(main_window)
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = test_window()
    widget.show()

    sys.exit(app.exec())
