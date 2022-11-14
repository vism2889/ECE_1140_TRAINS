#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/13/2022
# FILENAME: launchComms.py
# DESCRIPTION:
#   Used to luanch TrackModel UI and to launch the occupancySignalSender module
#   for testing.
##############################################################################

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
from TrackModelApp import TrackModel
from occupancySignalSender import SendOccupancy
sys.path.append("..\..\SystemSignals") # tell interpreter where to look for model files
from Signals import Signals

class signalTestMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals         = Signals()
        self.TrackModelUI    = TrackModel(self.signals)
        self.occupancySender = SendOccupancy(self.signals)

App = QApplication(sys.argv)
x   = signalTestMain()

sys.exit(App.exec())