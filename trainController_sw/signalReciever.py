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
        
        self.powerSignal = []
        self.lightSignal = []
        self.doorSignal = []
        self.temperatureSignal = []
        self.announcementsSignal = []
        self.advertisementsSignals = []
        self.serviceBrakeSignal = []
        self.emergencyBrakeSignal = []
        
        self.signal.powerSignal.connect(self.printPower)
    
    def printPower(self, power):
        print("POWER RECIEVED IN Signal Reciever:", end=None)
        print(power)