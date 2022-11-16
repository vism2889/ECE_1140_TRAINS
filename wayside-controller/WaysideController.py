from  PyQt5 import QtWidgets
import sys
import os

from ui.WaysideUI import TrackControllerWindow
from WaysideIO.WaysideIO import WaysideIO
from ui.WCTestWindow import Ui_test_window
from track_layout import extract_layout

if __name__ == '__main__':

    wayside = WaysideIO()

    ## UI 
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    main = TrackControllerWindow(wayside)
    main.setupUi(w)
    w.show()

    ## Set UI reference 
    wayside.setUI(main)

    path = os.getcwd()
    jsonPath = os.getcwd()

    wayside.setBlockOccupancy('green', 150, True)
    # wayside.setFaults('green', 150, [1])

    wayside.setBlockMaintenance('green', 150, True)
    wayside.setSwitch('green',63, True)
    wayside.setCrossing('green', 19, True)
    ## Exit 
    sys.exit(app.exec_())
    

    