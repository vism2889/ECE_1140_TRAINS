#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/05/2022
# FILENAME: TrackModelUI.py
# DESCRIPTION:
#
##############################################################################

import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QListWidget, QLabel, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from LayoutParser import LayoutParser
from TrackModelTestInterfaceUI import TestUI
from infraParser import InfraParser

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
        self.testUI        = TestUI()
        self.testList      = []
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
        for i in range(len(self.lineNames)):
            self.stations.append([])
        for i in range(len(self.lineNames)):
            for station in infraParser.stations:
                if station[0] == self.lineNames[i]:
                    self.stations[i].append(station)
        print(self.stations)
        print(len(self.stations[0]))

        for i in range(len(self.lineNames)):
            self.switches.append([])
        for i in range(len(self.lineNames)):
            for switch in infraParser.switches:
                if switch[0] == self.lineNames[i]:
                    self.switches[i].append(switch)

        for i in range(len(self.lineNames)):
            self.crossings.append([])
        for i in range(len(self.lineNames)):
            for crossing in infraParser.crossings:
                if crossing[0] == self.lineNames[i]:
                    self.crossings[i].append(crossing)
                
        #self.stations = infraParser.stations 
        #self.switches = infraParser.switches

        self.loadLines()
        self.loadBlockInfo()
        # Enable clicking of test UI button once aboove information has been loaded

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.bt1 = QPushButton("LOAD LAYOUT ",self)
        # self.bt1.setStyleSheet("background-color: rgb(175, 225, 175); color: black; border-radius: 5px")
        self.bt1.resize(self.width, 30)
        self.bt1.clicked.connect(self.openFileNameDialog)

        # testing interface UI
        self.launchTestUIBt = QPushButton("TEST INTERFACE",self)
        self.launchTestUIBt.resize(130, 30)
        self.launchTestUIBt.move(self.width-150,50)
        self.launchTestUIBt.clicked.connect(self.getTestVals)

        #self.loadBlockImage()
        self.blocksLabel = QLabel("TRACK BLOCKS", self)
        self.blocksLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blocksLabel.move(5,250)
        self.blocksLabel.resize(100,18)
        self.blockslistwidget = QListWidget(self)
        self.blockslistwidget.move(5,268)
        self.blockslistwidget.resize(100,340)
        #self.loadFaults()
        self.loadBlockInformationList()
        self.loadLineInfoList()
        self.loadListOfLineNames()
        self.loadBeaconInfo()
        self.loadBeaconList()
        self.loadFaults()
        # self.createTable()
        self.show()
    
    def loadBlockInformationList(self):
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
    
    def loadBeaconInfo(self):
        self.beaconInformationLabel = QLabel("-BEACON INFORMATION-",self)
        self.beaconInformationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.beaconInformationLabel.resize(300,18)
        self.beaconInformationLabel.setStyleSheet("background-color: cyan; color: black;")
        self.beaconInformationLabel.move(140,650)

        self.beaconInformationlistwidget = QListWidget(self)
        self.beaconInformationlistwidget.move(140,668)
        self.beaconInformationlistwidget.resize(150,380)

        self.beaconInformationVallistwidget = QListWidget(self)
        self.beaconInformationVallistwidget.setStyleSheet("color: orange;")
        self.beaconInformationVallistwidget.move(290,668)
        self.beaconInformationVallistwidget.resize(150,380) 

    def loadBeaconList(self):
        self.beaconInformationlistwidget.insertItem(0, "Data A:")
        self.beaconInformationlistwidget.insertItem(1, "Data B:")
        self.beaconInformationlistwidget.insertItem(2, "Data C:")
        self.beaconInformationlistwidget.insertItem(3, "Data D:")
    
    def loadListOfLineNames(self):
        self.linesLabel = QLabel("TRACK LINES", self)
        self.linesLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesLabel.move(5,32)
        self.linesLabel.resize(100,18)
        self.linelistwidget = QListWidget(self)
        self.linelistwidget.move(5,50)
        self.linelistwidget.resize(100,100)
        
    def loadLineInfoList(self):
        # create section that provides infor for each line (# of blocks, # of stations, # of switches)
        self.linesInfoLabel = QLabel("LINE INFORMATION", self)
        self.linesInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesInfoLabel.move(140,32)
        self.linesInfoLabel.resize(300,18)
        self.lineInfolistwidget = QListWidget(self)
        self.lineInfolistwidget.setStyleSheet("color: orange;")
        self.lineInfolistwidget.move(140,50)
        self.lineInfolistwidget.resize(150,200)
        self.lineInfolistwidget.insertItem(0,"Blocks on Line: ")
        self.lineInfolistwidget.insertItem(1,"Stations on Line: ")
        self.lineInfolistwidget.insertItem(2,"Switches on Line: ")
        self.lineInfolistwidget.insertItem(3,"Crossings on Line: ")
        self.lineInfolistwidget.insertItem(4,"Trains on Line: ")
        self.lineInfolistwidget.insertItem(5,"Heater State: ")
        self.lineInfolistwidget.insertItem(6,"Sales for Line: ")

        self.lineInfoVallistwidget = QListWidget(self)
        self.lineInfoVallistwidget.setStyleSheet("color: orange;")
        self.lineInfoVallistwidget.move(290,50)
        self.lineInfoVallistwidget.resize(150,200)
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
        
    def loadBlockImage(self):
        self.imageLabel = QLabel(self)
        self.pixmap     = QPixmap('trackblock.png')
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(140,10)
        self.imageLabel.resize(self.pixmap.width(), 130)
    
    def loadFaults(self):
        
        self.faultsLabel = QLabel("\tTRACK FAULTS:", self)
        self.faultsLabel.setStyleSheet("background-color: orange; color: black;")
        self.faultsLabel.move(600,510)
        self.faultsLabel.resize(self.width, 30)
        self.fault1 = QCheckBox("BROKEN RAIL", self)
        #self.fault1 = QPushButton("FAULT #1",self)
        self.fault1.move(600,550)
        self.fault2 = QCheckBox("CIRCUIT FAILURE",self)
        self.fault2.move(600,590)
        self.fault3 = QCheckBox("POWER FAILURE",self)
        self.fault3.move(600,630)
        # if self.currBlock != None:
        #     self.fault1.setChecked(self.currBlock.faults[0])
        self.fault1.stateChanged.connect(self.printVal)
        self.fault2.stateChanged.connect(self.printVal)
        self.fault3.stateChanged.connect(self.printVal)

    def printVal(self):
        print("VAL")
        if self.fault1.isChecked():
            self.currBlock.faultsText = "BROKEN RAIL"
        elif self.fault2.isChecked():
            self.currBlock.faultsText = "CIRCUIT FAILURE"
        elif self.fault3.isChecked():
            self.currBlock.faultsText = "POWER FAILURE"
        else:
            self.currBlock.faultsText = ""

        self.updateBlockInfo(int(self.currBlock.blockNumber)-1)

    def createTable(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,250)
        self.table.setRowCount(18)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.move(500, 120)
        self.table.resize(400,575)
        self.addTableLabels()
    
    def addTableLabels(self):
        item1 = QTableWidgetItem("Track Line")
        item2 = QTableWidgetItem("Section")
        item3 = QTableWidgetItem("Block Number")
        item4 = QTableWidgetItem("Block Length")
        item5 = QTableWidgetItem("Block Grade")
        item6 = QTableWidgetItem("Speed Limit")
        item7 = QTableWidgetItem("Infrastructure")
        item8 = QTableWidgetItem("Station Side")
        item9 = QTableWidgetItem("Elevation")
        item10 = QTableWidgetItem("Cumulative Elevation")
        item11 = QTableWidgetItem("Seconds To Traverse")
        item12 = QTableWidgetItem("Block Direction")
        item13 = QTableWidgetItem("Occupied")
        item14 = QTableWidgetItem("Switch Presence")
        item15 = QTableWidgetItem("Block Number")
        item16 = QTableWidgetItem("Block Number")
        item17 = QTableWidgetItem("Block Number")
        item18 = QTableWidgetItem("Block Number")
        item19 = QTableWidgetItem("Block Number")
        self.table.setItem(0,0, item1)
        
        self.table.setItem(1,0, item2)
        self.table.setItem(2,0, item3)
        self.table.setItem(3,0, item4)
        self.table.setItem(4,0, item5)
        self.table.setItem(5,0, item6)
        self.table.setItem(6,0, item7)
        self.table.setItem(7,0, item8)
        self.table.setItem(8,0, item9)
        self.table.setItem(9,0, item10)
        self.table.setItem(10,0, item11)
        self.table.setItem(11,0, item12)
        self.table.setItem(12,0, item13)
        self.table.setItem(13,0, item14)
        self.table.setItem(14,0, item15)
        self.table.setItem(15,0, item16)
        self.table.setItem(16,0, item17)
        self.table.setItem(17,0, item18)
        self.table.resizeRowsToContents()
        for i in range(12):
            self.table.item(i,0).setForeground(QtCore.Qt.cyan)

    def updateTableData(self, pCurrBlockIndex):
        currBlock = self.lines[self.currLineIndex][pCurrBlockIndex]
        item1 = QTableWidgetItem(currBlock.line)
        item2 = QTableWidgetItem(currBlock.section)
        item3 = QTableWidgetItem(currBlock.blockNumber)
        item4 = QTableWidgetItem(currBlock.blockLength)
        item5 = QTableWidgetItem(currBlock.grade)
        item6 = QTableWidgetItem(currBlock.speedLimit)
        item7 = QTableWidgetItem(currBlock.infrastructure)
        item8 = QTableWidgetItem(currBlock.stationSide)
        item9 = QTableWidgetItem(currBlock.elevation)
        item10 = QTableWidgetItem(currBlock.cumulativeElevation)
        item11 = QTableWidgetItem(currBlock.secsToTraverseBlock)
        item12 = QTableWidgetItem(currBlock.occupancy)
        item13 = QTableWidgetItem("NA")
        item14 = QTableWidgetItem("NA")
        item15 = QTableWidgetItem("NA")
        item16 = QTableWidgetItem("NA")
        item17 = QTableWidgetItem("NA")
        item18 = QTableWidgetItem("NA")
        self.table.setItem(0,1, item1)
        self.table.setItem(1,1, item2)
        self.table.setItem(2,1, item3)
        self.table.setItem(3,1, item4)
        self.table.setItem(4,1, item5)
        self.table.setItem(5,1, item6)
        self.table.setItem(6,1, item7)
        self.table.setItem(7,1, item8)
        self.table.setItem(8,1, item9)
        self.table.setItem(9,1, item10)
        self.table.setItem(10,1, item11)
        self.table.setItem(11,1, item12)
        self.table.setItem(12,1, item13)
        self.table.setItem(13,1, item14)
        self.table.setItem(14,1, item15)
        self.table.setItem(15,1, item16)
        self.table.setItem(16,1, item17)
        self.table.setItem(17,1, item18)
        for i in range(11):
            self.table.item(i,1).setForeground(QtCore.Qt.green)
        self.table.resizeRowsToContents()

    def loadLines(self):
        for i in range(len(self.lineNames)):
            self.linelistwidget.insertItem(0, self.lineNames[i])
        self.linelistwidget.itemClicked.connect(self.onClickedLine)

    def onClickedLine(self, item):
        currLine = item.text()
        self.currLineIndex = self.lineNames.index(currLine)
        print(currLine, self.currLineIndex)
        self.updateLineInformation()
        self.loadBlocks()
   
    def loadBlocks(self):
        self.blockslistwidget.clear()
        for i in range(len(self.lines[self.currLineIndex])):
            vBlockNumber = str(self.lines[self.currLineIndex][i].blockNumber)
            self.blockslistwidget.insertItem(i, "BLOCK "+vBlockNumber)
        self.blockslistwidget.itemClicked.connect(self.onClickedBlock)
    
    def onClickedBlock(self, item):
        currBlockIndex = int(item.text().split(" ")[1]) -1

        self.currBlock = self.lines[self.currLineIndex][currBlockIndex]
        # self.loadFaults()
        self.updateBlockInfo(currBlockIndex)
        # self.updateTableData(currBlockIndex)
        
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
        self.blockInfolistwidget.insertItem(18, "Fault Presence:       ")
        self.blockInfolistwidget.insertItem(19, "CIRCUIT FAILURE:      ")
        #self.blockslistwidget.itemClicked.connect(self.onClickedBlock)
        #fself.testFaultCheck = QCheckBox("CIRCUIT FAILURE",self)
        #self.blockInfolistwidget.insertItem(19, self.testFaultCheck)
       # self.blockInfolistwidget.insertItem(17," ")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Track Layout Selection", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.layoutFile = fileName
            self.initLayout()
        self.initTestUIData()

    def getTestVals(self):
        self.testUI.submitClicked.connect(self.printVals)
        self.testUI.occupancySignal.connect(self.updateTestOccupancy)
        self.testUI.switchStateSignal.connect(self.updateTestSwitchStates)   
        self.testUI.crossingLightSignal.connect(self.updateTestCrossingLights) 
        self.testUI.trackHeaterSignal.connect(self.updateTestTrackHeater)   
        
        self.testUI.show()
        self.initTestUIData()

    def updateTestOccupancy(self, occupancy):
        print("Updating Occupany from Test UI")
        blockList = self.lines[0] +self.lines[1]
        for i in range(len(blockList)):
            currBlock = blockList[i]
            if occupancy[i] == 0:
                currBlock.occupancy = False 
            else:
                currBlock.occupancy = True

        print(occupancy)

    def updateTestSwitchStates(self):
        print("Updating Switch States from Test UI")
        return 42

    def updateTestCrossingLights(self):
        print("Updating Crossing Lights from Test UI")
        return 42

    def updateTestTrackHeater(self, heaterVal):
        self.updateLineInformation(heaterVal)
        print("Updating Track Heater State from Test UI")
        return 42

    def updateLineInformation(self, heatVal=''):

        self.lineInfoVallistwidget.clear()
        self.lineInfoVallistwidget.insertItem(0,str(len(self.lines[self.currLineIndex])))
        self.lineInfoVallistwidget.item(0).setForeground(QtCore.Qt.green)
        self.lineInfoVallistwidget.insertItem(1,str(len(self.stations[self.currLineIndex])))
        self.lineInfoVallistwidget.item(1).setForeground(QtCore.Qt.green)
        self.lineInfoVallistwidget.insertItem(2,str(len(self.switches[self.currLineIndex])))
        self.lineInfoVallistwidget.item(2).setForeground(QtCore.Qt.green)
        self.lineInfoVallistwidget.insertItem(3,str(len(self.crossings[self.currLineIndex])))
        self.lineInfoVallistwidget.item(3).setForeground(QtCore.Qt.green)
        self.lineInfoVallistwidget.insertItem(4,"NA")
        self.lineInfoVallistwidget.item(4).setForeground(QtCore.Qt.gray)
        if heatVal != '':
            self.lineInfoVallistwidget.insertItem(5,str(heatVal))
            self.lineInfoVallistwidget.item(5).setForeground(QtCore.Qt.green)
        else:
            self.lineInfoVallistwidget.insertItem(5,"NA")
            self.lineInfoVallistwidget.item(5).setForeground(QtCore.Qt.gray)
        self.lineInfoVallistwidget.insertItem(6,"NA")
        self.lineInfoVallistwidget.item(6).setForeground(QtCore.Qt.gray)
# def on_sub_window_confirm(self, url):  # <-- This is the main window's slot
#         self.label.setText(f"Current URL: {url}")
    def printVals(self,testList):
        self.testVals = testList
        for i in range(len(self.testVals)):
            print(self.testVals[i])

    def initTestUIData(self):
        self.testUI.setDataFields(self.lineNames, self.lines, self.infraCounts)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())