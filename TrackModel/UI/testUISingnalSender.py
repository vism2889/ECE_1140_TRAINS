#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/17/2022
# FILENAME: testUISignalSender.py
# DESCRIPTION:
#   Used to send signal communications to the TrackModel UI
#   Emulates:
#       - Occupancy
#       - Track Faults
#       - Block Maintenance
#   Has functionality to hide and show the TrackModelApp UI, as to better navigate other system modules
#   and to optionally reduce clutter on smaller screens.
##############################################################################

# Python Imports
import time
import random
import threading
import sys

# PyQt5 Imports
from   PyQt5.QtWidgets       import * 
from   PyQt5.QtGui           import * 
from   PyQt5.QtCore          import *

# Developer Imports
from   TrackModelApp         import TrackModel
from   occupancySignalSender import SendOccupancy
sys.path.append("..\..\SystemSignals") # tell interpreter where to look for model files
from   Signals import Signals

class SignalSenderUI(QWidget):
    '''
    Class Description here
    '''
    def __init__(self, signals, TrackModelUI):
        super().__init__()
        
        self.UiComponents()
        #self.show()
        self.signals         = signals
        self.modelUI         = TrackModelUI
        self.blocks          = [i for i in range(150)]
        self.blockLens       = [random.randint(10,25) for i in range(150)]
        self.distance        = 0
        self.currBlockIndex  = 0
        self.timerr          = 0
        
        self.occupancy       = [[False for i in range(76)],[False for i in range(150)]] # only Green line for right not
        self.faults          = [[0 for i in range(76)],[0 for i in range(150)]]     # only Green line for right not
        self.maintenance     = [[0 for i in range(76)],[0 for i in range(150)]]
        self.line            = "Green"
        self.lineBlocks      = []
        self.greenLineBlocks = [] 
        self.breakThread = False

        # Signal Connections
        self.signals.greenLineTrackBlockSignal.connect(self.loadGreenLineBlocks)
        self.signals.trackFailuresSignal.connect(self.updateFaults)
        self.signals.trackBlocksToTrainModelSignal.connect(self.updateLineBlocks)
        
    def UiComponents(self):
        self.setWindowTitle("Python ")
        self.setGeometry(500, 40, 400, 600)
        self.startTestTrainButton = QPushButton("Start Train", self)
        self.startTestTrainButton.setGeometry(25, 25, 150, 50)
        self.startTestTrainButton.clicked.connect(self.startTimerThread)

        self.startTestTrainButton = QPushButton("Stop Train", self)
        self.startTestTrainButton.setGeometry(25, 80, 150, 50)
        self.startTestTrainButton.clicked.connect(self.stopTimerThread)

        self.currBlocklabel = QLineEdit("Curr Block: 1", self)
        self.currBlocklabel.setGeometry(180, 25, 200, 50)
        self.currBlocklabel.setFont(QFont("Arial",20))
        self.currBlocklabel.setDisabled(True)

        self.startTestTrainButton = QPushButton("Update Switch", self)
        self.startTestTrainButton.setGeometry(25, 135, 150, 50)

        self.startTestTrainButton = QPushButton("Launch Track Model", self)
        self.startTestTrainButton.setGeometry(25, 190, 150, 50)
        self.startTestTrainButton.clicked.connect(self.launchModelUI)

        self.label = QLabel("Block", self)
        self.label.setGeometry(180, 135, 50, 50)
        self.label.setFont(QFont("Arial",10))

        self.label = QLineEdit(self)
        self.label.setGeometry(220, 135, 50, 50)
        self.label.setFont(QFont("Arial",20))

        self.label = QLabel("State", self)
        self.label.setGeometry(295, 135, 50, 50)
        self.label.setFont(QFont("Arial",10))

        self.label = QLineEdit(self)
        self.label.setGeometry(335, 135, 50, 50)
        self.label.setFont(QFont("Arial",20))

    def launchModelUI(self):
        self.modelUI.show()

    def stopTimerThread(self):
        self.breakThread = True
        self.occupancyThread.join()

    def startTimerThread(self):
        self.occupancyThread = threading.Thread(target=self.timer)
        self.occupancyThread.start()
        
    def timer(self):
        while self.currBlockIndex < 10 and self.breakThread == False:
            speed = 50
            self.timerr += .01
            self.distance = speed*self.timerr
            print("distance:", self.distance)
            self.getOccupancy()
            time.sleep(0.1)

    def loadGreenLineBlocks(self, blockNums):
        self.greenLineBlocks = blockNums
        print("LOADING GREEN LINE BLOCKS:", self.greenLineBlocks)

    def updateFaults(self, faults):
        self.faults = faults

    def updateLineBlocks(self, blocks):
        self.lineBlocks = blocks

    def getOccupancy(self):
        if self.distance >= self.blockLens[self.currBlockIndex]:
            self.currBlockIndex += 1
            self.distance                            = 0
            self.timerr                              = 0
            self.occupancy[1][self.currBlockIndex-1] = 0
            self.occupancy[1][self.currBlockIndex]   = 1
            self.currBlocklabel.setText('Curr Block: '+str(self.currBlockIndex+1))
            
            print("NEW OCCUPANCY:", self.currBlockIndex)

        # Emit Occupancy    
        self.signals.occupancyFromTrainSignal.emit(self.occupancy)
        
        print("From sender: Train on Block:", self.currBlockIndex+1)
        print("From sender: FAULTS:\n", self.faults)
        #print("From sender: LineBlocks:\n", self.lineBlocks)
        #print("From sender: GREEN LINE", self.greenLineBlocks)

if __name__ == '__main__':
    App          = QApplication(sys.argv)
    signals      = Signals()
    TrackModelUI = TrackModel(signals)
    signalSender = SignalSenderUI(signals, TrackModelUI)
    signalSender.show()
    sys.exit(App.exec())