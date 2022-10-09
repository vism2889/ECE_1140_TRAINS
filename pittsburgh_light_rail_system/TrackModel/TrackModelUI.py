#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/05/2022
# FILENAME: TrackModelUI.py
# DESCRIPTION:
#
##############################################################################

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from LayoutParser import LayoutParser
from TrackModelTestInterfaceUI import TestUI
from InfraParser import InfraParser

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title         = 'Train Model - Pittsburgh Light Rail'
        self.left          = 10
        self.top           = 10
        self.width         = 640
        self.height        = 540
        self.lineNames     = []
        self.lines         = []
        self.infraCounts   = [] # holds the count  for  stations, switches, crossings
        self.currLineIndex = None
        self.layoutFile    = None
        self.testUI        = TestUI()
        self.initUI()

    def initLayout(self):
        ''' 
            Calls LayoutParser.py which will return a list of track-line names, 
            and a 2D list of BlockModel objects, the columns are the track-lines, 
            and the rows are the blocks for that line
        '''
        parser = LayoutParser(self.layoutFile)
        self.lineNames, self.lines = parser.process()
        print(self.lineNames)

        infraParser = InfraParser(self.layoutFile)
        infraParser.parse()
        infraParser.process()
        
        self.loadLines()
        self.loadBlockInfo()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.bt1 = QPushButton("LOAD LAYOUT",self)
        # self.bt1.setStyleSheet("background-color: rgb(175, 225, 175); color: black; border-radius: 5px")
        self.bt1.resize(self.width, 30)
        self.bt1.clicked.connect(self.openFileNameDialog)

        # testing interface UI
        self.launchTestUIBt = QPushButton("TEST INTERFACE",self)
        self.launchTestUIBt.resize(130, 30)
        self.launchTestUIBt.move(self.width-150,50)
        self.launchTestUIBt.clicked.connect(self.testUI.show)

        #self.loadBlockImage()
        self.loadFaults()
        
        self.blocksLabel = QLabel("TRACK BLOCKS", self)
        self.blocksLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blocksLabel.move(5,150)
        self.blocksLabel.resize(100,18)
        self.blockslistwidget = QListWidget(self)
        self.blockslistwidget.move(5,168)
        self.blockslistwidget.resize(100,340)

        self.blockInfoLabel = QLabel("- BLOCK INFORMATION -", self)
        self.blockInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.blockInfoLabel.resize(300,18)
        self.blockInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blockInfoLabel.move(140,150)
        
        self.blockInfolistwidget = QListWidget(self)
        self.blockInfolistwidget.move(140,168)
        self.blockInfolistwidget.resize(150,340)

        self.blockVallistwidget = QListWidget(self)
        self.blockVallistwidget.setStyleSheet("color: orange;")
        self.blockVallistwidget.move(290,168)
        self.blockVallistwidget.resize(150,340)

        self.linesLabel = QLabel("TRACK LINES", self)
        self.linesLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesLabel.move(5,32)
        self.linesLabel.resize(100,18)
        self.linelistwidget = QListWidget(self)
        self.linelistwidget.move(5,50)
        self.linelistwidget.resize(100,100)

        # create section that provides infor for each line (# of blocks, # of stations, # of switches)
        self.linesInfoLabel = QLabel("LINE INFORMATION", self)
        self.linesInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesInfoLabel.move(140,32)
        self.linesInfoLabel.resize(300,18)
        self.lineInfolistwidget = QListWidget(self)
        self.lineInfolistwidget.setStyleSheet("font: 9pt; color: orange;")
        self.lineInfolistwidget.move(140,50)
        self.lineInfolistwidget.resize(150,100)
        self.lineInfolistwidget.insertItem(0,"Number Blocks on Line: ")
        self.lineInfolistwidget.insertItem(1,"Number Stations on Line: ")
        self.lineInfolistwidget.insertItem(2,"Number Switches on Line: ")
        self.lineInfolistwidget.insertItem(3,"Number Crossings on Line: ")
        self.lineInfolistwidget.insertItem(4,"Number Trains Routed on Line: ")
        self.lineInfolistwidget.insertItem(5,"Track Heater State: ")
        self.lineInfolistwidget.insertItem(6,"Ticket Sales for Line: ")

        self.lineInfoVallistwidget = QListWidget(self)
        self.lineInfoVallistwidget.setStyleSheet("font: 9pt; color: orange;")
        self.lineInfoVallistwidget.move(290,50)
        self.lineInfoVallistwidget.resize(150,100)
        self.lineInfoVallistwidget.insertItem(0,"NA")
        self.lineInfoVallistwidget.item(0).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(1,"NA")
        self.lineInfoVallistwidget.item(1).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(2,"NA")
        self.lineInfoVallistwidget.item(2).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(3,"NA")
        self.lineInfoVallistwidget.item(3).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(4,"NA")
        self.lineInfoVallistwidget.item(4).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(5,"NA")
        self.lineInfoVallistwidget.item(5).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(6,"NA")
        self.lineInfoVallistwidget.item(6).setForeground(QtCore.Qt.gray)
        self.show()

    def loadBlockImage(self):
        self.imageLabel = QLabel(self)
        self.pixmap     = QPixmap('trackblock.png')
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(140,10)
        self.imageLabel.resize(self.pixmap.width(), 130)
    
    def loadFaults(self):
        self.faultsLabel = QLabel("\tTRACK FAULTS:", self)
        self.faultsLabel.setStyleSheet("background-color: orange; color: black;")
        self.faultsLabel.move(0,510)
        self.faultsLabel.resize(self.width, 30)
        self.fault1 = QCheckBox("FAULT #1", self)
        #self.fault1 = QPushButton("FAULT #1",self)
        self.fault1.move(160,515)
        self.fault2 = QCheckBox("FAULT #2",self)
        self.fault2.move(260,515)
        self.fault3 = QCheckBox("FAULT #3",self)
        self.fault3.move(360,515)

    def loadLines(self):
        for i in range(len(self.lineNames)):
            self.linelistwidget.insertItem(0, self.lineNames[i])
        self.linelistwidget.itemClicked.connect(self.onClickedLine)

    def onClickedLine(self, item):
        currLine = item.text()
        self.currLineIndex = self.lineNames.index(currLine)
        print(currLine, self.currLineIndex)
        self.loadBlocks()
   
    def loadBlocks(self):
        self.blockslistwidget.clear()
        for i in range(len(self.lines[self.currLineIndex])):
            vBlockNumber = str(self.lines[self.currLineIndex][i].blockNumber)
            self.blockslistwidget.insertItem(i, "BLOCK "+vBlockNumber)
        self.blockslistwidget.itemClicked.connect(self.onClickedBlock)
    
    def onClickedBlock(self, item):
        currBlockIndex = int(item.text().split(" ")[1]) -1
        self.updateBlockInfo(currBlockIndex)

    def updateBlockInfo(self, pCurrBlockIndex):
        self.blockVallistwidget.clear()
        currBlock = self.lines[self.currLineIndex][pCurrBlockIndex]
        self.blockVallistwidget.insertItem(0,currBlock.line)
        self.blockVallistwidget.insertItem(1,currBlock.section)
        self.blockVallistwidget.insertItem(2,currBlock.blockNumber)
        self.blockVallistwidget.insertItem(3,currBlock.blockLength)
        self.blockVallistwidget.insertItem(4,currBlock.grade)
        self.blockVallistwidget.insertItem(5,currBlock.speedLimit)

        if len(currBlock.infrastructure) < 1:
            self.blockVallistwidget.insertItem(6,"NA")
            self.blockVallistwidget.item(6).setForeground(QtCore.Qt.gray) 
        else:
            self.blockVallistwidget.insertItem(6,currBlock.infrastructure)

        if len(currBlock.stationSide) < 1:
            self.blockVallistwidget.insertItem(7,"NA")
            self.blockVallistwidget.item(7).setForeground(QtCore.Qt.gray) 
        else:
            self.blockVallistwidget.insertItem(7,currBlock.stationSide)

        self.blockVallistwidget.insertItem(8,currBlock.elevation)
        self.blockVallistwidget.insertItem(9,currBlock.cumulativeElevation)

        if len(currBlock.secsToTraverseBlock) < 1:
            self.blockVallistwidget.insertItem(10,"NA")
            self.blockVallistwidget.item(10).setForeground(QtCore.Qt.gray) 
        else:
            self.blockVallistwidget.insertItem(10,currBlock.secsToTraverseBlock)

        self.blockVallistwidget.insertItem(11,"NA")
        self.blockVallistwidget.item(11).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(12,"NA")
        self.blockVallistwidget.item(12).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(13,"NA")
        self.blockVallistwidget.item(13).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(14,"NA")
        self.blockVallistwidget.item(14).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(15,"NA")
        self.blockVallistwidget.item(15).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(16,"NA")
        self.blockVallistwidget.item(16).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(17,"NA")
        self.blockVallistwidget.item(17).setForeground(QtCore.Qt.gray) 

    def loadBlockInfo(self):
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
       # self.blockInfolistwidget.insertItem(17," ")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Track Layout Selection", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.layoutFile = fileName
            self.initLayout()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())