#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackModelUI_2.py
# DESCRIPTION:
#
##############################################################################

import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore

# tell interpreter where to look for model files
sys.path.insert(0,"../parsers")
from LayoutParser2 import LayoutParser
# from TrackModelTestInterfaceUI import TestUI
# from infraParser import InfraParser



class App(QWidget):
    # occupancySignal     = QtCore.pyqtSignal(list)  # <-- This is the sub window's signal
    def __init__(self):
        super().__init__()
        self.title         = 'Train Model - Pittsburgh Light Rail'
        self.left          = 10
        self.top           = 10
        self.width         = 1000
        self.height        = 800
        self.currBlock = None

        # Layout Information
        self.lineNames     = []
        self.lines         = []
        self.stations      = []
        self.crossings     = []
        self.switches      = []
        self.infraCounts   = [] # holds the count  for  stations, switches, crossings
        self.currLineIndex = None
        self.layoutFile    = None
        #self.testUI       = TestUI()
        self.testList      = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.bt1 = QPushButton("LOAD LAYOUT ",self)
        # self.bt1.setStyleSheet("background-color: rgb(175, 225, 175); color: black; border-radius: 5px")
        self.bt1.resize(self.width, 30)
        self.bt1.clicked.connect(self.openFileNameDialog)
        #
        # testing interface UI
        self.launchTestUIBt = QPushButton("TEST INTERFACE",self)
        self.launchTestUIBt.resize(130, 30)
        self.launchTestUIBt.move(self.width-150,50)

        self.blocksLabel = QLabel("TRACK BLOCKS", self)
        self.blocksLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blocksLabel.move(5,250)
        self.blocksLabel.resize(100,18)
        self.blockslistwidget = QListWidget(self)
        self.blockslistwidget.move(5,268)
        self.blockslistwidget.resize(100,380)

        self.blockInfoLabel = QLabel("- BLOCK INFORMATION -", self)
        self.blockInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.blockInfoLabel.resize(300,18)
        self.blockInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blockInfoLabel.move(140,250)

        self.blockInfolistwidget = QListWidget(self)
        self.blockInfolistwidget.move(140,268)
        self.blockInfolistwidget.resize(150,380)

        self.blockVallistwidget = QListWidget(self)
        self.blockVallistwidget.setStyleSheet("color: orange;")
        self.blockVallistwidget.move(290,268)
        self.blockVallistwidget.resize(150,380) 


        self.linesLabel = QLabel("TRACK LINES", self)
        self.linesLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesLabel.move(5,32)
        self.linesLabel.resize(100,18)
        self.linelistwidget = QListWidget(self)
        self.linelistwidget.move(5,50)
        self.linelistwidget.resize(100,100)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Track Layout Selection", "../Layout-Files","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.layoutFile = fileName
            self.initLayout()

    def initLayout(self):
        ''' 
            Calls LayoutParser.py which will return a list of track-line names, 
            and a 2D list of BlockModel objects, the columns are the track-lines, 
            and the rows are the blocks for that line
        '''
        parser = LayoutParser(self.layoutFile)
        self.lines = parser.process()
        for line in self.lines:
            print(line.name)
        self.loadLines()
        self.loadBlockInfoLabels()
        #self.confirmLayoutData()

    def confirmLayoutData(self):
        for line in self.lines:
            print(line.name)
            for section in line.sections:
                print("\t", section.name)

    def loadLines(self):
        for i in range(len(self.lines)):
            self.linelistwidget.insertItem(i, self.lines[i].name)


    def loadBlockInfoLabels(self):
        self.blockInfolistwidget.insertItem(0,  "Track Line:           ")
        self.blockInfolistwidget.insertItem(1,  "Section:              ")
        self.blockInfolistwidget.insertItem(2,  "Block Number:         ")
        self.blockInfolistwidget.insertItem(3,  "Block Length:         ")
        self.blockInfolistwidget.insertItem(4,  "Block Grade:          ")
        self.blockInfolistwidget.insertItem(5,  "Speed Limit:          ")
        self.blockInfolistwidget.insertItem(6,  "Infrastructure:       ")
        self.blockInfolistwidget.insertItem(7,  "Station Side:         ")
        self.blockInfolistwidget.insertItem(8,  "Elevation:            ")
        self.blockInfolistwidget.insertItem(9,  "Cumulative Elevation: ")
        self.blockInfolistwidget.insertItem(10, "Seconds To Traverse:  ")
        for i in range(0,10):
            self.blockInfolistwidget.item(i).setForeground(QtCore.Qt.cyan) 

        self.blockInfolistwidget.insertItem(11, "Block Direction:      ")
        self.blockInfolistwidget.insertItem(12, "Occupied:             ")
        self.blockInfolistwidget.insertItem(13, "Switch Presence:      ")
        self.blockInfolistwidget.insertItem(14, "Switch State:         ")
        self.blockInfolistwidget.insertItem(15, "Crossing Presence:    ")
        self.blockInfolistwidget.insertItem(16, "Crossing Lights:      ")
        self.blockInfolistwidget.insertItem(17, "Ticket Sales:         ")
        self.blockInfolistwidget.insertItem(18, "Fault Presence:       ")
        self.blockInfolistwidget.insertItem(19, "CIRCUIT FAILURE:      ")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())