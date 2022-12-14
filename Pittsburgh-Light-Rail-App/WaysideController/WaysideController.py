## System pathing
import sys

sys.path.append('track_layout')
sys.path.append("../../SystemSignals")

## PyQt comms and widgets
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
if __name__ == '__main__': from Signals import Signals
## Wayside controller library
from ui.WaysideUI import TrackControllerWindow
from WaysideIO.WaysideIO import WaysideIO
from ui.WCTestWindow import Ui_test_window

## Logging
import logging

## Interupts
import signal

class WaysideController():
    def __init__(self, signals, launchTestWindow=False):

        ## Logger
        format = '[%(asctime)s] %(name)s (%(levelname)s): %(message)s'
        logging.basicConfig(format=format, level=logging.INFO,
                            filename='logs/waysidecontroller.log', filemode='w')
        logger = logging.getLogger('WAYSIDE-MODULE')
        logger.setLevel(logging.DEBUG)

        ## Main Wayside Controller class
        wayside = WaysideIO(signals)

        ## UI
        self.w = QtWidgets.QWidget()
        wTest = QtWidgets.QWidget()
        self.main = TrackControllerWindow(wayside)
        self.main.setupUi(self.w)

        ## Set UI reference
        wayside.setUI(self.main)

    def show(self):
        self.w.show()

## Commandline CTRL-C ##
def handler(signum, frame):
    print("CTRL-C was pressed")
    exit(1)

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) ## COMMENT OUT FOR FINAL PRODUCT
    signals = Signals() ## COMMENT OUT FOR FINAL PRODUCT
    wayside = WaysideController(signals)
    wayside.show()

    signals.trainLocation.emit(['green', 0, 84, 85])

    ## Testing
    # blockFailures = []
    # for i in range(76):
    #     blockFailures.append(0)

    # while True:
    #     key = input("Hit Enter: ")
    #     if key == 'q':
    #         exit(0)
    #         sys.exit(app.exec_()) ## COMMENT OUT FOR FINAL PRODUCT

    #     blockFailures[0] = 0x01
        # blockFailures[98] = 0x03
        # blockFailures[149] = 0x02
        # signals.blockFailures.emit(blockFailures)

    ## Exit
    sys.exit(app.exec_()) ## COMMENT OUT FOR FINAL PRODUCT