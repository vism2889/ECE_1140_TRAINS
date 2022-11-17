# This Python file uses the following encoding: utf-8
import sys
from  PyQt5 import QtWidgets

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_test_window
from main_window import TrackControllerWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w_main = QtWidgets.QWidget()
    w_test = QtWidgets.QWidget()
    main = TrackControllerWindow()
    main.setupUi(w_main)

    test = Ui_test_window(main)
    test.setupUi(w_test)
    w_main.show()
    w_test.show()

    sys.exit(app.exec())
