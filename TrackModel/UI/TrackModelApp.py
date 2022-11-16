#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackModelApp.py
# DESCRIPTION:
#
##############################################################################

# Python Imports
import sys

# PyQt5 Imports
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QApplication, QFileDialog, QPushButton, QListWidget, QLabel
from PyQt5.QtGui import QFont, QColor
from PyQt5 import QtCore

# Developer Imports
sys.path.append("..\parsers") # tell interpreter where to look for parser files
from LayoutParser2 import LayoutParser


class TrackModel(QWidget):
    def __init__(self, signals=None):
        super().__init__()
        self.title         = 'Track Model - Pittsburgh Light Rail'
        self.left          = 40
        self.top           = 40
        self.width         = 450
        self.height        = 750
        self.currBlock     = None

        # Layout Information
        self.lineNames     = []    # List of Strings holding line names
        self.lines         = []    # List of TrackLine Objects
        self.lineBlocks    = []    # 2D List of blocks, each list representing a line
        self.blocksLoaded  = False # Bool to represent wether the TrackBlocks for a given line have been loaded
        self.currLineIndex = None
        self.layoutFile    = None
        self.testList      = []
        

        # System Communication Signals  
        self.occupancy     = [False for i in range(150)] # only Green line for right not
        self.faults        = [0 for i in range(150)]     # only Green line for right not
        self.orderedGreenLineList = []
        self.orderedGreenLine()
        if signals:
            self.signals = signals
            self.signals.occupancyFromTrainSignal.connect(self.getOccupancy)
            self.signals.globalOccupancyFromTrackModelSignal.emit(self.occupancy)
            
        
        print('ORDERED GREENLINE LIST:', self.orderedGreenLineList)
        self.initUI()

    def orderedGreenLine(self):
        print("Ordered green line being created")
        sec1     = [i for i in range(63, 101)]
        sec2     = [i for i in range(85, 76, -1)]
        sec3     = [i for i in range(101, 151)]
        sec4     = [i for i in range(29, 0, -1)]
        sec5     = [i for i in range(13, 58)]
        self.orderedGreenLineList = sec1 + sec2 + sec3 + sec4 + sec5
        print('FROM UI', self.orderedGreenLineList)

    def updateBlockCall(self):
        if self.currLineIndex != None and self.blocksLoaded == True:
            self.updateBlocks()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.bt1 = QPushButton("LOAD LAYOUT ",self)
        self.bt1.resize(self.width, 30)
        self.bt1.setStyleSheet("background-color: orange ; color: black;")
        self.bt1.clicked.connect(self.openFileNameDialog)
        # self.center() # Opens UI in the center of the current screen

        

        self.blocksLabel = QLabel("TRACK BLOCKS", self)
        self.blocksLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blocksLabel.move(5,150)
        self.blocksLabel.resize(100,18)
        self.blockslistwidget = QListWidget(self)
        self.blockslistwidget.move(5,168)
        self.blockslistwidget.resize(100,580)
        self.blockslistwidget.setStyleSheet("background-color: gray;")

        self.blockInfoLabel = QLabel("- BLOCK INFORMATION -", self)
        self.blockInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.blockInfoLabel.resize(300,18)
        self.blockInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blockInfoLabel.move(130,250)

        self.blockInfolistwidget = QListWidget(self)
        self.blockInfolistwidget.move(130,268)
        self.blockInfolistwidget.resize(150,420)
        self.blockInfolistwidget.setStyleSheet("background-color: gray;")

        self.blockVallistwidget = QListWidget(self)
        self.blockVallistwidget.setStyleSheet("color: orange;")
        self.blockVallistwidget.move(280,268)
        self.blockVallistwidget.resize(150,420) 
        self.blockVallistwidget.setStyleSheet("background-color: gray;")

        self.currBlockDisplay = QLabel("BLOCK:", self)
        self.currBlockDisplay.move(130, 40)
        self.currBlockDisplay.resize(300, 100)
        self.currBlockDisplay.setStyleSheet("background-color: cyan; color: black;")
        self.currBlockDisplay.setFont(QFont('Arial', 20))

        self.trackFault1 = QPushButton("Toggle Track Fault", self)
        self.trackFault1.move(130, 690)
        self.trackFault1.resize(100,50)
        self.trackFault1.setStyleSheet("background-color: orange ; color: black;")
        self.trackFault1.clicked.connect(self.updateFaults)

        self.trackFault2 = QPushButton("Toggle Power Fault", self)
        self.trackFault2.move(235, 690)
        self.trackFault2.resize(100,50)
        self.trackFault2.setStyleSheet("background-color: orange ; color: black;")

        self.trackFault3 = QPushButton("Toggle Switch Fault", self)
        self.trackFault3.move(340, 690)
        self.trackFault3.resize(100,50)
        self.trackFault3.setStyleSheet("background-color: orange ; color: black;")

        self.linesLabel = QLabel("TRACK LINES", self)
        self.linesLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesLabel.move(5,40)
        self.linesLabel.resize(100,18)
        self.linelistwidget = QListWidget(self)
        self.linelistwidget.move(5,58)
        self.linelistwidget.resize(100,50)
        self.linelistwidget.setStyleSheet("background-color: gray;")

        self.loadBeaconInfo()

        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def updateFaults(self):
        print(self.currBlock.faultPresence)
        if self.currBlock.faultPresence == False:
            self.currBlock.faultPresence = True
            self.currBlock.faultsText = "Fault1"
            self.blockslistwidget.item(int(self.currBlock.blockNumber)-1).setBackground(QColor(255,0,0))
            self.updateBlockInfo(self.currBlockIndex)

            self.faults[self.currBlockIndex] = 1
            self.signals.trackFailuresSignal.emit(self.faults)
        else:
            self.currBlock.faultPresence = False
            self.currBlock.faultsText = "None"
            self.blockslistwidget.item(int(self.currBlock.blockNumber)-1).setBackground(QColor(250,250,250))
            self.updateBlockInfo(self.currBlockIndex)

            self.faults[self.currBlockIndex] = 0
            self.signals.trackFailuresSignal.emit(self.faults)

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
                item = QListWidgetItem("BLOCK "+vBlockNumber)
                self.blockslistwidget.insertItem(i+1, item)
                self.lineBlocks[self.currLineIndex].append(block)
                i+=1
        self.blockslistwidget.itemClicked.connect(self.onClickedBlock)
        self.blocksLoaded = True
        self.signals.trackBlocksToTrainModelSignal.emit(self.lineBlocks)
        self.signals.greenLineTrackBlockSignal.emit(self.orderedGreenLineList)

    def updateBlocks(self):
        for i in range(len(self.occupancy)):
            if self.faults[i] == True:
                self.blockslistwidget.item(i).setBackground(QColor(255,0,0))
            elif self.occupancy[i] == True:
                self.blockslistwidget.item(i).setBackground(QColor(200,200,50))
            else:
                self.blockslistwidget.item(i).setBackground(QColor(134, 132, 130))

    def onClickedLine(self, item):
        currLine = item.text()
        self.currLineIndex = self.lineNames.index(currLine)
        print(currLine, self.currLineIndex)
        self.loadBlocks()

    def onClickedBlock(self, item):
        self.currBlockIndex = int(item.text().split(" ")[1]) -1
        self.currBlock      = self.lineBlocks[self.currLineIndex][self.currBlockIndex]
        self.updateBlockInfo(self.currBlockIndex)
        self.currBlockDisplay.setText("BLOCK: "+str(self.currBlock.line)+"-"+str(self.currBlock.section)+"-"+str(self.currBlock.blockNumber))
        
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

        self.currBlock.occupancy = self.occupancy[self.currBlockIndex]
        
        
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
        self.beaconInformationLabel.move(130,150)

        self.beaconInformationlistwidget = QListWidget(self)
        self.beaconInformationlistwidget.move(130,168)
        self.beaconInformationlistwidget.resize(150,80)
        self.beaconInformationlistwidget.setStyleSheet("background-color: gray;")
        self.beaconInformationlistwidget.insertItem(0, "Next station Forward:")
        self.beaconInformationlistwidget.insertItem(1, "Forward Station Side:")
        self.beaconInformationlistwidget.insertItem(2, "Next station Reverse:")
        self.beaconInformationlistwidget.insertItem(3, "Reverse Station Side:")


        self.beaconInformationVallistwidget = QListWidget(self)
        self.beaconInformationVallistwidget.setStyleSheet("color: orange;")
        self.beaconInformationVallistwidget.move(280,168)
        self.beaconInformationVallistwidget.resize(150,80) 
        self.beaconInformationVallistwidget.setStyleSheet("background-color: gray;")
    
    def getOccupancy(self, occupancy):
        self.occupancy = occupancy
        # print("GUI OCCUPANCY", self.occupancy)
        self.updateBlockCall()

    def updateBlockList(self, line):
        for block in self.lineBlocks[line]:
            block.occupancy = 5

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrackModel()
    sys.exit(app.exec_())