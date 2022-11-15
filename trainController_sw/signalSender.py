#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/13/2022
# FILENAME: signalSender.py
# DESCRIPTION:
#   Test case for Signals.py: emits to occupancySignal
##############################################################################

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 


class signalSender(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        
        # Outputs to Train Model
        self.powerSignal = 0
        self.lightSignal = [False, False]
        self.doorSignal = [False, False]
        self.temperatureSignal = 72.0
        self.announcementsSignal = False
        self.advertisementsSignals = False
        self.serviceBrakeSignal = False
        self.emergencyBrakeSignal = False
        
        

        self.occupancy = [True, False, True, False]

        self.pb = QPushButton("EMIT", self)
        self.pb.setGeometry(125, 100, 150, 50)
        self.pb.clicked.connect(self.emit)
        self.setWindowTitle("Signal Sender")
        self.setGeometry(100, 100, 400, 600)
        
        self.show()
    
    def emit(self):
        print("Emitting From Signal Sender")
        self.signals.occupancySignal.emit(self.occupancy)