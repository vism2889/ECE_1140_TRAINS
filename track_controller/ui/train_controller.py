from  PyQt5 import QtWidgets
from main_window import TrainControllerWindow


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    ui = TrainControllerWindow()
    ui.setupUi(w)
    ui.setBlockState('red', 71, True)
    w.show()
    sys.exit(app.exec_())