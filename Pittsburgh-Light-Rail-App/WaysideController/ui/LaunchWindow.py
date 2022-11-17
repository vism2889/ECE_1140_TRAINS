from  PyQt5 import QtWidgets
from WaysideUI import TrackControllerWindow


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    ui = TrackControllerWindow()
    ui.setupUi(w)
    
    w.show()
    sys.exit(app.exec_())