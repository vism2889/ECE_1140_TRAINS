from  PyQt5 import QtWidgets
from main_window import Ui_main_window


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    ui = Ui_main_window()
    ui.setupUi(w)
    w.show()
    sys.exit(app.exec_())