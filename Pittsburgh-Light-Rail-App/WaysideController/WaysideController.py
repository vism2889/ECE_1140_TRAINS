from  PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QWidget
import sys
import os

from ui.WaysideUI import TrackControllerWindow
from WaysideIO.WaysideIO import WaysideIO
# from ui.WCTestWindow import Ui_test_window
# from track_layout import extract_layout

class WaysideController():
    def __init__(self, signals):

        wayside = WaysideIO(signals)
        ## UI
        # app = QtWidgets.QApplication(sys.argv)
        w = QtWidgets.QWidget()
        main = TrackControllerWindow(wayside)
        main.setupUi(w)
        w.show()

        ## Set UI reference
        wayside.setUI(main)

        ## Exit
        # sys.exit(app.exec_())


if __name__ == '__main__':
    WaysideController()