#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/13/2022
# FILENAME: signalTestMain.py
# DESCRIPTION:
#   Test case for Signals.py: Launches signalSender.py and signalReciever.py to
#   test signal communications.
##############################################################################

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
from Signals import Signals

from signalReciever import signalReciever
from signalSender import signalSender

class signalTestMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals  = Signals()
        self.senderr  = signalSender(self.signals)
        self.reciever = signalReciever(self.signals)

App = QApplication(sys.argv)
x   = signalTestMain()

sys.exit(App.exec())