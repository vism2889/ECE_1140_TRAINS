#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackModelApp.py
# DESCRIPTION:
#
#############################################################################

# Python Imports
import sys
import random
from datetime import date

# PyQt5 Imports
from PyQt5.QtWidgets import (
    QApplication, QInputDialog, QTableWidgetItem, 
    QAbstractItemView, QListWidgetItem, QWidget, 
    QApplication, QFileDialog, QPushButton, QListWidget,
    QLabel, QLineEdit, QTableWidget, QTableView
    )

from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5 import QtCore

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# Developer Imports
sys.path.append("..\parsers") # tell interpreter where to look for parser files
from LayoutParser2 import LayoutParser

class TrackModel(QWidget):
    '''
    Class Description here
    '''
    
    heaterSignal = QtCore.pyqtSignal(bool)

    def __init__(self, signals=None):
        '''
        Description here
        '''
        super().__init__()
        
        today                        = date.today()
        self.currDate                = today.strftime("%d/%m/%Y")
        #print("d1 =", self.currDate)

        # Current Selections
        self.currBlock               = None
        self.currBlockIndex          = None
        self.currLineIndex           = None

        self.currGreenLineBlock      = None
        self.currGreenLineBlockIndex = None
        self.currRedLineBlock        = None
        self.currRedLineBlockIndex   = None

        # Layout Information
        self.lineNames               = []    # List of Strings holding line names
        self.lines                   = []    # List of TrackLine Objects
        self.lineBlocks              = []    # 2D List of blocks, each list representing a line
        self.blocksLoaded            = False # Bool to represent wether the TrackBlocks for a given line have been loaded
        self.layoutFile              = None
        self.signals                 = None
        self.temp                    = 50
        self.currTemp                = 0

        # Variables to hold values for System Communication Signals For final presentation
        self.occupancy               = [[False for i in range(76)],[False for i in range(150)]]
        self.faults                  = [[0 for i in range(76)],[0 for i in range(150)]]
        self.switches                = [[0 for i in range(76)],[0 for i in range(150)]]

        # Variables to hold values for displaying stations and switches on a selected line
        self.switchText              = []
        self.stations                = []
        self.boardingPassengers      = []
        self.departingPassengers     = []
        
        self.heaterOn                = False 
        
        self.orderedGreenLineList    = []
        self.orderedGreenLine()
        self.authorityFromWayside    = []
        
        # System Communication Signals
        if signals:
            self.signals = signals # system signals instance 

            self.signals.trainLocation.connect(self.getOccupancy)          # from train model: (used for occupancy)

            self.signals.waysideAuthority.connect(self.getAuthority)       # from wayside: (used for authority)
            # self.signals.crossingState.connect()                         # from wayside: List of length two indicating a block and it's crossing state [(int) block #, (bool) state]
            self.signals.switchState.connect(self.updateSwitchState)       # from wayside: List of length 2 [(int) block #, (bool) state]


            self.signals.ctcSwitchState.connect(self.updateCtcSwitchState) # from ctc office: List of length 3 [(int) line, (int) block #, (bool) switch state]

            # self.signals.stoppedBlocks.connect(self.updateStoppedBlocks) # sets a list = [list of blocks that trains are stopped at]

        # Signals local to module
        #self.heaterSignal
        self.heaterSignal.connect(self.updateHeaterState)
        self.initUI()
    
    def initUI(self):
        '''
        Initializes all of the objects in the base UI before a given track layout 
        has been loaded or a track line has been selected
        '''
        # Pyqt Window Properties
        self.title               = 'Track Model - Pittsburgh Light Rail'
        self.left                = 40
        self.top                 = 40
        self.width               = 950
        self.height              = 750
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setFixedHeight(self.height)
        #self.setFixedWidth(self.width)
        self.setStyleSheet("background-color: rgb(150,137,130);")
        self.displayLoadLayoutButton()
        # self.center() # Opens UI in the center of the current screen
        self.displayTrackBlockList()
        self.displayBlockInformationSection()
        self.displayLargeSelectedBlockLabel()
        self.displayTrackLineList()
        self.displayFaultButtons()
        self.displayBeaconInformationLabels()
        self.displayStationList()
        self.displaySwitchList()
        self.displayTemperatureButton()
        self.autoGeneratedTemperatureInit()

        # Track Model System Themed Logo
        self.trackModelImage     = QLabel(self)
        self.pixmap              = QPixmap('../images/TrackModel.png')
        self.pixmap              = self.pixmap.scaled(QtCore.QSize(160, 100))
        self.trackModelImage.setPixmap(self.pixmap)
        self.trackModelImage.resize(175,100)
        self.trackModelImage.move(self.width-160, self.height-100)

    def displayTemperatureButton(self):
        '''
        Displays the UI components for interacting with the temperature
        '''
        self.temperatureDisplay = QPushButton("Set Temperature:", self)
        self.temperatureDisplay.move(440, 40)
        self.temperatureDisplay.resize(200, 50)
        self.temperatureDisplay.setStyleSheet("background-color: cyan; color: black;")
        self.temperatureDisplay.setFont(QFont('Arial', 10))
        self.temperatureDisplay.clicked.connect(self.updateTemperature)

        self.temperatureVal = QLabel("Temp:"+ str(self.currTemp) + ' F', self)
        
        self.temperatureVal.setStyleSheet("background-color: white; color: black;")
        self.temperatureVal.move(650, 40)
        self.temperatureVal.resize(95, 50)
        self.temperatureVal.setFont(QFont('Arial', 10))

    def autoGeneratedTemperatureInit(self):
        '''
        generates temperature based on averages for the month based on past data
        '''
        avgTemps      = [23.6, 31.9, 42.7, 48.9, 62.8, 69.6, 74.2, 72.1, 64.3, 50.7, 44.3, 40.9]
        month         = self.currDate[3:5]
        self.currTemp = avgTemps[int(month)-1]
        self.temperatureVal.setText("Temp: " + str(self.currTemp) + ' F')

        if self.currTemp <= 32:
            self.heaterSignal.emit(True)
        else:
            self.heaterSignal.emit(False)
        
    def updateTemperature(self):
        '''
        updates the temperature to be what the user inputs into the temperature prompt
        '''
        self.temp, done = QInputDialog.getInt(self, 'Temperature Edit', 'Enter Track Line Temperature:')
        #print(self.temp)
        self.temperatureVal.setText("Temp: " + str(self.temp) + ' F')
        if self.temp <= 32:
            self.heaterSignal.emit(True)
        else:
            self.heaterSignal.emit(False)

    def displaySwitchList(self):
        '''
        Creates the table that shows all of the switches and their information 
        respective to the currently loaded line
        '''
        # Switch Information / State Label
        self.switchInfoLabel = QLabel("Switch Information", self)
        
        self.switchInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.switchInfoLabel.move(440, 470)
        self.switchInfoLabel.resize(300, 50)
        self.switchInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.switchInfoLabel.setFont(QFont('Arial', 10))

        # Switch State Table
        self.switchInfoTable = QTableWidget(self)
        self.switchInfoTable.move(440, 530)
        self.switchInfoTable.resize(300, 200)
        self.switchInfoTable.setStyleSheet("background-color: gray; color: black;")
        self.switchInfoTable.setFont(QFont('Arial', 10))
        self.switchInfoTable.setColumnCount(3)
        self.switchInfoTable.setHorizontalHeaderLabels(['BLOCK','FORWARD', 'REVERSE'])
        self.switchInfoTable.setColumnWidth(0, 40)
        self.switchInfoTable.setColumnWidth(1, 120)
        self.switchInfoTable.setColumnWidth(2, 120)
        self.switchInfoTable.setRowCount(15) 
        self.switchInfoTable.verticalHeader().hide()
        self.switchInfoTable.horizontalHeader().setStretchLastSection(True)
        self.switchInfoTable.setSelectionMode(QAbstractItemView.NoSelection)

    def displayStationList(self):
        '''
        Creates the table that shows all of the stations and their information 
        respective to the currently loaded line
        '''
        self.stationInfoLabel = QLabel("Station Information", self)
        self.stationInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.stationInfoLabel.move(440, 100)
        self.stationInfoLabel.resize(410, 50)
        self.stationInfoLabel.setStyleSheet("background-color: cyan; color: black;")
        self.stationInfoLabel.setFont(QFont('Arial', 10))

        # Switch State Table
        self.stationInfoTable = QTableWidget(self)
        #self.stationInfoTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter | Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.stationInfoTable.move(440, 160)
        self.stationInfoTable.resize(410, 300)
        self.stationInfoTable.setStyleSheet("background-color: gray; color: black;")
        self.stationInfoTable.setFont(QFont('Arial', 10))
        self.stationInfoTable.setColumnCount(4)
        self.stationInfoTable.setHorizontalHeaderLabels(['BLOCK', 'STATION','Passengers Boarding', 'Total Ticket Sales'])
        self.stationInfoTable.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.Alignment(QtCore.Qt.TextWordWrap))
        self.stationInfoTable.horizontalHeader().setFixedHeight(40)
        self.stationInfoTable.setColumnWidth(0, 40)
        self.stationInfoTable.setColumnWidth(1, 150)
        self.stationInfoTable.setColumnWidth(2, 100)
        self.stationInfoTable.setColumnWidth(3, 100)
        self.stationInfoTable.setRowCount(15) 
        self.stationInfoTable.verticalHeader().hide()
        self.stationInfoTable.horizontalHeader().setStretchLastSection(True)
        self.stationInfoTable.setSelectionMode(QAbstractItemView.NoSelection)

    def updateSwitchState(self, switch):
        '''
        updates the swicthes for a given line
        '''
        for i in range(len(self.switchText)):
            # print('TEXT', self.switchText[self.currLineIndex][i][0])
            blockNum = int(self.switchText[self.currLineIndex][i][0])
            if switch[0] == blockNum:
                # print('switch signal 2:', switch, ', current line switch', )
                self.lineBlocks[self.currLineIndex][switch[0]-1].switchState = switch[1]
                if switch[1] == True:
                    self.switchInfoTable.item(i,1).setBackground(QtCore.Qt.green)
                    self.switchInfoTable.item(i,2).setBackground(QtCore.Qt.red)
                else:
                    self.switchInfoTable.item(i,1).setBackground(QtCore.Qt.red)
                    self.switchInfoTable.item(i,2).setBackground(QtCore.Qt.green)

    def updateCtcSwitchState(self, switchState):
        print("CTC Switch State Signal", switchState)

    def orderedGreenLine(self):
        '''
        Creates an green line for temporary use when presenting progress
        '''
        #print("Ordered green line being created")
        sec1     = [i for i in range(63, 101)]
        sec2     = [i for i in range(85, 76, -1)]
        sec3     = [i for i in range(101, 151)]
        sec4     = [i for i in range(29, 0, -1)]
        sec5     = [i for i in range(13, 58)]
        self.orderedGreenLineList = sec1 + sec2 + sec3 + sec4 + sec5

    def updateBlockOccupancyCallback(self):
        '''
        Checks to see if a line has been loaded, if so then the occupancy is 
        displayed over the list of blocks for that line
        '''
        if self.currLineIndex != None and self.blocksLoaded == True:
            self.updateBlocksOccupancy()

    def displayLoadLayoutButton(self):
        '''
        Creates and displays the button used to load the tracklayout file.
        '''
        self.bt1 = QPushButton("LOAD LAYOUT ",self)
        self.bt1.resize(self.width, 30)
        self.bt1.setStyleSheet("background-color: orange ; color: black;")
        self.bt1.clicked.connect(self.openFileNameDialog)

    def displayLargeSelectedBlockLabel(self):
        '''
        Displays a large block label to get important information for a block quickly
        '''
        self.currBlockDisplay = QLabel("BLOCK:", self)
        self.currBlockDisplay.move(130, 40)
        self.currBlockDisplay.resize(300, 100)
        self.currBlockDisplay.setStyleSheet("background-color: cyan; color: black;")
        self.currBlockDisplay.setFont(QFont('Arial', 20))
        
        # Sets large indicator with track fault label
        self.blockFaultIndicator = QLabel('', self)
        self.blockFaultIndicator.hide()

        # Sets large indicator with switch label
        self.blockSwitchIndicator = QLabel('', self)
        self.blockSwitchIndicator.hide()

    def displayTrackLineList(self):
        '''
        Displays the list of track lines loaded from the track layout file.
        '''
        self.linesLabel = QLabel("TRACK LINES", self)
        
        self.linesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.linesLabel.setStyleSheet("background-color: cyan; color: black;")
        self.linesLabel.move(5,40)
        self.linesLabel.resize(100,18)
        self.linelistwidget = QListWidget(self)
        self.linelistwidget.move(5,58)
        self.linelistwidget.resize(100,50)
        self.linelistwidget.setStyleSheet("background-color: gray;")

    def displayTrackBlockList(self):
        '''
        Displays the list of blocks for the trackline selected from the trackline list.
        '''
        self.blocksLabel = QLabel("TRACK BLOCKS", self)
        self.blocksLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.blocksLabel.setStyleSheet("background-color: cyan; color: black;")
        self.blocksLabel.move(5,150)
        self.blocksLabel.resize(120,18)
        self.blockslistwidget = QListWidget(self)
        self.blockslistwidget.move(5,168)
        self.blockslistwidget.resize(120,580)
        self.blockslistwidget.setStyleSheet("background-color: rgb(128, 128, 128);")

    def displayBlockInformationSection(self):
        '''
        Displays the lists that hold block information labels and block information values
        '''
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

    def displayFaultButtons(self):
        '''
        Displays the buttons for triggering the three possible trackmodel related faults
        '''
        self.trackFault1 = QPushButton("Track Fault", self)
        self.trackFault1.move(130, 690)
        self.trackFault1.resize(90,50)
        self.trackFault1.setStyleSheet("background-color: orange ; color: black;")
        self.trackFault1.clicked.connect(lambda : self.updateFaults("Track Fault"))

        self.trackFault2 = QPushButton("Power Fault", self)
        self.trackFault2.move(235, 690)
        self.trackFault2.resize(90,50)
        self.trackFault2.setStyleSheet("background-color: orange ; color: black;")
        self.trackFault2.clicked.connect(lambda : self.updateFaults("Power Fault"))

        self.trackFault3 = QPushButton("Circuit Fault", self)
        self.trackFault3.move(340, 690)
        self.trackFault3.resize(90,50)
        self.trackFault3.setStyleSheet("background-color: orange ; color: black;")
        self.trackFault3.clicked.connect(lambda : self.updateFaults("Circuit Fault"))

        self.trackFault1.setEnabled(False)
        self.trackFault2.setEnabled(False)
        self.trackFault3.setEnabled(False)

    def center(self):
        '''
        Aligns the main window to the center of the screen upon launching 
        TrackModel application.
        '''
        frameGm     = self.frameGeometry()
        screen      = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def updateFaults(self, faultName):
        '''
        Updates all the fault related information for a given block when a fault it triggered.
        '''
        #print(faultName)
        faultNum = 0
        if faultName == 'Track Fault':
            faultNum = 1
        elif faultName == 'Power Fault':
            faultNum = 2
        elif faultName == 'Circuit Fault':
            faultNum = 4
        else:
            faultNum = 0

        if self.currBlock.faultPresence == False and faultName not in self.currBlock.faultsText:
            self.currBlock.faultsText        = []
            self.currBlock.faultPresence     = True
            self.faults[self.currLineIndex][self.currBlockIndex] += faultNum
            self.currBlock.faultsText.append(faultName)
            self.blockslistwidget.item(int(self.currBlock.blockNumber)-1).setBackground(QColor(255,0,0))
            self.blockslistwidget.item(int(self.currBlock.blockNumber)-1).setIcon(QIcon("../images/alert.png"))
            self.linelistwidget.item(int(self.currLineIndex)).setIcon(QIcon("../images/alert.png"))
            self.updateBlockInfo(self.currBlockIndex)
        
        elif self.currBlock.faultPresence == True and faultName not in self.currBlock.faultsText: 
            self.currBlock.faultsText.append(faultName)
            self.faults[self.currLineIndex][self.currBlockIndex] += faultNum
            self.updateBlockInfo(self.currBlockIndex)
        
        elif self.currBlock.faultPresence == True and faultName in self.currBlock.faultsText:
            self.currBlock.faultsText.remove(faultName)
            self.faults[self.currLineIndex][self.currBlockIndex] -= faultNum
            self.updateBlockInfo(self.currBlockIndex)
        
        if not self.currBlock.faultsText:
            self.currBlock.faultPresence     = False
            self.faults[self.currLineIndex][self.currBlockIndex] = 0
            self.blockslistwidget.item(int(self.currBlock.blockNumber)-1).setBackground(QColor(128, 128, 128))
            self.currBlockDisplay.setStyleSheet("background-color: cyan; color: black;")
            self.blockslistwidget.item(int(self.currBlock.blockNumber)-1).setIcon(QIcon(""))
        
        x = [x for x in self.faults[self.currLineIndex] if x != 0]
        #print(x)
        if len(x)==0:
            self.linelistwidget.item(int(self.currLineIndex)).setIcon(QIcon(""))

        #self.signals.blockFailures.emit(self.faults)
        if self.signals:
            self.signals.trackFailuresSignal.emit(self.faults)

    def openFileNameDialog(self):
        '''
        Launchs the file dialog allowing a user to load a trackline diagram.
        '''
        dial = QFileDialog()
        options = dial.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Track Layout Selection", "../Layout-Files","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            #print(fileName)
            self.layoutFile = fileName
            self.initLayout()

    def initLayout(self):
        ''' 
            Calls LayoutParser.py which will return a list of track-line names, 
            and a 2D list of BlockModel objects, the columns are the track-lines, 
            and the rows are the blocks for that line
        '''
        parser     = LayoutParser(self.layoutFile)
        self.lines = parser.process()
        for line in self.lines:
            self.lineNames.append(line.name)
            #print(line.name)

        self.loadLines()
        self.displayBlockInfoLabels()

    def loadLines(self):
        '''
        Loads the names of the track lines parsed from the layout file into the 
        lines selection list.
        '''
        for i in range(len(self.lines)):
            self.lineBlocks.append([])

            self.switchText.append([])
            self.stations.append([])
            self.departingPassengers.append([])
            self.boardingPassengers.append([])
            self.linelistwidget.insertItem(i, self.lines[i].name)
        self.linelistwidget.itemClicked.connect(self.onClickedLine)
        self.loadAllLinesBlocks()

    def displayBlockInfoLabels(self):
        '''
        Displays all of the labels for the information contained in a given track block.
        '''
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

    def loadAllLinesBlocks(self):
        '''
        Loads all the blocks for all the lines in the layout specified 
        with the user provided csv file
        '''
        i = 0
        for k in range(len(self.lineNames)):
            i = 0
            for section in self.lines[k].sections:
                for block in section.blocks:
                    self.lineBlocks[k].append(block)
                    i+=1
                    if block.switch != "":
                        self.switches[k][i] = [8,25]
                        self.switchText[k].append([block.blockNumber, block.switch, block.switchForward, block.switchReverse])
                    if block.station:
                        self.stations[k].append([block.blockNumber, block.station])
                        self.departingPassengers[k].append(self.generateBoardingPassengers())
                        self.boardingPassengers[k].append(self.generateLeavingPassengers())

    def loadBlocks(self):
        '''
        Loads all of the track blocks for a given track line into   
        the block selection list.
        '''
        self.blockslistwidget.clear()
        i = 0
        for section in self.lines[self.currLineIndex].sections:
            for block in section.blocks:
                vBlockNumber = str(block.blockNumber)
                item = QListWidgetItem("BLOCK "+vBlockNumber)
                self.blockslistwidget.insertItem(i+1, item)
                if block.faultsText:
                    self.blockslistwidget.item(i).setBackground(QColor(255,0,0))
                    self.blockslistwidget.item(i).setIcon(QIcon("../images/alert.png"))
                else:
                    self.blockslistwidget.item(i).setBackground(QColor(134, 132, 130))
                    
                    self.blockslistwidget.item(i).setIcon(QIcon(""))
                i+=1
        self.blockslistwidget.itemClicked.connect(self.onClickedBlock)
        self.blocksLoaded = True
            
        if self.signals:
            self.signals.trackBlocksToTrainModelSignal.emit(self.lineBlocks)
            self.signals.greenLineTrackBlockSignal.emit(self.orderedGreenLineList)
            
    def updateBlocksOccupancy(self):
        '''
        Updates the background color of all the blocks in the current lines
        block selection list with colors reflecting thier fault and occupancy states.
        '''
        #print("Block Update Called")
        for i in range(len(self.occupancy[self.currLineIndex])):
            if self.faults[self.currLineIndex][i] == True:
                self.blockslistwidget.item(i).setBackground(QColor(255,0,0))
                
                self.blockslistwidget.item(i).setIcon(QIcon("../images/alert.png"))
            elif self.occupancy[self.currLineIndex][i] == True:
                self.blockslistwidget.item(i).setBackground(QColor(200,200,50))
                self.signals.beaconFromTrackModelSignal.emit(self.lineBlocks[self.currLineIndex][i].forwardBeacon.split())
                print(self.lineBlocks[self.currLineIndex][i].forwardBeacon)
                if self.currBlockIndex == i: 
                    self.currBlockDisplay.setStyleSheet("background-color: rgb(200,200,50); color: black;")
            elif self.authorityFromWayside != None and (i+1) in self.authorityFromWayside:

                self.blockslistwidget.item(i).setBackground(QtCore.Qt.green)
            else:
                self.blockslistwidget.item(i).setBackground(QColor(134, 132, 130))
                
                self.blockslistwidget.item(i).setIcon(QIcon(""))
        # updates the current block information display
        self.updateBlockInfo(self.currBlockIndex)

    def displayLineStations(self):
        ''' 
        used to display all the stations for a given line, the boarding and 
        exiting passengers, and the block at which the station exists
        '''
        self.stationInfoTable.setRowCount(0)
        self.stationInfoTable.setRowCount(15) 
        for i in range(len(self.stations[self.currLineIndex])):
            self.stationInfoTable.setItem(i, 0, QTableWidgetItem(self.stations[self.currLineIndex][i][0]))
            self.stationInfoTable.setItem(i, 1, QTableWidgetItem(self.stations[self.currLineIndex][i][1]))
            self.stationInfoTable.setItem(i, 2, QTableWidgetItem(str(self.boardingPassengers[self.currLineIndex][i])))
            self.stationInfoTable.setItem(i, 3, QTableWidgetItem('0'))
        
        #print(self.stations)

    def displayLineSwitches(self):
        '''
        Used to display all the switches for a given line, the switch state, 
        and the block at which the switch exists
        '''
        
        self.switchInfoTable.setRowCount(0)
        self.switchInfoTable.setRowCount(10) 
        for i in range(len(self.switchText[self.currLineIndex])):
            self.switchInfoTable.setItem(i, 0, QTableWidgetItem(str(self.switchText[self.currLineIndex][i][0])))
            self.switchInfoTable.setItem(i, 1, QTableWidgetItem(str(self.switchText[self.currLineIndex][i][2])))
            self.switchInfoTable.item(i,1).setBackground(QtCore.Qt.green)
            self.switchInfoTable.setItem(i, 2, QTableWidgetItem(str(self.switchText[self.currLineIndex][i][3])))
            self.switchInfoTable.item(i,2).setBackground(QtCore.Qt.red)

    def onClickedLine(self, item):
        '''
        Sets the current line based on the selection make from the list of lines
        and loads the blocks for that line.
        '''
        currLine = item.text()
        self.currLineIndex = self.lineNames.index(currLine)
        # print(currLine, self.currLineIndex)
        
        self.switchInfoLabel.setText(self.lineNames[self.currLineIndex] + " Line Switch Information")
        self.stationInfoLabel.setText(self.lineNames[self.currLineIndex] + " Line Station Information")
        self.displayLineStations()
        self.displayLineSwitches()
        self.loadBlocks()
        #print(self.boardingPassengers)
        #print(self.stations)

    def onClickedBlock(self, item):
        '''
        Sets the current block selected from the current lines block list
        and loads that blocks information into the block information values list.
        '''
        self.currBlockIndex = int(item.text().split(" ")[1]) -1
        self.currBlock      = self.lineBlocks[self.currLineIndex][self.currBlockIndex]
        self.updateBlockInfo(self.currBlockIndex)
        self.currBlockDisplay.setText("BLOCK: "+str(self.currBlock.line)+"-"+str(self.currBlock.section)+"-"+str(self.currBlock.blockNumber))
        self.trackFault1.setEnabled(True)
        self.trackFault2.setEnabled(True)
        self.trackFault3.setEnabled(True)
        
    def updateBlockInfo(self, pCurrBlockIndex):
        '''
        Updates the displayed information in the block information list to that of
        the currently selected block.
        '''
        if self.currBlockIndex != None:
            if self.currBlock.faultsText:
                self.currBlockDisplay.setStyleSheet("background-color: red; color: black;")
                self.blockFaultIndicator.setText(str(self.currBlock.faultsText))
                self.blockFaultIndicator.show()
                self.blockFaultIndicator.move(130, 40)
                self.blockFaultIndicator.resize(300, 20)
                self.blockFaultIndicator.setStyleSheet("background-color: yellow; color: black;")
                self.blockFaultIndicator.setFont(QFont('Arial', 10))
            else:
                self.currBlockDisplay.setStyleSheet("background-color: cyan; color: black;")
                self.blockFaultIndicator.hide()

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

            self.currBlock.occupancy = self.occupancy[self.currLineIndex][self.currBlockIndex]
            
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
            self.blockVallistwidget.insertItem(14, str(self.lineBlocks[1][self.currBlockIndex].switchState))
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
            self.blockVallistwidget.insertItem(18,str(currBlock.faultsText))
            self.blockVallistwidget.item(18).setForeground(QtCore.Qt.red)
            self.blockVallistwidget.insertItem(19,currBlock.station)
            self.blockVallistwidget.item(19).setForeground(QtCore.Qt.yellow)

            if self.currBlock.switch:
                self.blockSwitchIndicator.setText('SWITCH STATE: '+str(self.lineBlocks[1][self.currBlockIndex].switchState)) #TODO: Update here to reflect new switchState signal
                self.blockSwitchIndicator.show()
                self.blockSwitchIndicator.move(130, 120)
                self.blockSwitchIndicator.resize(300, 20)
                self.blockSwitchIndicator.setStyleSheet("background-color: rgb(68,214,44); color: black;")
                self.blockSwitchIndicator.setFont(QFont('Arial', 10))
                self.blockSwitchIndicator.setAlignment(QtCore.Qt.AlignCenter)
            else:
                self.blockSwitchIndicator.setStyleSheet("background-color: cyan; color: black;")
                self.blockSwitchIndicator.hide()

            self.blockVallistwidget.insertItem(20,str(currBlock.switch))
            self.blockVallistwidget.item(20).setForeground(QtCore.Qt.red)
            self.blockVallistwidget.insertItem(21,str(currBlock.underground))
            self.blockVallistwidget.item(21).setForeground(QtCore.Qt.red)
            
            self.blockVallistwidget.insertItem(22,str(self.heaterOn))
            self.blockVallistwidget.insertItem(23, str(self.lineBlocks[1][self.currBlockIndex].forwardBeacon))
        
    def displayBeaconInformationLabels(self):
        '''
        Description here
        '''
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
        '''
        Updates all occupancy related displays and emits a new global occupancy
        '''
        #print(occupancy)
        line      = occupancy[0]
        lastBlock = occupancy[2]
        currBlock = occupancy[3]

        # print("GUI OCCUPANCY", self.occupancy)
        self.occupancy[int(line)][int(lastBlock)-1] = 0
        self.occupancy[int(line)][int(currBlock)-1] = 1
        self.signals.globalOccupancyFromTrackModelSignal.emit(self.occupancy) # should emit a new global occupancy
        self.updateBlockOccupancyCallback()

    def getAuthority(self, authority):
        self.authorityFromWayside = authority[1]
        #print('authority from track model:', self.authorityFromWayside)
        self.updateBlocksOccupancy()


    def addPassngersToStations(self):
        '''
        should add boarding and departing passengers to all stations
        '''
        return 42

    def generateBoardingPassengers(self):
        '''
        Generates a random number of passengers between 1-99 to board the next 
        arriving train
        '''
        boardingPassengers = random.randint(0,50)
        return boardingPassengers

    def generateLeavingPassengers(self):
        '''
        Generates a random number of passengers between 1-99 to exit the next 
        arriving train
        '''
        leavingPassengers = random.randint(0, 50)
        return leavingPassengers

    def updateHeaterState(self, state):
        '''
        should update the track heater to be True for all blocks on both lines
        '''
        if state:
            #print("heater on")
            self.heaterOn = True
        else:
           # print("heater off")
            self.heaterOn = False
        
        if self.currBlockIndex != None:
            self.blockVallistwidget.item(22).setText(str(self.heaterOn))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrackModel()
    ex.show()
    sys.exit(app.exec_())