from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QAbstractItemView
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from LayoutParser import LayoutParser
from DispatchPopUp import DispatchPopUp
import sys

class Ui_MainWindow(object):

#################################################################
# Start UI generation and setup
#################################################################
    def __init__(self, redLineBlocks, greenLineBlocks):
        self.redLineBlocks = redLineBlocks
        self.greenLineBlocks = greenLineBlocks
        self.redLineBlocksKeys = redLineBlocks.keys()
        self.greenLineBlocksKeys = greenLineBlocks.keys()

        self.redLineStations = dict()
        self.greenLineStations = dict()
        for value in self.redLineBlocks.stations().values():
            self.redLineStations[value] = "No"
        for value in self.greenLineBlocks.stations().values():
            self.greenLineStations[value] = "No"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(10, 10, 800, 613)
        MainWindow.setMouseTracking(True)
        self.redLineMaintenance = False
        self.greenLineMaintenance = False

    ##################### RED LINE ##########################
        self.redLineBlockTable = QTableWidget(MainWindow)
        self.redLineBlockTable.setRowCount(self.redLineBlocks.len())
        self.redLineBlockTable.setColumnCount(3)
        self.redLineBlockTable.setColumnWidth(0, 40)
        self.redLineBlockTable.setColumnWidth(2, 40)
        self.redLineBlockTable.setGeometry(0,20,210,300)
        self.redLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
        self.redLineBlockTable.verticalHeader().hide()
        self.redLineBlockTable.show()

        self.redLineTrainTable = QTableWidget(MainWindow)
        self.redLineTrainTable.setColumnCount(1)
        self.redLineTrainTable.setGeometry(0,320,105,120)
        self.redLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.redLineTrainTable.verticalHeader().hide()
        self.redLineTrainTable.show()

        self.redLineBacklogTable = QTableWidget(MainWindow)
        self.redLineBacklogTable.setColumnCount(1)
        self.redLineBacklogTable.setGeometry(105,320,105,120)
        self.redLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.redLineBacklogTable.verticalHeader().hide()
        self.redLineBacklogTable.show()

    ##################### GREEN LINE ########################
        self.greenLineBlockTable = QTableWidget(MainWindow)
        self.greenLineBlockTable.setRowCount(self.greenLineBlocks.len())
        self.greenLineBlockTable.setColumnCount(3)
        self.greenLineBlockTable.setColumnWidth(0, 40)
        self.greenLineBlockTable.setColumnWidth(2, 40)
        self.greenLineBlockTable.setGeometry(220,20,210,300)
        self.greenLineBlockTable.setHorizontalHeaderLabels(['Block','Switch','Xing'])
        self.greenLineBlockTable.verticalHeader().hide()
        self.greenLineBlockTable.show()

        self.greenLineTrainTable = QTableWidget(MainWindow)
        self.greenLineTrainTable.setColumnCount(1)
        self.greenLineTrainTable.setGeometry(220,320,105,120)
        self.greenLineTrainTable.setHorizontalHeaderLabels(['Active Trains'])
        self.greenLineTrainTable.verticalHeader().hide()
        self.greenLineTrainTable.show()

        self.greenLineBacklogTable = QTableWidget(MainWindow)
        self.greenLineBacklogTable.setColumnCount(1)
        self.greenLineBacklogTable.setGeometry(325,320,105,120)
        self.greenLineBacklogTable.setHorizontalHeaderLabels(['Scheduled'])
        self.greenLineBacklogTable.verticalHeader().hide()
        self.greenLineBacklogTable.show()

    ##################### TRAIN INFO ########################
        font = QtGui.QFont()
        font.setPointSize(13)
        self.trainInfo = QtWidgets.QLabel(MainWindow)
        self.trainInfo.setGeometry(QtCore.QRect(20, 435, 160, 21))
        self.trainInfo.setFont(font)
        self.trainInfo.show()

        self.trainName = QtWidgets.QLabel(MainWindow)
        self.trainName.setGeometry(QtCore.QRect(175, 435, 100, 21))
        self.trainName.setFont(font)
        self.trainName.show()

        self.trainLine = QtWidgets.QLabel(MainWindow)
        self.trainLine.setGeometry(QtCore.QRect(20, 455, 161, 17))
        self.trainLine.show()
        self.commandedSpeed = QtWidgets.QLabel(MainWindow)
        self.commandedSpeed.setGeometry(QtCore.QRect(20, 473, 170, 17))
        self.commandedSpeed.show()
        self.authority = QtWidgets.QLabel(MainWindow)
        self.authority.setGeometry(QtCore.QRect(20, 491, 161, 17))
        self.authority.show()

        self.destinationList = QtWidgets.QListWidget(MainWindow)
        self.destinationList.setGeometry(QtCore.QRect(200, 480, 240, 71))
        self.destinationList.setMouseTracking(True)
        self.destinationList.setSelectionRectVisible(True)
        self.destinationList.setSelectionMode(QAbstractItemView.MultiSelection)
        item = QtWidgets.QListWidgetItem()
        self.destinationList.addItem(item)

        self.setCommandedSpeedValue = QtWidgets.QLineEdit(MainWindow)
        self.setCommandedSpeedValue.setGeometry(QtCore.QRect(20, 510, 31, 21))
        self.setCommandedSpeedValue.show()
        self.setAuthorityValue = QtWidgets.QLineEdit(MainWindow)
        self.setAuthorityValue.setGeometry(QtCore.QRect(20, 530, 31, 21))
        self.setAuthorityValue.show()

        self.setCommandedSpeedButton = QtWidgets.QPushButton(MainWindow)
        self.setCommandedSpeedButton.setGeometry(QtCore.QRect(60, 510, 131, 21))
        #self.setCommandedSpeedButton.clicked.connect(self.setCommandedSpeed)
        self.setAuthorityButton = QtWidgets.QPushButton(MainWindow)
        self.setAuthorityButton.setGeometry(QtCore.QRect(60, 530, 131, 21))
        #self.setAuthorityButton.clicked.connect(self.setAuthority)

        self.toggleDestinationsButton = QtWidgets.QPushButton(MainWindow)
        self.toggleDestinationsButton.setGeometry(QtCore.QRect(200, 555, 150, 31))
        #self.toggleDestinationsButton.clicked.connect(self.toggleDestinations)

        self.destinationsLabel = QtWidgets.QLabel(MainWindow)
        self.destinationsLabel.setGeometry(QtCore.QRect(200, 460, 91, 17))
        self.destinationsLabel.setText("Destinations")

        self.dispatchTrainButton = QtWidgets.QPushButton(MainWindow)
        self.dispatchTrainButton.setGeometry(QtCore.QRect(620, 60, 130, 30))
        self.dispatchTrainButton.setText("Dispatch")
        self.dispatchTrainButton.show()
        self.dispatchTrainButton.clicked.connect(self.launchDispatchPopUp)
        self.uploadScheduleButton = QtWidgets.QPushButton(MainWindow)
        self.uploadScheduleButton.setGeometry(QtCore.QRect(620, 100, 130, 30))
        self.uploadScheduleButton.setText("Upload Schedule")
        #self.uploadScheduleButton.clicked.connect(self.uploadSchedule)
        self.uploadScheduleButton.hide()  

        self.populateRedLineTable()
        self.populateGreenLineTable()

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
            
    def launchDispatchPopUp(self):
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = DispatchPopUp()
        self.dispatchPopUp.setupUi(self.dispatchWidget, self.redLineStations, self.greenLineStations)
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
