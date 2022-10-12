#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/09/2022
# FILENAME: TrackModelTestInterfaceUI.py
# DESCRIPTION:
#
##############################################################################

import sys
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
#from TrackModelUI import *

class TestUI(QWidget):
    submitClicked = QtCore.pyqtSignal(list)  # <-- This is the sub window's signal

    occupancySignal     = QtCore.pyqtSignal(list)  # <-- This is the sub window's signal
    switchStateSignal   = QtCore.pyqtSignal(list)  # <-- This is the sub window's signal
    crossingLightSignal = QtCore.pyqtSignal(list)  # <-- This is the sub window's signal
    trackHeaterSignal   = QtCore.pyqtSignal(bool)  # <-- This is the sub window's signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Model - Test Interface - Pittsburgh Light Rail')
        self.left   = 650
        self.top    = 10
        self.width  = 640
        self.height = 540
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: gray; color: black;")
        
        self.label = QLabel("NOTE: Please upload a tracklayout file in the main UI to begin testing.", self)
        self.label.move(10,10)
        self.label.setStyleSheet("color: orange;")

        self.lineNames   = []
        self.testlines   = []
        self.infraCounts = []

        self.launchTestUIBt = QPushButton("PopulateVals",self)
        self.launchTestUIBt.setStyleSheet("background-color: cyan; color: black; border-radius: 5px;")
        self.launchTestUIBt.resize(180, 25)
        self.launchTestUIBt.move(self.width-200,50)
        self.launchTestUIBt.clicked.connect(self.confirm)

        self.trackHeaterBtn = QPushButton("Update Track Heater",self)
        self.trackHeaterBtn.setStyleSheet("background-color: cyan; color: black; border-radius: 5px;")
        self.trackHeaterBtn.resize(180, 25)
        self.trackHeaterBtn.move(self.width-200,80)
        self.trackHeaterBtn.clicked.connect(self.updateTrackHeaterState)

        self.occupancyBtn = QPushButton("Update Occupancy",self)
        self.occupancyBtn.setStyleSheet("background-color: cyan; color: black; border-radius: 5px;")
        self.occupancyBtn.resize(180, 25)
        self.occupancyBtn.move(self.width-200,110)
        self.occupancyBtn.clicked.connect(self.updateOccupancyValues)

        self.switchStatesBtn = QPushButton("Update Switch States",self)
        self.switchStatesBtn.setStyleSheet("background-color: cyan; color: black; border-radius: 5px;")
        self.switchStatesBtn.resize(180, 25)
        self.switchStatesBtn.move(self.width-200,140)
        self.switchStatesBtn.clicked.connect(self.updateSwitchStateValues)

        self.crossingLightsBtn = QPushButton("Update Crossing Lights",self)
        self.crossingLightsBtn.setStyleSheet("background-color: cyan; color: black; border-radius: 5px;")
        self.crossingLightsBtn.resize(180, 25)
        self.crossingLightsBtn.move(self.width-200,170)
        self.crossingLightsBtn.clicked.connect(self.updateCrossingLightValues)

        


        self.faultsLabel = QLabel("TRACK FAULTS:", self)
        self.faultsLabel.setStyleSheet("background-color: orange; color: black;")
        self.faultsLabel.move(0,198)
        self.faultsLabel.resize(self.width, 30)

        self.fault1 = QCheckBox("FAULT #1", self)
        self.fault1.setStyleSheet("background-color: orange; color: white;")
        self.fault1.move(120,205)
        self.fault2 = QCheckBox("FAULT #2",self)
        self.fault2.setStyleSheet("background-color: orange; color: white;")
        self.fault2.move(220,205)
        self.fault3 = QCheckBox("FAULT #3",self)
        self.fault3.setStyleSheet("background-color: orange; color: white;")
        self.fault3.move(320,205)

        self.faultsBtn = QPushButton("Update Fault Values",self)
        self.faultsBtn.setStyleSheet("background-color: cyan; color: black; border-radius: 5px;")
        self.faultsBtn.resize(180, 25)
        self.faultsBtn.move(self.width-200,200)
        self.faultsBtn.clicked.connect(self.updateFaultValues)
        

        # self.line_edit = QLineEdit(self, placeholderText="Enter list here:")

    def confirm(self):  # <-- Here, the signal is emitted *along with the data we want*
        self.submitClicked.emit([1,2,3,4,5,1578])
        # self.close()

    def printLines(self):
        print(self.lineNames)
        
    def getTestVals(self):
        return [5,120,60]


    def updateOccupancyValues(self):
        self.occupancySignal.emit([])

    def updateSwitchStateValues(self):
        self.switchStateSignal.emit([])

    def updateCrossingLightValues(self):
        self.crossingLightSignal.emit([])
    
    def updateTrackHeaterState(self):
        self.trackHeaterSignal.emit(self.fault1.isChecked())

    def updateFaultValues(self):
        #self.trackHeaterSignal.emit([])
        print("Fault #1:", self.fault1.isChecked())
        print("Fault #2:", self.fault2.isChecked())
        print("Fault #3:", self.fault3.isChecked())

    def setDataFields(self, plineNames, plines, pinfraCounts):
        self.lineNames   = plineNames
        self.testlines   = plines 
        self.infraCounts = pinfraCounts
        #print(plines)
        #print("self.lineNames", self.lineNames)
