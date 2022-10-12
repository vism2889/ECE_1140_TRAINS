# -*- coding: utf-8 -*-

import sys

sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/block-functionality/')
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/train-functionality/')
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QDialog
from PyQt5.QtCore import Qt
from lines import redLineBlocks, greenLineBlocks
from trains import redLineTrains, greenLineTrains
from trains import redLineStations, greenLineStations, addRedLineTrain, addGreenLineTrain

class Ui_MainWindow(object):

#################################################################
# Start UI generation and setup
#################################################################

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 613)
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        # create dispatch button
        self.dispatchTrain = QtWidgets.QPushButton(self.centralwidget)
        self.dispatchTrain.setGeometry(QtCore.QRect(620, 50, 131, 31))
        self.dispatchTrain.setObjectName("dispatchTrain")
        self.dispatchTrain.clicked.connect(self.launchDispatchPopUp)

        # create dispatch pop up widget
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = dispatchPopUp()

        # create redLine block list
        self.redLineBlockList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineBlockList.setGeometry(QtCore.QRect(330, 50, 181, 331))
        self.redLineBlockList.setMouseTracking(True)
        self.redLineBlockList.setSelectionRectVisible(True)
        self.redLineBlockList.setObjectName("redLineBlockList")
        self.redLineBlockList.itemActivated.connect(self.redSelectionChanged)

        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.redLineBlockList.addItem(item)

        self.redLineBlockList.setCurrentRow(0)

        # create greenLine block list
        self.greenLineBlockList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineBlockList.setGeometry(QtCore.QRect(90, 50, 181, 331))
        self.greenLineBlockList.setMouseTracking(True)
        self.greenLineBlockList.setSelectionRectVisible(True)
        self.greenLineBlockList.setObjectName("greenLineBlockList")
        self.greenLineBlockList.itemActivated.connect(self.greenSelectionChanged)
        
        self.greenLineBlocksKeys = greenLineBlocks.keys()
        for key in self.greenLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.greenLineBlockList.addItem(item)

        # creating block information chart
        self.blockInfo = QtWidgets.QLabel(self.centralwidget)
        self.blockInfo.setGeometry(QtCore.QRect(350, 435, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.blockInfo.setFont(font)
        self.blockInfo.setObjectName("blockInfo")
        self.blockLine = QtWidgets.QLabel(self.centralwidget)
        self.blockLine.setGeometry(QtCore.QRect(350, 460, 101, 17))
        self.blockLine.setObjectName("blockLine")
        self.occupancy = QtWidgets.QLabel(self.centralwidget)
        self.occupancy.setGeometry(QtCore.QRect(350, 480, 101, 17))
        self.occupancy.setObjectName("occupancy")
        self.faultState = QtWidgets.QLabel(self.centralwidget)
        self.faultState.setGeometry(QtCore.QRect(350, 500, 101, 17))
        self.faultState.setObjectName("faultState")
        self.maintenanceState = QtWidgets.QLabel(self.centralwidget)
        self.maintenanceState.setGeometry(QtCore.QRect(350, 520, 171, 17))
        self.maintenanceState.setObjectName("maintenanceState")
        self.startMaintenance = QtWidgets.QPushButton(self.centralwidget)
        self.startMaintenance.setGeometry(QtCore.QRect(350, 540, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.startMaintenance.setFont(font)
        self.startMaintenance.setObjectName("startMaintenance")

        # create train list
        self.redLineTrainList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineTrainList.setGeometry(QtCore.QRect(620, 200, 131, 101))
        self.redLineTrainList.setMouseTracking(True)
        self.redLineTrainList.setSelectionRectVisible(True)
        self.redLineTrainList.setObjectName("redLineTrainList")
        self.redLineTrainList.itemActivated.connect(self.redLineTrainSelectionChanged)

        # create green line train list
        self.greenLineTrainList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineTrainList.setGeometry(QtCore.QRect(620, 340, 131, 101))
        self.greenLineTrainList.setMouseTracking(True)
        self.greenLineTrainList.setSelectionRectVisible(True)
        self.greenLineTrainList.setObjectName("greenLineTrainList")
        self.greenLineTrainList.itemActivated.connect(self.greenLineTrainSelectionChanged)

        # create train information chart 
        self.trainInfo = QtWidgets.QLabel(self.centralwidget)
        self.trainInfo.setGeometry(QtCore.QRect(20, 435, 160, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.trainInfo.setFont(font)
        self.trainInfo.setObjectName("trainInfo")
        self.trainName = QtWidgets.QLabel(self.centralwidget)
        self.trainName.setGeometry(QtCore.QRect(175, 435, 100, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.trainName.setFont(font)
        self.trainName.setObjectName("trainName")
        self.trainLine = QtWidgets.QLabel(self.centralwidget)
        self.trainLine.setGeometry(QtCore.QRect(20, 455, 161, 17))
        self.trainLine.setObjectName("trainLine")
        self.commandedSpeed = QtWidgets.QLabel(self.centralwidget)
        self.commandedSpeed.setGeometry(QtCore.QRect(20, 473, 170, 17))
        self.commandedSpeed.setObjectName("commandedSpeed")
        self.authority = QtWidgets.QLabel(self.centralwidget)
        self.authority.setGeometry(QtCore.QRect(20, 491, 161, 17))
        self.authority.setObjectName("authority")
        self.destinationList = QtWidgets.QListWidget(self.centralwidget)
        self.destinationList.setGeometry(QtCore.QRect(200, 480, 111, 71))
        self.destinationList.setMouseTracking(True)
        self.destinationList.setSelectionRectVisible(True)
        self.destinationList.setObjectName("destinationList")
        self.destinationList.setSelectionMode(QAbstractItemView.MultiSelection)
        item = QtWidgets.QListWidgetItem()
        self.destinationList.addItem(item)
        self.setCommandedSpeedValue = QtWidgets.QLineEdit(self.centralwidget)
        self.setCommandedSpeedValue.setGeometry(QtCore.QRect(20, 510, 31, 21))
        self.setCommandedSpeedValue.setObjectName("setCommandedSpeedValue")
        self.setAuthorityValue = QtWidgets.QLineEdit(self.centralwidget)
        self.setAuthorityValue.setGeometry(QtCore.QRect(20, 530, 31, 21))
        self.setAuthorityValue.setObjectName("setAuthorityValue")
        self.setCommandedSpeed = QtWidgets.QPushButton(self.centralwidget)
        self.setCommandedSpeed.setGeometry(QtCore.QRect(60, 510, 131, 21))
        self.setCommandedSpeed.setObjectName("setCommandedSpeed")
        self.setAuthority = QtWidgets.QPushButton(self.centralwidget)
        self.setAuthority.setGeometry(QtCore.QRect(60, 530, 131, 21))
        self.setAuthority.setObjectName("setAuthority")
        self.destinations = QtWidgets.QLabel(self.centralwidget)
        self.destinations.setGeometry(QtCore.QRect(200, 460, 91, 17))
        self.destinations.setObjectName("destinations")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # set up timer refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRedLineBlockList)
        self.timer.timeout.connect(self.updateGreenLineBlockList)
        self.timer.timeout.connect(self.updateBlockInfo)
        self.timer.timeout.connect(self.updateRedLineTrainList)
        self.timer.timeout.connect(self.updateGreenLineTrainList)
        self.timer.start(1000)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.redLineBlockList.isSortingEnabled()
        self.redLineBlockList.setSortingEnabled(False)
        self.greenLineBlockList.setSortingEnabled(False)
        self.dispatchTrain.setText(_translate("MainWindow", "Dispatch Train"))

        # set red line block names
        for key in self.redLineBlocksKeys:
            item = self.redLineBlockList.item(redLineBlocks[key].number-1)
            item.setText(_translate("MainWindow", key))

        # set green line block names
        for key in self.greenLineBlocksKeys:
            item = self.greenLineBlockList.item(greenLineBlocks[key].number-1)
            item.setText(_translate("MainWindow", key))

        # set block info text
        self.redLineBlockList.setSortingEnabled(__sortingEnabled)
        self.greenLineBlockList.setSortingEnabled(__sortingEnabled)
        self.blockLine.setText(_translate("MainWindow", "Line: Red"))
        self.blockInfo.setText(_translate("MainWindow", "Block Information: Block 1"))
        self.occupancy.setText(_translate("MainWindow", "Occupied: no"))
        self.faultState.setText(_translate("MainWindow", "Track Fault: no"))
        self.maintenanceState.setText(_translate("MainWindow", "Under Maintenance: no"))
        self.startMaintenance.setText(_translate("MainWindow", "Start Maintenance"))

        # set train info test
        self.trainInfo.setText(_translate("MainWindow", "Train Information: "))
        self.trainName.setText(_translate("MainWindow", "N/A"))
        self.trainLine.setText(_translate("MainWindow", "Line: N/A"))
        self.commandedSpeed.setText(_translate("MainWindow", "Comm. Speed (mph): N/A"))
        self.authority.setText(_translate("MainWindow", "Authority (mi): N/A"))
        self.setCommandedSpeed.setText(_translate("MainWindow", "Command Speed"))
        self.setAuthority.setText(_translate("MainWindow", "Set Authority"))
        self.destinations.setText(_translate("MainWindow", "Destinations"))
        __sortingEnabled = self.destinationList.isSortingEnabled()
        self.destinationList.setSortingEnabled(False)
        item = self.destinationList.item(0)
        item.setText(_translate("MainWindow", "N/A"))
        self.destinationList.setSortingEnabled(__sortingEnabled)

#################################################################
# End UI generation, start functions
#################################################################

# block methods
    def redSelectionChanged(self):
        # update block information
        selectedBlock = self.redLineBlockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        self.occupancy.setText("Occupied: " + redLineBlocks[selectedBlock].getOccupancy())
        self.faultState.setText("Track Fault: " + redLineBlocks[selectedBlock].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + redLineBlocks[selectedBlock].getMaintenanceState())
        self.blockLine.setText("Line: Red")

    def greenSelectionChanged(self):
        # update block information
        selectedBlock = self.greenLineBlockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        self.occupancy.setText("Occupied: " + greenLineBlocks[selectedBlock].getOccupancy())
        self.faultState.setText("Track Fault: " + greenLineBlocks[selectedBlock].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + greenLineBlocks[selectedBlock].getMaintenanceState())
        self.blockLine.setText("Line: Green")

    def updateRedLineBlockList(self):
        for i in range(0, len(redLineBlocks)):
            item = self.redLineBlockList.item(i)
            selectedBlock = item.text()

            if (redLineBlocks[selectedBlock].getMaintenanceState() == "yes"):
                item.setBackground(Qt.yellow)
            elif (redLineBlocks[selectedBlock].getFaultState() == "yes"):
                item.setBackground(Qt.red)
            elif (redLineBlocks[selectedBlock].getOccupancy() == "yes"):
                item.setBackground(Qt.green)
            else:
                item.setBackground(Qt.white)

    def updateGreenLineBlockList(self):
        for i in range(0, len(greenLineBlocks)):
            item = self.greenLineBlockList.item(i)
            selectedBlock = item.text()

            if (greenLineBlocks[selectedBlock].getMaintenanceState() == "yes"):
                item.setBackground(Qt.yellow)
            elif (greenLineBlocks[selectedBlock].getFaultState() == "yes"):
                item.setBackground(Qt.red)
            elif (greenLineBlocks[selectedBlock].getOccupancy() == "yes"):
                item.setBackground(Qt.green)
            else:
                item.setBackground(Qt.white)

    def updateBlockInfo(self):
        blockLineText = self.blockLine.text()
        if (blockLineText == "Line: Red"):
            self.redSelectionChanged()
        elif (blockLineText == "Line: Green"):
            self.greenSelectionChanged()

# train methods
    def launchDispatchPopUp(self):
        self.dispatchPopUp.setupUi(self.dispatchWidget)
        self.dispatchWidget.show()

    def updateRedLineTrainList(self):
        self.redLineTrainsKeys = redLineTrains.keys()
        self.currentredLineTrainList = dict()

        # checking for removed trains
        for i in range(self.redLineTrainList.count()):
            self.currentredLineTrainList[self.redLineTrainList.item(i).text()] = None

            if ((self.redLineTrainList.item(i).text() in redLineTrains) == False):
                self.redLineTrainList.takeItem(i)
            
        # checking for new trains
        for key in self.redLineTrainsKeys:
            if ((key in self.currentredLineTrainList) == False):
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.redLineTrainList.addItem(item)
    
    def updateGreenLineTrainList(self):
        self.greenLineTrainsKeys = greenLineTrains.keys()
        self.currentgreenLineTrainList = dict()

        # checking for removed trains
        for i in range(self.greenLineTrainList.count()):
            self.currentgreenLineTrainList[self.greenLineTrainList.item(i).text()] = None

            if ((self.greenLineTrainList.item(i).text() in greenLineTrains) == False):
                self.greenLineTrainList.takeItem(i)
            
        # checking for new trains
        for key in self.greenLineTrainsKeys:
            if ((key in self.currentgreenLineTrainList) == False):
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.greenLineTrainList.addItem(item)


    def redLineTrainSelectionChanged(self):
        self.selectedTrain = self.redLineTrainList.currentItem().text()
        self.trainLine.setText("Line: Red")
        self.trainName.setText(self.selectedTrain)
        self.commandedSpeed.setText("Comm. Speed (mph): " + redLineTrains[self.selectedTrain].getCommandedSpeed())
        self.authority.setText("Authority (mi): " + redLineTrains[self.selectedTrain].getAuthority())
        
        self.destinationList.clear()
        self.currentTrainDestinations = redLineTrains[self.selectedTrain].getDestinations()
        for key in self.currentTrainDestinations.keys():
            item = QtWidgets.QListWidgetItem()
            item.setText(key + ": " + self.currentTrainDestinations[key])
            self.destinationList.addItem(item)

    def greenLineTrainSelectionChanged(self):
        self.selectedTrain = self.greenLineTrainList.currentItem().text()
        self.trainLine.setText("Line: Green")
        self.trainName.setText(self.selectedTrain)
        self.commandedSpeed.setText("Comm. Speed (mph): " + greenLineTrains[self.selectedTrain].getCommandedSpeed())
        self.authority.setText("Authority (mi): " + greenLineTrains[self.selectedTrain].getAuthority())
        
        self.destinationList.clear()
        self.currentTrainDestinations = greenLineTrains[self.selectedTrain].getDestinations()
        for key in self.currentTrainDestinations.keys():
            item = QtWidgets.QListWidgetItem()
            item.setText(key + ": " + self.currentTrainDestinations[key])
            self.destinationList.addItem(item)

    

class Ui_testWindow(object):

#################################################################
# Start UI generation and setup
#################################################################
    
    def setupUi(self, testWindow):
        testWindow.setObjectName("testWindow")
        testWindow.resize(400, 300)
        self.toggleOccupancyButton = QtWidgets.QPushButton(testWindow)
        self.toggleOccupancyButton.setGeometry(QtCore.QRect(50, 170, 131, 21))
        self.toggleOccupancyButton.setObjectName("toggleOccupancyButton")
        self.toggleOccupancyButton.clicked.connect(self.toggleOccupancy)
        self.toggleFaultStateButton = QtWidgets.QPushButton(testWindow)
        self.toggleFaultStateButton.setGeometry(QtCore.QRect(50, 210, 131, 21))
        self.toggleFaultStateButton.setObjectName("toggleFaultStateButton")
        self.toggleFaultStateButton.clicked.connect(self.toggleFaultState)
        self.toggleMaintenanceStateButton = QtWidgets.QPushButton(testWindow)
        self.toggleMaintenanceStateButton.setGeometry(QtCore.QRect(50, 250, 131, 21))
        self.toggleMaintenanceStateButton.setObjectName("toggleMaintenanceStateButton")
        self.toggleMaintenanceStateButton.clicked.connect(self.toggleMaintenanceState)
        self.redLineBlockList = QtWidgets.QListWidget(testWindow)
        self.redLineBlockList.setGeometry(QtCore.QRect(220, 120, 131, 111))
        self.redLineBlockList.setMouseTracking(True)
        self.redLineBlockList.setSelectionRectVisible(True)
        self.redLineBlockList.setObjectName("redLineBlockList")

        # create redLine block list
        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.redLineBlockList.addItem(item)

        self.retranslateUi(testWindow)
        QtCore.QMetaObject.connectSlotsByName(testWindow)

    def retranslateUi(self, testWindow):
        _translate = QtCore.QCoreApplication.translate
        testWindow.setWindowTitle(_translate("testWindow", "Form"))
        self.toggleOccupancyButton.setText(_translate("testWindow", "Toggle Occupancy"))
        self.toggleFaultStateButton.setText(_translate("testWindow", "Toggle Fault State"))
        self.toggleMaintenanceStateButton.setText(_translate("testWindow", "Toggle Maintenance"))
        __sortingEnabled = self.redLineBlockList.isSortingEnabled()
        self.redLineBlockList.setSortingEnabled(False)

        # set red line block names
        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = self.redLineBlockList.item(redLineBlocks[key].number-1)
            item.setText(_translate("testWindow", key))

        self.redLineBlockList.setSortingEnabled(__sortingEnabled)

#################################################################
# End UI generation, start functions
#################################################################

    def toggleFaultState(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        redLineBlocks[selectedBlock].toggleFaultState()

    def toggleOccupancy(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        redLineBlocks[selectedBlock].toggleOccupancy()

    def toggleMaintenanceState(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        redLineBlocks[selectedBlock].toggleMaintenanceState()

class dispatchPopUp(object):
    def setupUi(self, dispatchPopUp):
        dispatchPopUp.setObjectName("dispatchPopUp")
        dispatchPopUp.resize(200, 300)
        self.trainNameEntry = QtWidgets.QLineEdit(dispatchPopUp)
        self.trainNameEntry.setGeometry(QtCore.QRect(40, 10, 100, 21))
        self.trainNameEntry.setObjectName("trainName")
        self.lineSelection = QtWidgets.QComboBox(dispatchPopUp)
        self.lineSelection.setGeometry(QtCore.QRect(40, 40, 100, 23))
        self.lineSelection.setObjectName("comboBox")
        self.lineSelection.addItem("")
        self.lineSelection.addItem("")
        self.stationList = QtWidgets.QListWidget(dispatchPopUp)
        self.stationList.setGeometry(QtCore.QRect(40, 70, 111, 71))
        self.stationList.setMouseTracking(True)
        self.stationList.setSelectionRectVisible(True)
        self.stationList.setObjectName("destinationList")
        self.stationList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.dispatch = QtWidgets.QPushButton(dispatchPopUp)
        self.dispatch.setGeometry(QtCore.QRect(40, 150, 100, 31))
        self.dispatch.setObjectName("dispatchTrain")
        self.redLineStationsKeys = redLineStations.keys()
        self.greenLineStationsKeys = greenLineStations.keys()
        self.lineSelection.activated.connect(self.updateDestinationList)
        self.dispatch.clicked.connect(self.dispatchTrain)

        # add items to destinationList
        for key in self.redLineStationsKeys:
            item = QtWidgets.QListWidgetItem()
            self.stationList.addItem(item)

        self.retranslateUi(dispatchPopUp)
        QtCore.QMetaObject.connectSlotsByName(dispatchPopUp)

    def retranslateUi(self, dispatchPopUp):
        _translate = QtCore.QCoreApplication.translate
        self.lineSelection.setItemText(0, _translate("MainWindow", "Red Line"))
        self.lineSelection.setItemText(1, _translate("MainWindow", "Green Line"))
        __sortingEnabled = self.stationList.isSortingEnabled()
        self.stationList.setSortingEnabled(False)
        self.stationList.setSortingEnabled(__sortingEnabled)
        self.dispatch.setText(_translate("MainWindow", "Dispatch"))

        # set red line destination list 
        self.index = 0
        for key in self.redLineStationsKeys:
            item = self.stationList.item(self.index)
            item.setText(_translate("MainWindow", key))
            self.index += 1

    def updateDestinationList(self):
        self.currentLine = self.lineSelection.currentText()

        if (self.currentLine == "Red Line"):
            self.index = 0
            for key in self.redLineStationsKeys:
                item = self.stationList.item(self.index)
                item.setText(key)
                self.index += 1
        elif (self.currentLine == "Green Line"):
            self.index = 0
            for key in self.greenLineStationsKeys:
                item = self.stationList.item(self.index)
                item.setText(key)
                self.index += 1

    def dispatchTrain(self):
        self.currentLine = self.lineSelection.currentText()
        self.destinationList = []
        self.selectedDestinations = self.stationList.selectedItems()
        self.trainName = self.trainNameEntry.text()

        # add dispatch destinations to list
        for destination in self.selectedDestinations:
            self.destinationList.append(destination.text())

        if (self.currentLine == "Red Line"):
            addRedLineTrain(self.destinationList, self.trainName)
        elif (self.currentLine == "Green Line"):
            addGreenLineTrain(self.destinationList, self.trainName)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    testWindow = QtWidgets.QWidget()
    ui = Ui_testWindow()
    ui.setupUi(testWindow)
    mainUi = Ui_MainWindow()
    mainUi.setupUi(MainWindow)
    MainWindow.show()
    testWindow.show()
    
    sys.exit(app.exec_())
