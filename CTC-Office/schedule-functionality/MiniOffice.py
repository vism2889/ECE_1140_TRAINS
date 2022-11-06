from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTime

from TrainDictionary import TrainDictionary
from LayoutParser import LayoutParser
from DispatchPopUp import DispatchPopUp
import sys

class Ui_MainWindow(object):

#################################################################
# Start UI generation and setup
#################################################################
    def __init__(self, redLineBlocks, greenLineBlocks):
        self.redLineTrains = TrainDictionary()
        self.greenLineTrains = TrainDictionary()
        self.redLineBlocks = redLineBlocks
        self.greenLineBlocks = greenLineBlocks
        self.redLineBlocksKeys = redLineBlocks.keys()
        self.greenLineBlocksKeys = greenLineBlocks.keys()

        # Create default station dictionary
        self.redLineStations = dict()
        self.greenLineStations = dict()
        for value in self.redLineBlocks.stations().values():
            self.redLineStations[value] = "No"
        for value in self.greenLineBlocks.stations().values():
            self.greenLineStations[value] = "No"

        # select default block
        self.selectedBlock = 1
        self.selectedBlockLine = self.redLineBlocks

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(10, 10, 600, 613)
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
        self.redLineBlockTable.setColumnWidth(2, 42)
        self.redLineBlockTable.setGeometry(10,20,210,300)
        self.redLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
        self.redLineBlockTable.verticalHeader().hide()
        self.redLineBlockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.redLineBlockTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.redLineBlockTable.itemClicked.connect(self.redBlockSelectionChanged)
        self.selectedBlockTable = self.redLineBlockTable
        self.redLineBlockTable.show()

        self.redLineTrainTable = QTableWidget(MainWindow)
        self.redLineTrainTable.setColumnCount(1)
        self.redLineTrainTable.setGeometry(10,320,105,120)
        self.redLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.redLineTrainTable.verticalHeader().hide()
        self.redLineTrainTable.itemClicked.connect(self.redTrainSelectionChanged)
        self.redLineTrainTable.show()

        self.redLineBacklogTable = QTableWidget(MainWindow)
        self.redLineBacklogTable.setColumnCount(1)
        self.redLineBacklogTable.setGeometry(115,320,105,120)
        self.redLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.redLineBacklogTable.verticalHeader().hide()
        self.redLineBacklogTable.show()

    ##################### GREEN LINE ########################
        self.greenLineBlockTable = QTableWidget(MainWindow)
        self.greenLineBlockTable.setRowCount(self.greenLineBlocks.len())
        self.greenLineBlockTable.setColumnCount(3)
        self.greenLineBlockTable.setColumnWidth(0, 40)
        self.greenLineBlockTable.setColumnWidth(2, 41)
        self.greenLineBlockTable.setGeometry(230,20,210,300)
        self.greenLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
        self.greenLineBlockTable.verticalHeader().hide()
        self.greenLineBlockTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.greenLineBlockTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.greenLineBlockTable.itemClicked.connect(self.greenBlockSelectionChanged)
        self.greenLineBlockTable.clicked.connect(self.greenBlockSelectionChanged)
        self.greenLineBlockTable.show()

        self.greenLineTrainTable = QTableWidget(MainWindow)
        self.greenLineTrainTable.setColumnCount(1)
        self.greenLineTrainTable.setGeometry(230,320,105,120)
        self.greenLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.greenLineTrainTable.verticalHeader().hide()
        self.greenLineTrainTable.itemClicked.connect(self.greenTrainSelectionChanged)
        self.greenLineTrainTable.show()

        self.greenLineBacklogTable = QTableWidget(MainWindow)
        self.greenLineBacklogTable.setColumnCount(1)
        self.greenLineBacklogTable.setGeometry(335,320,105,120)
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
        self.destinationTable.setGeometry(10, 460, 200, 100)
        self.destinationTable.setColumnCount(1)
        self.destinationTable.verticalHeader().hide()
        self.destinationTable.horizontalHeader().hide()
        self.destinationTable.show()

        self.dispatchTrainButton = QtWidgets.QPushButton(MainWindow)
        self.dispatchTrainButton.setGeometry(450, 55, 140, 25)
        self.dispatchTrainButton.setText("Dispatch")
        self.dispatchTrainButton.show()
        self.dispatchTrainButton.clicked.connect(self.launchDispatchPopUp)
        self.uploadScheduleButton = QtWidgets.QPushButton(MainWindow)
        self.uploadScheduleButton.setGeometry(620, 100, 130, 30)
        self.uploadScheduleButton.setText("Upload Schedule")
        #self.uploadScheduleButton.clicked.connect(self.uploadSchedule)
        self.uploadScheduleButton.hide()  

        self.populateRedLineTable()
        self.populateGreenLineTable()

        # set up timer refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRedLineTrainTable)
        self.timer.timeout.connect(self.updateGreenLineTrainTable)
        self.timer.timeout.connect(self.showTime)
        self.timer.timeout.connect(self.updateBlockTable)
        self.timer.start(100)

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
                item.setText(self.redLineBlocks.switch(key))
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
                item.setText(self.greenLineBlocks.switch(key))
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
    
    def updateDestinationTable(self):
        index = 0
        self.destinationTable.clear()
        self.destinationTable.setRowCount(len(self.selectedTrainStations))
        for key in self.selectedTrainStations.keys():
            print(key)
            item = QtWidgets.QTableWidgetItem()
            item.setText(key)
            self.destinationTable.setItem(index, 0, item)
            print((self.selectedTrainLine.getDestination(self.selectedTrain, key)))
            self.destinationTable.setItem(index, 1, item)
            index += 1

    def redBlockSelectionChanged(self):
        self.selectedBlock = self.redLineBlockTable.currentRow() + 1
        self.selectedBlockLine = self.redLineBlocks
        self.selectedBlockTable = self.redLineBlockTable

    def redTrainSelectionChanged(self):
        currentRow = self.redLineTrainTable.currentRow()
        self.selectedTrain = self.redLineTrainTable.item(currentRow, 0).text()
        self.selectedTrainLine = self.redLineTrains
        self.selectedTrainStations = self.redLineStations
        self.updateDestinationTable()

    def greenBlockSelectionChanged(self):
        self.selectedBlock = self.greenLineBlockTable.currentRow() + 1
        self.selectedBlockLine = self.greenLineBlocks
        self.selectedBlockTable = self.greenLineBlockTable

    def greenTrainSelectionChanged(self):
        currentRow = self.greenLineTrainTable.currentRow()
        self.selectedTrain = self.greenLineTrainTable.item(currentRow, 0).text()
        self.selectedTrainLine = self.greenLineTrains
        self.selectedTrainStations = self.greenLineStations
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
        item.setText(state)
        self.blockInfoTable.setItem(2,0,item)
        if state == "yes":
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(0,255,0))
        else:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,255))

    def updateFaultState(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getFaultState(str(self.selectedBlock))
        item.setText(state)
        self.blockInfoTable.setItem(3,0,item)
        if state == "yes":
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(0,255,0))
        else:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,255))

    def updateMaintenanceState(self):
        item = QtWidgets.QTableWidgetItem()
        state = self.selectedBlockLine.getMaintenanceState(str(self.selectedBlock))
        item.setText(state)
        self.blockInfoTable.setItem(4,0,item)
        if state == "yes":
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,0))
        else:
            self.selectedBlockTable.item(self.selectedBlock-1,0).setBackground(QtGui.QColor(255,255,255))

    def toggleMaintenance(self):
        self.selectedBlockLine.toggleMaintenanceState(str(self.selectedBlock))


    def launchDispatchPopUp(self):
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = DispatchPopUp()
        self.dispatchPopUp.setupUi(self.dispatchWidget, self.redLineStations, self.greenLineStations, self.redLineTrains, self.greenLineTrains)
        self.dispatchWidget.show()

        self.greenLineBlockTable.resizeColumnToContents(1)

if __name__ == "__main__":
    import sys

    # getting lists of blocks
    layoutFile = "Track_Layout_PGH_Light_Rail.csv"
    trackLayout = LayoutParser(layoutFile)
    redLineBlocks, greenLineBlocks = trackLayout.process()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    mainUi = Ui_MainWindow(redLineBlocks, greenLineBlocks)
    mainUi.setupUi(MainWindow)
    MainWindow.show()
    
    sys.exit(app.exec_())
