#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/13/2022
# FILENAME: signalReciever.py
# DESCRIPTION:
#   Test case for Signals.py: listens to occupancySignal
##############################################################################

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class signalReciever(QMainWindow):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        self.occupancy = []
        self.signals.occupancySignal.connect(self.printOccupancy)

        self.setWindowTitle("Signal Reciever ")
        self.setGeometry(100, 100, 400, 600)
        self.show()

    def printOccupancy(self, occupancy):
        print("OCCUPANCY RECIEVED IN Signal Reciever:", end=None)
        print(occupancy)
