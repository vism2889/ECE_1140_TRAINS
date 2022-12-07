## System pathing
import sys

sys.path.append('track_layout')
sys.path.append("../../SystemSignals")

## PyQt comms and widgets
from  PyQt5 import QtWidgets
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
        self.active = False

        ## Logger
        format = '[%(asctime)s] %(name)s (%(levelname)s): %(message)s'
        logging.basicConfig(format=format, level=logging.DEBUG,
                            filename='logs/waysidecontroller.log', filemode='w')
        logger = logging.getLogger('WAYSIDE-MODULE')
        logger.setLevel(logging.DEBUG)

        ## Main Wayside Controller class
        wayside = WaysideIO(signals, logger)

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
        self.active = True

## Commandline CTRL-C ##
def handler(signum, frame):
    print("CTRL-C was pressed")
    exit(1)

signal.signal(signal.SIGINT, handler)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) ## COMMENT OUT FOR FINAL PRODUCT
    signals = Signals() ## COMMENT OUT FOR FINAL PRODUCT
    wayside = WaysideController(signals)

    ## Testing
    blockFailures = []
    for i in range(150):
        blockFailures.append(0)

    blockFailures[0] = 0x01
    blockFailures[5] = 0x03
    blockFailures[149] = 0x02
    signals.blockFailures.emit(blockFailures)

    ## Exit
    sys.exit(app.exec_()) ## COMMENT OUT FOR FINAL PRODUCT