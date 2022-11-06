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
sys.path.insert(0,"../parsers") # tell interpreter where to look for model files
from LayoutParser2 import LayoutParser

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
        self.lineBlocks    = []
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
        self.blockslistwidget.resize(100,480)

        self.blockInfoLabel = QLabel("- BLOCK INFORMATION -", self)
        self.blockInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.blockInfoLabel.resize(300,18)
        self.blockInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blockInfoLabel.move(140,250)

        self.blockInfolistwidget = QListWidget(self)
        self.blockInfolistwidget.move(140,268)
        self.blockInfolistwidget.resize(150,480)

        self.blockVallistwidget = QListWidget(self)
        self.blockVallistwidget.setStyleSheet("color: orange;")
        self.blockVallistwidget.move(290,268)
        self.blockVallistwidget.resize(150,480) 


        self.linesLabel = QLabel("TRACK LINES", self)
        self.linesLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesLabel.move(5,32)
        self.linesLabel.resize(100,18)
        self.linelistwidget = QListWidget(self)
        self.linelistwidget.move(5,50)
        self.linelistwidget.resize(100,100)
        self.loadBeaconInfo()

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
            self.lineNames.append(line.name)
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
            self.lineBlocks.append([])
            self.linelistwidget.insertItem(i, self.lines[i].name)
        self.linelistwidget.itemClicked.connect(self.onClickedLine)

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
        self.blockInfolistwidget.insertItem(19, "Station:              ")
        self.blockInfolistwidget.insertItem(20, "Switch:               ")
        self.blockInfolistwidget.insertItem(21, "Underground:          ")
        self.blockInfolistwidget.insertItem(22, "Track Heater:         ")
        self.blockInfolistwidget.insertItem(23, "Beacon:               ")

    def loadBlocks(self):
        self.blockslistwidget.clear()
        i = 0
        for section in self.lines[self.currLineIndex].sections:
            for block in section.blocks:
                vBlockNumber = str(block.blockNumber)
                self.blockslistwidget.insertItem(i+1, "BLOCK "+vBlockNumber)
                self.lineBlocks[self.currLineIndex].append(block)
                i+=1
        self.blockslistwidget.itemClicked.connect(self.onClickedBlock)

    def onClickedLine(self, item):
        currLine = item.text()
        self.currLineIndex = self.lineNames.index(currLine)
        print(currLine, self.currLineIndex)
        #self.updateLineInformation()
        self.loadBlocks()

    def onClickedBlock(self, item):
        currBlockIndex = int(item.text().split(" ")[1]) -1

        self.currBlock = self.lineBlocks[self.currLineIndex][currBlockIndex]
        # self.loadFaults()
        self.updateBlockInfo(currBlockIndex)
        # self.updateTableData(currBlockIndex)

    def updateBlockInfo(self, pCurrBlockIndex):
        self.blockVallistwidget.clear()
        currBlock = self.lineBlocks[self.currLineIndex][pCurrBlockIndex]
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

        if(currBlock.occupancy == True):
            self.blockVallistwidget.insertItem(12,str(currBlock.occupancy))
            self.blockVallistwidget.item(12).setForeground(QtCore.Qt.green)
        else: 
            self.blockVallistwidget.insertItem(12,str(currBlock.occupancy))
            self.blockVallistwidget.item(12).setForeground(QtCore.Qt.red)

        if("SWITCH" in currBlock.infrastructure):
            self.blockVallistwidget.insertItem(13,str(True))
            self.blockVallistwidget.item(13).setForeground(QtCore.Qt.green) 
        else:
            self.blockVallistwidget.insertItem(13,str(False))
            self.blockVallistwidget.item(13).setForeground(QtCore.Qt.red) 
        self.blockVallistwidget.insertItem(14,"NA")
        self.blockVallistwidget.item(14).setForeground(QtCore.Qt.gray) 

        if ("CROSSING" in currBlock.infrastructure):
            self.blockVallistwidget.insertItem(15,str(True))
            self.blockVallistwidget.item(15).setForeground(QtCore.Qt.green)
        else:
            self.blockVallistwidget.insertItem(15,str(False))
            self.blockVallistwidget.item(15).setForeground(QtCore.Qt.red)
        if ("CROSSING" in currBlock.infrastructure and currBlock.occupancy == True):
            self.blockVallistwidget.insertItem(16,"ON")
            self.blockVallistwidget.item(16).setForeground(QtCore.Qt.green)
        else: 
            self.blockVallistwidget.insertItem(16,"OFF")
            self.blockVallistwidget.item(16).setForeground(QtCore.Qt.red)
        self.blockVallistwidget.insertItem(17,"NA")
        self.blockVallistwidget.item(17).setForeground(QtCore.Qt.gray) 
        self.blockVallistwidget.insertItem(18,currBlock.faultsText)
        self.blockVallistwidget.item(18).setForeground(QtCore.Qt.red)
        self.blockVallistwidget.insertItem(19,currBlock.station)
        self.blockVallistwidget.item(19).setForeground(QtCore.Qt.yellow)
        self.blockVallistwidget.insertItem(20,str(currBlock.switch))
        self.blockVallistwidget.item(20).setForeground(QtCore.Qt.red)
        self.blockVallistwidget.insertItem(21,str(currBlock.underground))
        self.blockVallistwidget.item(21).setForeground(QtCore.Qt.red)
        
    def loadBeaconInfo(self):
        self.beaconInformationLabel = QLabel("-BEACON INFORMATION-",self)
        self.beaconInformationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.beaconInformationLabel.resize(300,18)
        self.beaconInformationLabel.setStyleSheet("background-color: cyan; color: black;")
        self.beaconInformationLabel.move(540,250)

        self.beaconInformationlistwidget = QListWidget(self)
        self.beaconInformationlistwidget.move(540,268)
        self.beaconInformationlistwidget.resize(150,380)

        self.beaconInformationVallistwidget = QListWidget(self)
        self.beaconInformationVallistwidget.setStyleSheet("color: orange;")
        self.beaconInformationVallistwidget.move(690,268)
        self.beaconInformationVallistwidget.resize(150,380) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())