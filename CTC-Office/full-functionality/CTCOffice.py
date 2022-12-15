#!/usr/bin/env python3

##############################################################################
# AUTHOR(S):   GARRETT MARCINAK
# DATE:     11/13/2022
# FILENAME: CTCOffice.py
# DESCRIPTION:
#   Launches the CTC Office interface
##############################################################################

from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os

sys.path.append('../train-functionality/')
sys.path.append('../block-functionality/')
sys.path.append('../schedule-functionality/')
sys.path.append('../../SystemSignals/')
from TrainDictionary import TrainDictionary
from LayoutParserCTC import LayoutParserCTC
from DispatchPopUp import DispatchPopUp
from ScheduleParser import ScheduleParser

# if hasattr(Qt, 'AA_EnableHighDpiScaling'):
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

# if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class CTCOffice(QWidget):
    dispatchSignal = QtCore.pyqtSignal(bool)
#################################################################
# Start UI generation and setup
#################################################################
    def __init__(self, signals):
        super().__init__()

        self.setupLayout()
        self.setupUi()
        self.signals        = signals
        self.trainCount     = 1

        current_time        = QTime.currentTime()
        self.seconds        = current_time.toString('ss')
        self.minutes        = current_time.toString('mm')
        self.hours          = current_time.toString('hh')

        # connect to necessary signals
        self.signals.globalOccupancyFromTrackModelSignal.connect(self.readOccupancySignal)
        self.signals.switchState.connect(self.updateSwitchState)
        self.signals.clockSpeedSignal.connect(self.changeClockSpeed)
        self.signals.waysideAuthority.connect(self.showAuthority)
        self.signals.trackFailuresSignal.connect(self.readFaultSignal)

    def setupLayout(self):
        # getting lists of blocks
        layoutFile              = 'Track_Layout_PGH_Light_Rail.csv'
        trackLayout             = LayoutParserCTC(layoutFile)
        self.redLineBlocks, self.greenLineBlocks = trackLayout.process()

        # Create default station dictionary
        self.redLineStations    = dict()
        self.greenLineStations  = dict()

        # define station lists in order
        self.redLineStations["SHADYSIDE"]           = ["7", False]
        self.redLineStations["HERRON AVE"]          = ["16", False]
        self.redLineStations["SWISSVILLE"]          = ["21", False]
        self.redLineStations["PENN STATION"]        = ["25", False]
        self.redLineStations["STEEL PLAZA"]         = ["35", False]
        self.redLineStations["FIRST AVE"]           = ["45", False]
        self.redLineStations["STATION SQUARE"]      = ["48", False]
        self.redLineStations["SOUTH HILLS JUNC."]   = ["60", False]

        self.greenLineStations["GLENBURY"]          = ["65", False]
        self.greenLineStations["DORMONT (OUT)"]     = ["73", False]
        self.greenLineStations["MT-LEBANON"]        = ["77", False]
        self.greenLineStations["POPLAR"]            = ["88", False]
        self.greenLineStations["CASTE SHANNON"]     = ["96", False]
        self.greenLineStations["GLENBURY"]          = ["114", False]
        self.greenLineStations["OVERBROOK (OUT)"]   = ["122", False]
        self.greenLineStations["INGLEWOOD (OUT)"]   = ["131", False]
        self.greenLineStations["CENTRAL (OUT)"]     = ["140", False]
        self.greenLineStations["WHITED"]            = ["22", False]
        self.greenLineStations["SUSHVILLE"]         = ["16", False]
        self.greenLineStations["EDGEBROOK"]         = ["9", False]
        self.greenLineStations["PIONEER"]           = ["2", False]
        self.greenLineStations["SOUTH BANK"]        = ["31", False]
        self.greenLineStations["CENTRAL (IN)"]      = ["38", False]
        self.greenLineStations["INGLEWOOD (IN)"]    = ["47", False]
        self.greenLineStations["OVERBROOK (IN)"]    = ["56", False]

        # select default block
        self.selectedBlock      = 1
        self.selectedBlockLine  = self.redLineBlocks
        self.redLineTrains      = TrainDictionary()
        self.greenLineTrains    = TrainDictionary()
        self.scheduleParser     = ScheduleParser()

    def setupUi(self):
        self.setObjectName("self")
        self.setGeometry(50, 50, 700, 580)
        self.setMouseTracking(True)
        self.redLineMaintenance   = False
        self.greenLineMaintenance = False
        self.manualMode           = True
        self.tenTimeSpeed         = False
        self.clockSpeed           = 1000

        font = QtGui.QFont()
        font.setPointSize(16)
        self.clockLabel = QtWidgets.QLabel(self)
        self.clockLabel.setGeometry(QtCore.QRect(550, 35, 140, 25))
        self.clockLabel.setObjectName("clockLabel")
        self.clockLabel.setStyleSheet("background-color: #7b8fb0; border: 1px solid black")
        self.clockLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clockLabel.setFont(font)

        self.throughPutTable = QTableWidget(self)
        self.throughPutTable.setRowCount(2)
        self.throughPutTable.setColumnCount(1)
        self.throughPutTable.setGeometry(550, 180, 140, 60)
        self.throughPutTable.verticalHeader().setDefaultSectionSize(20)
        self.throughPutTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.throughPutTable.setVerticalHeaderLabels(['Red', 'Green'])
        self.throughPutTable.setHorizontalHeaderLabels(['ThroughPut'])

    ##################### RED LINE ##########################
        font.setPointSize(10)
        self.redLineLabelTable = QTableWidget(self)
        self.redLineLabelTable.setRowCount(0)
        self.redLineLabelTable.setColumnCount(1)
        self.redLineLabelTable.setGeometry(10,10,260,25)
        self.redLineLabelTable.setColumnWidth(0, 260)
        self.redLineLabelTable.setHorizontalHeaderLabels(['Red Line'])
        self.redLineBlockTable = QTableWidget(self)
        self.redLineBlockTable.setRowCount(self.redLineBlocks.len())
        self.redLineBlockTable.setColumnCount(4)
        self.redLineBlockTable.setColumnWidth(0, 40)
        self.redLineBlockTable.setColumnWidth(3, 40)
        self.redLineBlockTable.setGeometry(10,30,260,289)
        self.redLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Station','Xing'])
        self.redLineBlockTable.horizontalHeader().setFont(font)
        self.redLineBlockTable.verticalHeader().hide()
        self.redLineBlockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.redLineBlockTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.redLineBlockTable.itemClicked.connect(self.redBlockSelectionChanged)
        self.redLineBlockTable.clicked.connect(self.redBlockSelectionChanged)
        self.selectedBlockTable = self.redLineBlockTable

        for row in range(0,self.redLineBlockTable.rowCount()):
            self.redLineBlockTable.setRowHeight(row, 10)

        self.redLineBlockTable.show()

        self.redLineTrainTable = QTableWidget(self)
        self.redLineTrainTable.setColumnCount(1)
        self.redLineTrainTable.setColumnWidth(0,130)
        self.redLineTrainTable.setGeometry(10,319,130,120)
        self.redLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.redLineTrainTable.verticalHeader().hide()
        self.redLineTrainTable.itemClicked.connect(self.redTrainSelectionChanged)
        self.redLineTrainTable.show()

        self.redLineBacklogTable = QTableWidget(self)
        self.redLineBacklogTable.setColumnCount(1)
        self.redLineBacklogTable.setColumnWidth(0,130)
        self.redLineBacklogTable.setGeometry(140,319,130,120)
        self.redLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.redLineBacklogTable.verticalHeader().hide()
        self.redLineBacklogTable.show()

    ##################### GREEN LINE ########################
        font.setPointSize(10)
        self.greenLineLabelTable = QTableWidget(self)
        self.greenLineLabelTable.setRowCount(0)
        self.greenLineLabelTable.setColumnCount(1)
        self.greenLineLabelTable.setGeometry(280,10,260,25)
        self.greenLineLabelTable.setColumnWidth(0, 260)
        self.greenLineLabelTable.setHorizontalHeaderLabels(['Green Line'])
        self.greenLineBlockTable = QTableWidget(self)
        self.greenLineBlockTable.setRowCount(self.greenLineBlocks.len())
        self.greenLineBlockTable.setColumnCount(4)
        self.greenLineBlockTable.setColumnWidth(0, 40)
        self.greenLineBlockTable.setColumnWidth(3, 41)
        self.greenLineBlockTable.setGeometry(280,30,260,289)
        self.greenLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Station','Xing'])
        self.greenLineBlockTable.horizontalHeader().setFont(font)
        self.greenLineBlockTable.verticalHeader().hide()
        self.greenLineBlockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.greenLineBlockTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.greenLineBlockTable.itemClicked.connect(self.greenBlockSelectionChanged)
        self.greenLineBlockTable.clicked.connect(self.greenBlockSelectionChanged)

        for row in range(0,self.greenLineBlockTable.rowCount()):
            self.greenLineBlockTable.setRowHeight(row, 10)

        self.greenLineBlockTable.show()

        self.greenLineTrainTable = QTableWidget(self)
        self.greenLineTrainTable.setColumnCount(1)
        self.greenLineTrainTable.setColumnWidth(0,130)
        self.greenLineTrainTable.setGeometry(280,319,130,120)
        self.greenLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.greenLineTrainTable.verticalHeader().hide()
        self.greenLineTrainTable.itemClicked.connect(self.greenTrainSelectionChanged)
        self.greenLineTrainTable.show()

        self.greenLineBacklogTable = QTableWidget(self)
        self.greenLineBacklogTable.setColumnCount(1)
        self.greenLineBacklogTable.setColumnWidth(0,130)
        self.greenLineBacklogTable.setGeometry(410,319,130,120)
        self.greenLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.greenLineBacklogTable.verticalHeader().hide()
        self.greenLineBacklogTable.show()

    ##################### BLOCK INFO ########################
        self.blockInfoTable = QTableWidget(self)
        self.blockInfoTable.setRowCount(5)
        self.blockInfoTable.verticalHeader().setDefaultSectionSize(20)
        self.blockInfoTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.blockInfoTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.blockInfoTable.setColumnCount(1)
        self.blockInfoTable.setGeometry(550,260,140,102)
        self.blockInfoTable.horizontalHeader().hide()
        self.blockInfoTable.setVerticalHeaderLabels(['Line','Number','Occupancy','Fault','Maintenance'])
        self.blockInfoTable.show()

        self.toggleMaintenanceButton = QtWidgets.QPushButton(self)
        self.toggleMaintenanceButton.setGeometry(550,360,140,20)
        self.toggleMaintenanceButton.setText("Toggle Maintenance")
        self.toggleMaintenanceButton.clicked.connect(self.toggleMaintenance)
        self.toggleMaintenanceButton.show()

        self.toggleSwitchButton = QtWidgets.QPushButton(self)
        self.toggleSwitchButton.setGeometry(550,380,140,20)
        self.toggleSwitchButton.setText("Toggle Switch")
        self.toggleSwitchButton.clicked.connect(self.toggleSwitch)
        self.toggleSwitchButton.show()

    ##################### TRAIN INFO ########################
        self.destinationTable = QtWidgets.QTableWidget(self)
        self.destinationTable.setGeometry(10,450,285,120)
        self.destinationTable.setColumnCount(2)
        self.destinationTable.setColumnWidth(0, 160)
        self.destinationTable.setColumnWidth(1, 123)
        self.destinationTable.verticalHeader().hide()
        self.destinationTable.setHorizontalHeaderLabels(['Station', 'Stopping'])
        self.destinationTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.destinationTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.destinationTable.show()

        self.dispatchTrainButton = QtWidgets.QPushButton(self)
        self.dispatchTrainButton.setGeometry(550,70,140,25)
        self.dispatchTrainButton.setText("Dispatch")
        self.dispatchTrainButton.show()
        self.dispatchTrainButton.clicked.connect(self.launchDispatchPopUp)

        self.uploadScheduleButton = QtWidgets.QPushButton(self)
        self.uploadScheduleButton.setGeometry(550,70,140,25)
        self.uploadScheduleButton.setText("Upload Schedule")
        self.uploadScheduleButton.clicked.connect(self.uploadSchedule)
        self.uploadScheduleButton.hide()

        self.toggleDispatchModeButton = QtWidgets.QPushButton(self)
        self.toggleDispatchModeButton.setGeometry(550,105,140,25)
        self.toggleDispatchModeButton.setText("Toggle Dispatch Mode")
        self.toggleDispatchModeButton.show()
        self.toggleDispatchModeButton.clicked.connect(self.toggleDispatchMode)

        self.toggleDestinationsButton = QtWidgets.QPushButton(self)
        self.toggleDestinationsButton.setGeometry(300,545,140,20)
        self.toggleDestinationsButton.setText("Toggle Destinations")
        self.toggleDestinationsButton.clicked.connect(self.toggleDestinations)
        self.toggleDestinationsButton.show()

        self.suggestedSpeedLabel = QtWidgets.QLabel(self)
        self.suggestedSpeedLabel.setGeometry(300,520,140,20)
        self.suggestedSpeedLabel.setText("Suggested Speed: N/A")
        self.suggestedSpeedLabel.show()

        self.selectedTrainLabel = QtWidgets.QLabel(self)
        self.selectedTrainLabel.setGeometry(300,495,140,20)
        self.selectedTrainLabel.setText("Selected Train: N/A")
        self.selectedTrainLabel.show()

        self.trainImage          = QtWidgets.QLabel(self)
        self.pixmap              = QPixmap('LogoCTCOffice1.png')
        self.trainImage.setPixmap(self.pixmap)
        self.trainImage.setGeometry(500,440,200,120)

        self.populateRedLineTable()
        self.populateGreenLineTable()

        # set up timer refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRedLineTrainTable)
        self.timer.timeout.connect(self.updateGreenLineTrainTable)
        self.timer.timeout.connect(self.updateBlockTable)
        self.timer.timeout.connect(self.updateRedLineBacklog)
        self.timer.timeout.connect(self.updateGreenLineBacklog)
        self.timer.timeout.connect(self.checkForScheduledTrains)
        self.timer.timeout.connect(self.updateAllBlocks)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(10)

        # set up clock timer
        self.clock = QtCore.QTimer()
        self.clock.timeout.connect(self.tickClock)
        self.startClock()
        #self.show()

    def tickClock(self):
        self.seconds = int(self.seconds)
        self.minutes = int(self.minutes)
        self.hours   = int(self.hours)

        self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1
        if self.minutes == 60:
            self.hours += 1
            self.minutes = 0
        if self.hours == 24:
            self.hours = 0

    def showTime(self):
        secs = ('%02d' % int(self.seconds))
        mins = ('%02d' % int(self.minutes))
        hours = ('%02d' % int(self.hours))
        self.clockWithoutSeconds = (str(hours) + ":" + str(mins))
        self.clockLabel.setText(str(hours) + ":" + str(mins) + ":" + str(secs))
        self.signals.timeSignal.emit([self.hours, self.minutes, self.seconds])

    def changeClockSpeed(self, msg):
        self.clockSpeed = int(1000 / msg)
        self.startClock()

    def startClock(self):
        self.clock.start(self.clockSpeed)

    def populateRedLineTable(self):
        font = QtGui.QFont()
        font.setPointSize(7)
        for key in self.redLineBlocks.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.redLineBlockTable.setItem(int(key)-1, 0, item)

        for key in self.redLineBlocks.keys():
           if (self.redLineBlocks.switch(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.redLineBlocks.switch(key)[0] + " " + str(self.redLineBlocks.switch(key)[1]))
                item.setFont(font)
                self.redLineBlockTable.setItem(int(key)-1, 1, item)

        for key in self.redLineBlocks.keys():
           if (self.redLineBlocks.crossing(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.redLineBlocks.crossing(key))
                self.redLineBlockTable.setItem(int(key)-1, 3, item)

        for key in self.redLineStations.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            item.setFont(font)
            self.redLineBlockTable.setItem(int(self.redLineStations[key][0])-1, 2, item)

        self.redLineBlockTable.resizeColumnToContents(1)

    def populateGreenLineTable(self):
        font = QtGui.QFont()
        font.setPointSize(7)
        for key in self.greenLineBlocks.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.greenLineBlockTable.setItem(int(key)-1, 0, item)

        for key in self.greenLineBlocks.keys():
            if (self.greenLineBlocks.switch(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.greenLineBlocks.switch(key)[0] + " " + str(self.greenLineBlocks.switch(key)[1]))
                item.setFont(font)
                self.greenLineBlockTable.setItem(int(key)-1, 1, item)

        for key in self.greenLineBlocks.keys():
            if (self.greenLineBlocks.crossing(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.greenLineBlocks.crossing(key))
                self.greenLineBlockTable.setItem(int(key)-1, 3, item)

        for key in self.greenLineStations.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            item.setFont(font)
            self.greenLineBlockTable.setItem(int(self.greenLineStations[key][0])-1, 2, item)

        self.greenLineBlockTable.resizeColumnToContents(1)

    def updateRedLineTrainTable(self):
        # TODO checking for removed trains
        self.currentRedLineTrains = []
        for i in range(self.redLineTrainTable.rowCount()):
            self.currentRedLineTrains.append(self.redLineTrainTable.item(i,0).text())
        # checking for new trains
        for key in self.redLineTrains.keys():
            if ((key in self.currentRedLineTrains) == False):
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                rowPosition = self.redLineTrainTable.rowCount()
                self.redLineTrainTable.insertRow(rowPosition)
                self.redLineTrainTable.setItem(rowPosition, 0, item)
                self.currentRedLineTrains = self.redLineTrains.keys()

    def updateRedLineBacklog(self):
        self.currentRedLineBacklog = []
        for i in range(self.redLineBacklogTable.rowCount()):
            time = self.redLineBacklogTable.item(i,0).text()
            if not(time in self.redLineTrains.backlogs()):
                self.redLineBacklogTable.removeRow(i)
            self.currentRedLineBacklog.append(time)

        for train in self.redLineTrains.backlogs():
            if ((train in self.currentRedLineBacklog) == False):
                item = QtWidgets.QTableWidgetItem()
                item.setText(train)
                rowPosition = self.redLineBacklogTable.rowCount()
                self.redLineBacklogTable.insertRow(rowPosition)
                self.redLineBacklogTable.setItem(rowPosition, 0, item)
                self.currentRedLineBacklog = self.redLineTrains.backlogs()

    def updateGreenLineTrainTable(self):
        # TODO checking for removed trains
        self.currentGreenLineTrains = []
        for i in range(self.greenLineTrainTable.rowCount()):
            self.currentGreenLineTrains.append(self.greenLineTrainTable.item(i,0).text())
        # checking for new trains
        for key in self.greenLineTrains.keys():
            if ((key in self.currentGreenLineTrains) == False):
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                rowPosition = self.greenLineTrainTable.rowCount()
                self.greenLineTrainTable.insertRow(rowPosition)
                self.greenLineTrainTable.setItem(rowPosition, 0, item)
                self.currentGreenLineTrains = self.greenLineTrains.keys()

    def updateGreenLineBacklog(self):
        self.currentGreenLineBacklog = []
        for i in range(self.greenLineBacklogTable.rowCount()):
            time = self.greenLineBacklogTable.item(i,0).text()
            if not(time in self.greenLineTrains.backlogs()):
                self.greenLineBacklogTable.removeRow(i)
            self.currentGreenLineBacklog.append(time)

        for train in self.greenLineTrains.backlogs():
            if ((train in self.currentGreenLineBacklog) == False):
                item = QtWidgets.QTableWidgetItem()
                item.setText(train)
                rowPosition = self.greenLineBacklogTable.rowCount()
                self.greenLineBacklogTable.insertRow(rowPosition)
                self.greenLineBacklogTable.setItem(rowPosition, 0, item)
                self.currentGreenLineBacklog = self.greenLineTrains.backlogs()

    def updateDestinationTable(self):
        index = 0
        self.destinationTable.clear()
        self.destinationTable.setHorizontalHeaderLabels(['Station', 'Stopping'])
        self.destinationTable.setRowCount(len(self.selectedTrainStations))
        for key in self.selectedTrainStations.keys():
            item1 = QtWidgets.QTableWidgetItem()
            item1.setText(key)
            self.destinationTable.setItem(index, 0, item1)
            item2 = QtWidgets.QTableWidgetItem()
            item2.setText(str(self.selectedTrainStations[key][1]))
            self.destinationTable.setItem(index, 1, item2)
            index += 1

    def updateTrainInfo(self):
        speed = int(self.selectedTrainLine.getSuggestedSpeed(self.selectedTrain))
        self.suggestedSpeedLabel.setText("Suggested Speed: " + str(speed*2.23694) + " mph")
        self.selectedTrainLabel.setText("Selected Train: " + self.selectedTrain)

    def redBlockSelectionChanged(self):
        self.selectedBlock = self.redLineBlockTable.currentRow() + 1
        self.selectedBlockLine = self.redLineBlocks
        self.selectedBlockTable = self.redLineBlockTable

    def redTrainSelectionChanged(self):
        currentRow = self.redLineTrainTable.currentRow()
        self.selectedTrain = self.redLineTrainTable.item(currentRow, 0).text()
        self.selectedTrainLine = self.redLineTrains
        self.selectedTrainStations = self.redLineTrains.getDestination(self.selectedTrain)
        self.updateDestinationTable()
        self.updateTrainInfo()

    def greenBlockSelectionChanged(self):
        self.selectedBlock = self.greenLineBlockTable.currentRow() + 1
        self.selectedBlockLine = self.greenLineBlocks
        self.selectedBlockTable = self.greenLineBlockTable

    def greenTrainSelectionChanged(self):
        currentRow = self.greenLineTrainTable.currentRow()
        self.selectedTrain = self.greenLineTrainTable.item(currentRow, 0).text()
        self.selectedTrainLine = self.greenLineTrains
        self.selectedTrainStations = self.greenLineTrains.getDestination(self.selectedTrain)
        self.updateDestinationTable()
        self.updateTrainInfo()

    def updateBlockTable(self):
        item = QtWidgets.QTableWidgetItem()
        item.setText(self.selectedBlockLine.getLine(str(self.selectedBlock)))
        self.blockInfoTable.setItem(0,0,item)
        item = QtWidgets.QTableWidgetItem()
        item.setText(str(self.selectedBlock))
        self.blockInfoTable.setItem(1,0,item)
        self.updateOccupancy()
        self.updateFaultState()
        self.updateMaintenanceState()

    def updateAllBlocks(self):
        for key in self.greenLineBlocks.keys():
            if self.greenLineBlocks.getMaintenanceState(key):
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,255,0))
            elif self.greenLineBlocks.getFaultState(key):
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,0,0))
            elif self.greenLineBlocks.getOccupancy(key):
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(20,107,43))
            elif self.greenLineBlocks.getAuthority(key):
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(135,201,153))
            else:
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(116,124,138))

        for key in self.redLineBlocks.keys():
            if self.redLineBlocks.getMaintenanceState(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,255,0))
            elif self.redLineBlocks.getFaultState(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,0,0))
            elif self.redLineBlocks.getOccupancy(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(20,107,43))
            elif self.redLineBlocks.getAuthority(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(135,201,153))
            else:
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(116,124,138))

    def updateOccupancy(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getOccupancy(str(self.selectedBlock))
        item.setText(str(state))
        self.blockInfoTable.setItem(2,0,item)

    def updateFaultState(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getFaultState(str(self.selectedBlock))
        item.setText(str(state))
        self.blockInfoTable.setItem(3,0,item)

    def updateMaintenanceState(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getMaintenanceState(str(self.selectedBlock))
        item.setText(str(state))
        self.blockInfoTable.setItem(4,0,item)

    def updateSwitchState(self, switchSignal):
        item = QtWidgets.QTableWidgetItem()
        if switchSignal[0] == 0:
            self.redLineBlocks.setSwitchState(str(switchSignal[1]), switchSignal[2])
            currentSwitch = self.redLineBlocks.switch(str(switchSignal[1]))
            print("current swtich" + currentSwitch)
            item.setText(str(currentSwitch) + " " + str(switchSignal[2]))
            self.redLineBlockTable.setItem(switchSignal[1]-1, 1, item)
        else:
            self.greenLineBlocks.setSwitchState(str(switchSignal[1]), switchSignal[2])
            currentSwitch = self.greenLineBlocks.switch(str(switchSignal[1]))
            item.setText(str(currentSwitch) + " " + str(switchSignal[2]))
            self.greenLineBlockTable.setItem(switchSignal[1]-1, 1, item)

    def toggleMaintenance(self):
        self.selectedBlockLine.toggleMaintenanceState(str(self.selectedBlock))
        maintenanceState = self.selectedBlockLine.getMaintenanceState(str(self.selectedBlock))
        if self.selectedBlockLine == self.greenLineBlocks:
            self.signals.signalMaintenance.emit([1, self.selectedBlock, maintenanceState])
            self.greenLineMaintenance = maintenanceState
        else:
            self.signals.signalMaintenance.emit([0, self.selectedBlock, maintenanceState])
            self.redLineMaintenance = maintenanceState
        self.updateMaintenanceState()

    def toggleSwitch(self):
        font = QtGui.QFont()
        font.setPointSize(7)
        # check if block has switch
        if self.selectedBlockLine.switch(str(self.selectedBlock)) == 0:
            return
        # if block has switch, toggle it
        currentSwitchState = self.selectedBlockLine.getSwitchState(str(self.selectedBlock))
        if self.selectedBlockLine == self.greenLineBlocks and self.greenLineMaintenance:
            self.selectedBlockLine.setSwitchState(str(self.selectedBlock), not currentSwitchState[1])
            currentSwitch = self.selectedBlockLine.switch(str(self.selectedBlock))
            self.signals.ctcSwitchState.emit([1,int(self.selectedBlock),not currentSwitchState[1]])
        elif self.selectedBlockLine == self.redLineBlocks and self.redLineMaintenance:
            self.selectedBlockLine.setSwitchState(str(self.selectedBlock), not currentSwitchState[1])
            currentSwitch = self.selectedBlockLine.switch(str(self.selectedBlock))
            self.signals.ctcSwitchState.emit([0,int(self.selectedBlock),not currentSwitchState[1]])
        else:
            return
        # change switch label
        item = QtWidgets.QTableWidgetItem()
        item.setText(str(currentSwitch[0]) + " " + str(not currentSwitchState[1]))
        item.setFont(font)
        self.selectedBlockTable.setItem(int(self.selectedBlock)-1,1,item)

    def launchDispatchPopUp(self):
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = DispatchPopUp(self.signals)
        self.dispatchPopUp.setupUi(self.dispatchWidget, self.redLineStations, self.greenLineStations, self.redLineTrains, self.greenLineTrains, self.trainCount)
        self.dispatchPopUp.dispatch.clicked.connect(self.closeDispatchPopUp)
        self.dispatchWidget.show()

    def closeDispatchPopUp(self):
        if self.dispatchPopUp.dispatch.text() == "Dispatch":
            self.trainCount += 1
        self.dispatchWidget.close()

    def uploadSchedule(self):
        fileName = QFileDialog.getOpenFileName(QtWidgets.QStackedWidget(), 'open file', '/home/garrett/git/ECE_1140_TRAINS/CTC-Office', 'csv files (*.csv)')
        if self.scheduleParser.loadSchedule(fileName[0], self.redLineStations, self.greenLineStations, self.redLineTrains, self.greenLineTrains, self.trainCount):
            self.trainCount += 1
        else:
            print("ERROR: invalid schedule uploaded")

    def checkForScheduledTrains(self):
        trainName = "Train " + str(self.trainCount)
        for train in list(self.redLineTrains.backlogs()):
            if str(train) == self.clockWithoutSeconds:
                self.redLineTrains.dispatchScheduledTrain(self.clockWithoutSeconds, trainName)
                suggestedSpeed = self.redLineTrains.getSuggestedSpeed(trainName)
                self.signals.dispatchTrainSignal.emit([trainName, "Red Line", suggestedSpeed])
                self.redLineTrains.sendAuthority(trainName, self.signals)
                self.trainCount += 1

        for train in list(self.greenLineTrains.backlogs()):
            if str(train) == self.clockWithoutSeconds:
                self.greenLineTrains.dispatchScheduledTrain(self.clockWithoutSeconds, trainName)
                suggestedSpeed = self.greenLineTrains.getSuggestedSpeed(trainName)
                self.signals.dispatchTrainSignal.emit([trainName, "Green Line", suggestedSpeed])
                self.greenLineTrains.sendAuthority(trainName, self.signals)
                self.trainCount += 1

    def toggleDestinations(self):
        self.selectedDestinations = self.destinationTable.selectedIndexes()
        for selection in self.selectedDestinations:
            destination = self.destinationTable.itemFromIndex(selection).text()
            if (destination != "True" and destination != "False"):
               self.selectedTrainLine.toggleDestination(self.selectedTrain, destination, False)
        self.updateDestinationTable()
        self.selectedTrainLine.sendAuthority(self.selectedTrain, self.signals)

    def readOccupancySignal(self, occupancySignal):
        for block in range(0, len(occupancySignal[1])):
            self.greenLineBlocks.setOccupancy(str(block+1), occupancySignal[1][block])
        for block in range(0, len(occupancySignal[0])):
            self.redLineBlocks.setOccupancy(str(block+1), occupancySignal[0][block])

    def readFaultSignal(self, faultSignal):
        for block in range(0, len(faultSignal[1])):
            if faultSignal[1][block] != 0:
                self.greenLineBlocks.setFaultState(str(block+1), True)
            else:
                self.greenLineBlocks.setFaultState(str(block+1), False)
        for block in range(0, len(faultSignal[0])):
            if faultSignal[0][block] != 0:
                self.redLineBlocks.setFaultState(str(block+1), True)
            else:
                self.redLineBlocks.setFaultState(str(block+1), False)

    def toggleDispatchMode(self):
        if self.manualMode:
            self.dispatchTrainButton.hide()
            self.toggleMaintenanceButton.hide()
            self.toggleSwitchButton.hide()
            self.uploadScheduleButton.show()
            self.manualMode = False
        else:
            self.dispatchTrainButton.show()
            self.toggleMaintenanceButton.show()
            self.toggleSwitchButton.show()
            self.uploadScheduleButton.hide()
            self.manualMode = True

    def showAuthority(self, msg):
        pass
        # red line
        if msg[0] == 0:
            for block in self.redLineBlocks.keys():
                if int(block) in msg[2]:
                    self.redLineBlocks.setAuthority(block, True)
                else:
                    self.redLineBlocks.setAuthority(block, False)
        elif msg[0] == 1:
            for block in self.greenLineBlocks.keys():
                if int(block) in msg[2]:
                    self.greenLineBlocks.setAuthority(block, True)
                else:
                    self.greenLineBlocks.setAuthority(block, False)
        else:
            return

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    signals = Signals()
    mainUi = CTCOffice(signals)

    sys.exit(app.exec_())
