from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QTime, pyqtSignal
import sys, os

sys.path.append('../train-functionality/')
sys.path.append('../block-functionality/')
sys.path.append('../schedule-functionality/')
sys.path.append('../../SystemSignals/')
from TrainDictionary import TrainDictionary
from LayoutParser import LayoutParser
from DispatchPopUp import DispatchPopUp
from ScheduleParser import ScheduleParser
from Signals import Signals

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

    def setupLayout(self):
        # getting lists of blocks
        layoutFile              = 'Track_Layout_PGH_Light_Rail.csv'
        trackLayout             = LayoutParser(layoutFile)
        self.redLineBlocks, self.greenLineBlocks = trackLayout.process()

        # Create default station dictionary
        self.redLineStations    = dict()
        self.greenLineStations  = dict()

        # define station lists in order    
        for key, value in self.redLineBlocks.stations().items():
            self.redLineStations[value]     = [key, False]

        self.greenLineStations["GLENBURY"]       = ["65", False]
        self.greenLineStations["DORMONT"]        = ["76", False]
        self.greenLineStations["MT-LEBANON"]     = ["77", False]
        self.greenLineStations["POPLAR"]         = ["88", False]
        self.greenLineStations["CASTE SHANNON"]  = ["77", False]
        self.greenLineStations["MT-LEBANON"]     = ["77", False]
        self.greenLineStations["GLENBURY"]       = ["114", False]
        self.greenLineStations["OVERBROOK (OUT)"]= ["122", False]
        self.greenLineStations["INGLEWOOD (OUT)"]= ["131", False]
        self.greenLineStations["CENTRAL (OUT)"]  = ["140", False]
        self.greenLineStations["WHITED"]         = ["22", False]
        self.greenLineStations["SUSHVILLE"]      = ["16", False]
        self.greenLineStations["EDGEBROOK"]      = ["9", False]
        self.greenLineStations["PIONEER"]        = ["2", False]
        self.greenLineStations["SOUTH BANK"]     = ["31", False]
        self.greenLineStations["CENTRAL (IN)"]   = ["38", False]
        self.greenLineStations["INGLEWOOD (IN)"] = ["47", False]
        self.greenLineStations["OVERBROOK (IN)"] = ["56", False]

        # select default block
        self.selectedBlock      = 1
        self.selectedBlockLine  = self.redLineBlocks
        self.redLineTrains      = TrainDictionary()
        self.greenLineTrains    = TrainDictionary()
        self.scheduleParser     = ScheduleParser()

    def setupUi(self):
        self.setObjectName("self")
        self.setGeometry(10, 10, 600, 580)
        self.setMouseTracking(True)
        self.redLineMaintenance   = False
        self.greenLineMaintenance = False
        self.manualMode           = True
        self.tenTimeSpeed         = False
        self.clockSpeed           = 1000

        font = QtGui.QFont()
        font.setPointSize(16)
        self.clockLabel = QtWidgets.QLabel(self)
        self.clockLabel.setGeometry(QtCore.QRect(450, 35, 140, 25))
        self.clockLabel.setObjectName("clockLabel")
        self.clockLabel.setStyleSheet("background-color: gray; border: 1px solid black")
        self.clockLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clockLabel.setFont(font)

        self.changeClockSpeedButton = QtWidgets.QPushButton(self)
        self.changeClockSpeedButton.setGeometry(450,15,140,20)
        self.changeClockSpeedButton.setText("Change clock speed")
        self.changeClockSpeedButton.clicked.connect(self.toggleTenTimeSpeed)

    ##################### RED LINE ##########################
        self.redLineLabelTable = QTableWidget(self)
        self.redLineLabelTable.setRowCount(0)
        self.redLineLabelTable.setColumnCount(1)
        self.redLineLabelTable.setGeometry(10,15,210,20)
        self.redLineLabelTable.setColumnWidth(0, 210)
        self.redLineLabelTable.setHorizontalHeaderLabels(['Red Line'])
        self.redLineBlockTable = QTableWidget(self)
        self.redLineBlockTable.setRowCount(self.redLineBlocks.len())
        self.redLineBlockTable.setColumnCount(3)
        self.redLineBlockTable.setColumnWidth(0, 40)
        self.redLineBlockTable.setColumnWidth(2, 40)
        self.redLineBlockTable.setGeometry(10,30,210,289)
        self.redLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
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
        self.redLineTrainTable.setGeometry(10,319,105,120)
        self.redLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.redLineTrainTable.verticalHeader().hide()
        self.redLineTrainTable.itemClicked.connect(self.redTrainSelectionChanged)
        self.redLineTrainTable.show()

        self.redLineBacklogTable = QTableWidget(self)
        self.redLineBacklogTable.setColumnCount(1)
        self.redLineBacklogTable.setGeometry(115,319,105,120)
        self.redLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.redLineBacklogTable.verticalHeader().hide()
        self.redLineBacklogTable.show()

    ##################### GREEN LINE ########################
        self.greenLineLabelTable = QTableWidget(self)
        self.greenLineLabelTable.setRowCount(0)
        self.greenLineLabelTable.setColumnCount(1)
        self.greenLineLabelTable.setGeometry(230,15,210,20)
        self.greenLineLabelTable.setColumnWidth(0, 210)
        self.greenLineLabelTable.setHorizontalHeaderLabels(['Green Line'])
        self.greenLineBlockTable = QTableWidget(self)
        self.greenLineBlockTable.setRowCount(self.greenLineBlocks.len())
        self.greenLineBlockTable.setColumnCount(3)
        self.greenLineBlockTable.setColumnWidth(0, 40)
        self.greenLineBlockTable.setColumnWidth(2, 41)
        self.greenLineBlockTable.setGeometry(230,30,210,289)
        self.greenLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
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
        self.greenLineTrainTable.setGeometry(230,319,105,120)
        self.greenLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.greenLineTrainTable.verticalHeader().hide()
        self.greenLineTrainTable.itemClicked.connect(self.greenTrainSelectionChanged)
        self.greenLineTrainTable.show()

        self.greenLineBacklogTable = QTableWidget(self)
        self.greenLineBacklogTable.setColumnCount(1)
        self.greenLineBacklogTable.setGeometry(335,319,105,120)
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
        self.blockInfoTable.setGeometry(450,210,140,102)
        self.blockInfoTable.horizontalHeader().hide()
        self.blockInfoTable.setVerticalHeaderLabels(['Line','Number','Occupancy','Fault','Maintenance'])
        self.blockInfoTable.show()

        self.toggleMaintenanceButton = QtWidgets.QPushButton(self)
        self.toggleMaintenanceButton.setGeometry(450,310,140,20)
        self.toggleMaintenanceButton.setText("Toggle Maintenance")
        self.toggleMaintenanceButton.clicked.connect(self.toggleMaintenance)
        self.toggleMaintenanceButton.show()

    ##################### TRAIN INFO ########################
        self.destinationTable = QtWidgets.QTableWidget(self)
        self.destinationTable.setGeometry(10,450,250,120)
        self.destinationTable.setColumnCount(2)
        self.destinationTable.setColumnWidth(0, 160)
        self.destinationTable.setColumnWidth(1, 88)
        self.destinationTable.verticalHeader().hide()
        self.destinationTable.setHorizontalHeaderLabels(['Station', 'Stopping'])
        self.destinationTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.destinationTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.destinationTable.show()

        self.dispatchTrainButton = QtWidgets.QPushButton(self)
        self.dispatchTrainButton.setGeometry(450,70,140,25)
        self.dispatchTrainButton.setText("Dispatch")
        self.dispatchTrainButton.show()
        self.dispatchTrainButton.clicked.connect(self.launchDispatchPopUp)

        self.uploadScheduleButton = QtWidgets.QPushButton(self)
        self.uploadScheduleButton.setGeometry(450,70,140,25)
        self.uploadScheduleButton.setText("Upload Schedule")
        self.uploadScheduleButton.clicked.connect(self.uploadSchedule)
        self.uploadScheduleButton.hide()

        self.toggleDispatchModeButton = QtWidgets.QPushButton(self)
        self.toggleDispatchModeButton.setGeometry(450,105,140,25)
        self.toggleDispatchModeButton.setText("Toggle Dispatch Mode")
        self.toggleDispatchModeButton.show()
        self.toggleDispatchModeButton.clicked.connect(self.toggleDispatchMode)

        self.toggleDestinationsButton = QtWidgets.QPushButton(self)
        self.toggleDestinationsButton.setGeometry(265,545,140,20)
        self.toggleDestinationsButton.setText("Toggle Destinations")
        self.toggleDestinationsButton.clicked.connect(self.toggleDestinations)
        self.toggleDestinationsButton.show()

        self.suggestedSpeedLabel = QtWidgets.QLabel(self)
        self.suggestedSpeedLabel.setGeometry(265,520,140,20)
        self.suggestedSpeedLabel.setText("Suggested Speed: N/A")
        self.suggestedSpeedLabel.show()

        self.selectedTrainLabel = QtWidgets.QLabel(self)
        self.selectedTrainLabel.setGeometry(265,495,140,20)
        self.selectedTrainLabel.setText("Selected Train: N/A")
        self.selectedTrainLabel.show()

        self.trainImage          = QtWidgets.QLabel(self)
        self.pixmap              = QPixmap('Train.png')
        self.trainImage.setPixmap(self.pixmap)
        self.trainImage.setGeometry(420,430,200,200)

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
        self.show()

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
        self.clockLabel.setText(str(hours) + ":" + str(mins))
        self.signals.timeSignal.emit([self.hours, self.minutes])

    def toggleTenTimeSpeed(self):
        self.tenTimeSpeed = not self.tenTimeSpeed
        if self.tenTimeSpeed:
            self.clockSpeed = 10
            self.signals.clockSpeedSignal.emit(10)
        else:
            self.clockSpeed = 1000
            self.signals.clockSpeedSignal.emit(1)

        self.startClock()

    def startClock(self):
        self.clock.start(self.clockSpeed)

    def populateRedLineTable(self):
        for key in self.redLineBlocks.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.redLineBlockTable.setItem(int(key)-1, 0, item)

        for key in self.redLineBlocks.keys():
           if (self.redLineBlocks.switch(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.redLineBlocks.switch(key)[0] + " " + str(self.redLineBlocks.switch(key)[1]))
                self.redLineBlockTable.setItem(int(key)-1, 1, item)

        for key in self.redLineBlocks.keys():
           if (self.redLineBlocks.crossing(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.redLineBlocks.crossing(key))
                self.redLineBlockTable.setItem(int(key)-1, 2, item)

        self.redLineBlockTable.resizeColumnToContents(1)

    def populateGreenLineTable(self):
        for key in self.greenLineBlocks.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.greenLineBlockTable.setItem(int(key)-1, 0, item)

        for key in self.greenLineBlocks.keys():
           if (self.greenLineBlocks.switch(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.greenLineBlocks.switch(key)[0] + " " + str(self.greenLineBlocks.switch(key)[1]))
                self.greenLineBlockTable.setItem(int(key)-1, 1, item)

        for key in self.greenLineBlocks.keys():
           if (self.greenLineBlocks.crossing(key) != 0):
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.greenLineBlocks.crossing(key))
                self.greenLineBlockTable.setItem(int(key)-1, 2, item)

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
            self.currentRedLineBacklog.append(self.redLineBacklogTable.item(i,0).text())

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
            self.currentGreenLineBacklog.append(self.greenLineBacklogTable.item(i,0).text())

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
        self.suggestedSpeedLabel.setText("Suggested Speed: " + str(speed) + " mph")
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
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(0,255,0))
            else:
                self.greenLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,255,255))

        for key in self.redLineBlocks.keys():
            if self.redLineBlocks.getMaintenanceState(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,255,0))
            elif self.redLineBlocks.getFaultState(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,0,0))
            elif self.redLineBlocks.getOccupancy(key):
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(0,255,0))
            else:
                self.redLineBlockTable.item(int(key)-1,0).setBackground(QtGui.QColor(255,255,255))

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
        self.greenLineBlocks.setSwitchState(switchSignal[0], switchSignal[1])
        item = QtWidgets.QTableWidgetItem()
        #item.setText(self.greenLineBlocks.switch(switchSignal[0])[0] + " " + str(self.greenLineBlocks.switch(switchSignal[0])[1]))

    def toggleMaintenance(self):
        self.selectedBlockLine.toggleMaintenanceState(str(self.selectedBlock))
        maintenanceState = self.selectedBlockLine.getMaintenanceState(str(self.selectedBlock))
        if self.selectedBlockLine == self.greenLineBlocks:
            self.signals.signalMaintenance.emit(["Green", self.selectedBlock, maintenanceState])
        else:
            self.signals.signalMaintenance.emit(["Red", self.selectedBlock, maintenanceState])
        self.updateMaintenanceState()

    def launchDispatchPopUp(self):
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = DispatchPopUp(self.signals)
        self.dispatchPopUp.setupUi(self.dispatchWidget, self.redLineStations, self.greenLineStations, self.redLineTrains, self.greenLineTrains, self.trainCount)
        self.dispatchPopUp.dispatch.clicked.connect(self.closeDispatchPopUp)
        self.dispatchWidget.show()

    def closeDispatchPopUp(self):
        self.dispatchWidget.close()
        self.trainCount += 1

    def uploadSchedule(self):
        fileName = QFileDialog.getOpenFileName(QtWidgets.QStackedWidget(), 'open file', '/home/garrett/git/ECE_1140_TRAINS/CTC-Office', 'csv files (*.csv)')
        self.scheduleParser.loadSchedule(fileName[0], self.redLineStations, self.greenLineStations, self.redLineTrains, self.greenLineTrains)

    def checkForScheduledTrains(self):
        for train in list(self.redLineTrains.backlogs()):
            if str(train) == self.clockLabel.text():
                self.redLineTrains.dispatchScheduledTrain(str(train))

        for train in list(self.greenLineTrains.backlogs()):
            if str(train) == self.clockLabel.text():
                self.greenLineTrains.dispatchScheduledTrain(str(train))

    def toggleDestinations(self):
        self.selectedDestinations = self.destinationTable.selectedIndexes()
        for selection in self.selectedDestinations:
            destination = self.destinationTable.itemFromIndex(selection).text()
            if (destination != "True" and destination != "False"):
               self.selectedTrainLine.toggleDestination(self.selectedTrain, destination, False)
        self.updateDestinationTable()
        self.selectedTrainLine.sendAuthority(self.selectedTrain, self.signals)

    def readOccupancySignal(self, occupancySignal):
        for block in range(0, len(occupancySignal)):
            self.greenLineBlocks.setOccupancy(str(block+1), occupancySignal[block])

    def toggleDispatchMode(self):
        if self.manualMode:
            self.dispatchTrainButton.hide()
            self.toggleMaintenanceButton.hide()
            self.uploadScheduleButton.show()
            self.manualMode = False
        else:
            self.dispatchTrainButton.show()
            self.toggleMaintenanceButton.show()
            self.uploadScheduleButton.hide()
            self.manualMode = True


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    signals = Signals()
    mainUi = CTCOffice(signals)

    sys.exit(app.exec_())
