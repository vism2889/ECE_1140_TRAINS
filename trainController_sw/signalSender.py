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
        self.powerSignal = [10]
        self.lightSignal = [True, True]
        self.doorSignal = [False, False]
        self.temperatureSignal = [72.0]
        self.announcementsSignal = [False]
        self.advertisementsSignals = [False]
        self.serviceBrakeSignal = [False]
        self.emergencyBrakeSignal = [False]
    
    def emit(self):
        print("Emitting From Signal Sender")
        self.signals.powerSignal.emit(self.powerSignal)
        self.signals.lightSignal.emit(self.lightSignal)
        self.signals.doorSignal.emit(self.doorSignal)
        self.signals.temperatureSignal.emit(self.temperatureSignal)
        self.signals.announcementsSignal.emit(self.announcementsSignal)
        self.signals.advertisementsSignals.emit(self.advertisementsSignals)
        self.signals.serviceBrakeSignal.emit(self.serviceBrakeSignal)
        self.signals.emergencyBrakeSignal.emit(self.emergencyBrakeSignal)
        