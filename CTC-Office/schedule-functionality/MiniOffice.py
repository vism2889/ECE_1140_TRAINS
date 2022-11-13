from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTime
import sys

sys.path.append('../train-functionality/')
sys.path.append('../block-functionality/')
sys.path.append('../server-functionality/')
from TrainDictionary import TrainDictionary
from LayoutParser import LayoutParser
from DispatchPopUp import DispatchPopUp
from ScheduleParser import ScheduleParser
from PublisherCTC import PublisherCTC

class Ui_MainWindow(object):
    dispatchSignal = QtCore.pyqtSignal(bool)

#################################################################
# Start UI generation and setup
#################################################################
    def __init__(self, MainWindow, redLineBlocks, greenLineBlocks):
        self.redLineTrains = TrainDictionary()
        self.greenLineTrains = TrainDictionary()
        self.redLineBlocks = redLineBlocks
        self.greenLineBlocks = greenLineBlocks
        self.redLineBlocksKeys = redLineBlocks.keys()
        self.greenLineBlocksKeys = greenLineBlocks.keys()
        self.scheduleParser = ScheduleParser()
        #self.publisherCTC = PublisherCTC()

        # Create default station dictionary
        self.redLineStations = dict()
        self.greenLineStations = dict()
        for value in self.redLineBlocks.stations().values():
            self.redLineStations[value] = False
        for value in self.greenLineBlocks.stations().values():
            self.greenLineStations[value] = False

        self.redLineStations["YARD"] = False
        self.greenLineStations["YARD"] = False

        # select default block
        self.selectedBlock = 1
        self.selectedBlockLine = self.redLineBlocks

        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(10, 10, 600, 580)
        MainWindow.setMouseTracking(True)
        self.redLineMaintenance = False
        self.greenLineMaintenance = False

        font = QtGui.QFont()
        font.setPointSize(16)
        self.clockLabel = QtWidgets.QLabel(MainWindow)
        self.clockLabel.setGeometry(QtCore.QRect(450, 20, 140, 25))
        self.clockLabel.setObjectName("clockLabel")
        self.clockLabel.setStyleSheet("background-color: gray; border: 1px solid black")
        self.clockLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clockLabel.setFont(font)

    ##################### RED LINE ##########################
        self.redLineBlockTable = QTableWidget(MainWindow)
        self.redLineBlockTable.setRowCount(self.redLineBlocks.len())
        self.redLineBlockTable.setColumnCount(3)
        self.redLineBlockTable.setColumnWidth(0, 40)
        self.redLineBlockTable.setColumnWidth(2, 40)
        self.redLineBlockTable.setGeometry(10,20,210,289)
        self.redLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
        self.redLineBlockTable.verticalHeader().hide()
        self.redLineBlockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.redLineBlockTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.redLineBlockTable.itemClicked.connect(self.redBlockSelectionChanged)
        self.selectedBlockTable = self.redLineBlockTable
        self.redLineBlockTable.show()

        self.redLineTrainTable = QTableWidget(MainWindow)
        self.redLineTrainTable.setColumnCount(1)
        self.redLineTrainTable.setGeometry(10,309,105,120)
        self.redLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.redLineTrainTable.verticalHeader().hide()
        self.redLineTrainTable.itemClicked.connect(self.redTrainSelectionChanged)
        self.redLineTrainTable.show()

        self.redLineBacklogTable = QTableWidget(MainWindow)
        self.redLineBacklogTable.setColumnCount(1)
        self.redLineBacklogTable.setGeometry(115,309,105,120)
        self.redLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.redLineBacklogTable.verticalHeader().hide()
        self.redLineBacklogTable.show()

    ##################### GREEN LINE ########################
        self.greenLineBlockTable = QTableWidget(MainWindow)
        self.greenLineBlockTable.setRowCount(self.greenLineBlocks.len())
        self.greenLineBlockTable.setColumnCount(3)
        self.greenLineBlockTable.setColumnWidth(0, 40)
        self.greenLineBlockTable.setColumnWidth(2, 41)
        self.greenLineBlockTable.setGeometry(230,20,210,289)
        self.greenLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
        self.greenLineBlockTable.verticalHeader().hide()
        self.greenLineBlockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.greenLineBlockTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.greenLineBlockTable.itemClicked.connect(self.greenBlockSelectionChanged)
        self.greenLineBlockTable.clicked.connect(self.greenBlockSelectionChanged)
        self.greenLineBlockTable.show()

        self.greenLineTrainTable = QTableWidget(MainWindow)
        self.greenLineTrainTable.setColumnCount(1)
        self.greenLineTrainTable.setGeometry(230,309,105,120)
        self.greenLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.greenLineTrainTable.verticalHeader().hide()
        self.greenLineTrainTable.itemClicked.connect(self.greenTrainSelectionChanged)
        self.greenLineTrainTable.show()

        self.greenLineBacklogTable = QTableWidget(MainWindow)
        self.greenLineBacklogTable.setColumnCount(1)
        self.greenLineBacklogTable.setGeometry(335,309,105,120)
        self.greenLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.greenLineBacklogTable.verticalHeader().hide()
        self.greenLineBacklogTable.show()

    ##################### BLOCK INFO ########################
        self.blockInfoTable = QTableWidget(MainWindow)
        self.blockInfoTable.setRowCount(5)
        self.blockInfoTable.verticalHeader().setDefaultSectionSize(20)
        self.blockInfoTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.blockInfoTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.blockInfoTable.setColumnCount(1)
        self.blockInfoTable.setGeometry(450,200,140,102)
        self.blockInfoTable.horizontalHeader().hide()
        self.blockInfoTable.setVerticalHeaderLabels(['Line','Number','Occupancy','Fault','Maintenance'])
        self.blockInfoTable.show()

        self.toggleMaintenanceButton = QtWidgets.QPushButton(MainWindow)
        self.toggleMaintenanceButton.setGeometry(450,300,140,20)
        self.toggleMaintenanceButton.setText("Toggle Maintenance")
        self.toggleMaintenanceButton.clicked.connect(self.toggleMaintenance)
        self.toggleMaintenanceButton.show()

    ##################### TRAIN INFO ########################
        self.destinationTable = QtWidgets.QTableWidget(MainWindow)
        self.destinationTable.setGeometry(10, 440, 250, 120)
        self.destinationTable.setColumnCount(2)
        self.destinationTable.setColumnWidth(0, 160)
        self.destinationTable.setColumnWidth(1, 88)
        self.destinationTable.verticalHeader().hide()
        self.destinationTable.setHorizontalHeaderLabels(['Station', 'Stopping'])
        self.destinationTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.destinationTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.destinationTable.show()

        self.dispatchTrainButton = QtWidgets.QPushButton(MainWindow)
        self.dispatchTrainButton.setGeometry(450, 55, 140, 25)
        self.dispatchTrainButton.setText("Dispatch")
        self.dispatchTrainButton.show()
        self.dispatchTrainButton.clicked.connect(self.launchDispatchPopUp)

        self.uploadScheduleButton = QtWidgets.QPushButton(MainWindow)
        self.uploadScheduleButton.setGeometry(450, 90, 140, 25)
        self.uploadScheduleButton.setText("Upload Schedule")
        self.uploadScheduleButton.clicked.connect(self.uploadSchedule)
        self.uploadScheduleButton.show()  

        self.toggleDestinationsButton = QtWidgets.QPushButton(MainWindow)
        self.toggleDestinationsButton.setGeometry(265, 535, 120, 25)
        self.toggleDestinationsButton.setText("Toggle Destinations")
        self.toggleDestinationsButton.clicked.connect(self.toggleDestinations)
        self.toggleDestinationsButton.show()

        self.populateRedLineTable()
        self.populateGreenLineTable()

        # set up timer refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRedLineTrainTable)
        self.timer.timeout.connect(self.updateGreenLineTrainTable)
        self.timer.timeout.connect(self.showTime)
        self.timer.timeout.connect(self.updateBlockTable)
        self.timer.timeout.connect(self.updateRedLineBacklog)
        self.timer.timeout.connect(self.updateGreenLineBacklog)
        self.timer.timeout.connect(self.checkForScheduledTrains)
        self.timer.start(100)
        MainWindow.show()

    def showTime(self):
        current_time = QTime.currentTime()
        self.label_time = current_time.toString('hh:mm:ss')
        self.clockLabel.setText(self.label_time)

    def populateRedLineTable(self):
        for key in self.redLineBlocksKeys:
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.redLineBlockTable.setItem(int(key)-1, 0, item)

        for key in self.redLineBlocksKeys:
           if (self.redLineBlocks.switch(key) != 0):      
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.redLineBlocks.switch(key)[0] + " " + str(self.redLineBlocks.switch(key)[1]))
                self.redLineBlockTable.setItem(int(key)-1, 1, item)
                
        for key in self.redLineBlocksKeys:
           if (self.redLineBlocks.crossing(key) != 0):      
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.redLineBlocks.crossing(key))
                self.redLineBlockTable.setItem(int(key)-1, 2, item)        

        self.redLineBlockTable.resizeColumnToContents(1)

    def populateGreenLineTable(self):
        for key in self.greenLineBlocksKeys:
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.greenLineBlockTable.setItem(int(key)-1, 0, item)

        for key in self.greenLineBlocksKeys:
           if (self.greenLineBlocks.switch(key) != 0):      
                item = QtWidgets.QTableWidgetItem()
                item.setText(self.greenLineBlocks.switch(key)[0] + " " + str(self.greenLineBlocks.switch(key)[1]))
                self.greenLineBlockTable.setItem(int(key)-1, 1, item)
                
        for key in self.greenLineBlocksKeys:
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
            item2.setText(str(self.selectedTrainStations[key]))
            self.destinationTable.setItem(index, 1, item2)
            index += 1

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

    def updateOccupancy(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getOccupancy(str(self.selectedBlock))
        item.setText(str(state))
        self.blockInfoTable.setItem(2,0,item)
        if state == True:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(0,255,0))
        else:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,255))

    def updateFaultState(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getFaultState(str(self.selectedBlock))
        item.setText(str(state))
        self.blockInfoTable.setItem(3,0,item)
        if state == True:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,0,0))
        else:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,255))

    def updateMaintenanceState(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getMaintenanceState(str(self.selectedBlock))
        item.setText(str(state))
        self.blockInfoTable.setItem(4,0,item)
        if state == True:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,0))
        else:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,255))

    def toggleMaintenance(self):
        self.selectedBlockLine.toggleMaintenanceState(str(self.selectedBlock))
        self.publishTrackMsg("red")

    def launchDispatchPopUp(self):
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = DispatchPopUp()
        self.dispatchPopUp.setupUi(self.dispatchWidget, self.redLineStations, self.greenLineStations, self.redLineTrains, self.greenLineTrains)
        self.dispatchPopUp.dispatch.clicked.connect(self.closeDispatchPopUp)
        self.dispatchWidget.show()
    
    def closeDispatchPopUp(self):
        self.dispatchWidget.close()
        self.dispatchSignal.emit(True)

    def uploadSchedule(self):
        fileName = QFileDialog.getOpenFileName(QtWidgets.QStackedWidget(), 'open file', '/home/garrett/git/ECE_1140_TRAINS/CTC-Office', 'xlsx files (*.xlsx)')
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
    
    def publishTrackMsg(self, line):
        switchList = []
        maintenanceList = []
        for key in self.redLineBlocks.keys():
            forward = self.redLineBlocks.switch(key)
            if forward != 0:
                if forward[1]:
                    switchList.append(True)
                elif not forward[1]:
                    switchList.append(False)
            
        for key in self.redLineBlocks.keys():
            maintenance = self.redLineBlocks.getMaintenanceState(key)
            if maintenance == True:
                maintenanceList.append(True)
            else:
                maintenanceList.append(False)

        #self.publisherCTC.publishTrackMsg(switchList, maintenanceList, "red")

    def subscribeTrackMsg(self):
        print("here")


if __name__ == "__main__":
    import sys

    # getting lists of blocks
    layoutFile = "Track_Layout_PGH_Light_Rail.csv"
    trackLayout = LayoutParser(layoutFile)
    redLineBlocks, greenLineBlocks = trackLayout.process()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    mainUi = Ui_MainWindow(MainWindow, redLineBlocks, greenLineBlocks)
    MainWindow.show()
    
    sys.exit(app.exec_())
