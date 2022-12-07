from  PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QWidget
import sys
import os
sys.path.append('track_layout')
sys.path.append("../../SystemSignals")
from Signals import Signals

from ui.WaysideUI import TrackControllerWindow
from WaysideIO.WaysideIO import WaysideIO
from ui.WCTestWindow import Ui_test_window
# from track_layout import extract_layout

class WaysideController():
    def __init__(self, signals=None, launchTestWindow=False):
    
        wayside = WaysideIO(signals)
        ## UI
        
        w = QtWidgets.QWidget()
        wTest = QtWidgets.QWidget()
        main = TrackControllerWindow(wayside)
        main.setupUi(w)

        if launchTestWindow: 
            test = Ui_test_window(main)
            test.setupUi(wTest)
            w.show()
            wTest.show()
        else:
            w.show()

        ## Set UI reference
        wayside.setUI(main)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) ## COMMENT OUT FOR FINAL PRODUCT
    signals = Signals() ## COMMENT OUT FOR FINAL PRODUCT
    WaysideController(signals)

    blockFailures = []
    for i in range(150): 
        blockFailures.append(0)
    
    signals.blockFailures.emit(blockFailures)

    ## Exit
    sys.exit(app.exec_()) ## COMMENT OUT FOR FINAL PRODUCT