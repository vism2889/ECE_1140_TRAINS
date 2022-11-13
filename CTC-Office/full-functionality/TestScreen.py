import sys
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/block-functionality/')
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/train-functionality/')
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/schedule-functionality/')
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import QTimer, QTime, Qt
from lines import *
from trains import *
from scheduleParser import readSchedule

class Ui_testWindow(object):

#################################################################
# Start UI generation and setup
#################################################################
    
    def setupUi(self, testWindow):
        testWindow.setObjectName("testWindow")
        testWindow.setGeometry(900, 10, 400, 430)
        self.toggleOccupancyButton = QtWidgets.QPushButton(testWindow)
        self.toggleOccupancyButton.setGeometry(QtCore.QRect(220, 280, 150, 20))
        self.toggleOccupancyButton.setObjectName("toggleOccupancyButton")
        self.toggleOccupancyButton.clicked.connect(self.toggleOccupancy)
        self.toggleFaultStateButton = QtWidgets.QPushButton(testWindow)
        self.toggleFaultStateButton.setGeometry(QtCore.QRect(220, 310, 150, 20))
        self.toggleFaultStateButton.setObjectName("toggleFaultStateButton")
        self.toggleFaultStateButton.clicked.connect(self.toggleFaultState)
        self.toggleMaintenanceStateButton = QtWidgets.QPushButton(testWindow)
        self.toggleMaintenanceStateButton.setGeometry(QtCore.QRect(220, 340, 150, 20))
        self.toggleMaintenanceStateButton.setObjectName("toggleMaintenanceStateButton")
        self.toggleMaintenanceStateButton.clicked.connect(self.toggleMaintenanceState)
        self.toggleRedCrossingButton = QtWidgets.QPushButton(testWindow)
        self.toggleRedCrossingButton.setGeometry(QtCore.QRect(220, 370, 150, 20))
        self.toggleRedCrossingButton.setObjectName("toggleRedCrossingButton")
        self.toggleRedCrossingButton.clicked.connect(self.toggleRedCrossing)
        self.toggleGreenCrossingButton = QtWidgets.QPushButton(testWindow)
        self.toggleGreenCrossingButton.setGeometry(QtCore.QRect(220, 390, 150, 20))
        self.toggleGreenCrossingButton.setObjectName("toggleGreenCrossingButton")
        self.toggleGreenCrossingButton.clicked.connect(self.toggleGreenCrossing)
        self.passengerSpinBox = QtWidgets.QSpinBox(testWindow)
        self.passengerSpinBox.setGeometry(10, 380, 60, 20)
        self.passengerSpinBox.setObjectName("passengerSpinBox")
        self.changeTotalPassengersLabel = QtWidgets.QLabel(testWindow)
        self.changeTotalPassengersLabel.setGeometry(QtCore.QRect(10, 360, 100, 20))
        self.changeTotalPassengersLabel.setObjectName("changeTotalPassengersLabel")
        self.changeTotalPassengersButton = QtWidgets.QPushButton(testWindow)
        self.changeTotalPassengersButton.setGeometry(70, 380, 70, 20)
        self.changeTotalPassengersButton.setObjectName("changeTotalPassengersButton")
        self.changeTotalPassengersButton.clicked.connect(self.changeTotalPassengers)

        # create train list
        self.redLineTrainList = QtWidgets.QListWidget(testWindow)
        self.redLineTrainList.setGeometry(QtCore.QRect(40, 20, 130, 100))
        self.redLineTrainList.setMouseTracking(True)
        self.redLineTrainList.setSelectionRectVisible(True)
        self.redLineTrainList.setObjectName("redLineTrainList")
        self.redLineRemoveTrainButton = QtWidgets.QPushButton(testWindow)
        self.redLineRemoveTrainButton.setGeometry(QtCore.QRect(40, 120, 130, 20))
        self.redLineRemoveTrainButton.setObjectName("redLineRemoveTrainButton")
        self.redLineRemoveTrainButton.clicked.connect(self.removeRedLineTrain)

        # red line block list
        self.redLineBlockListLabel = QtWidgets.QLabel(testWindow)
        self.redLineBlockListLabel.setGeometry(QtCore.QRect(220, 0, 100, 20))
        self.redLineBlockListLabel.setObjectName("redLineBlockListLabel")
        self.redLineBlockList = QtWidgets.QListWidget(testWindow)
        self.redLineBlockList.setGeometry(QtCore.QRect(220, 20, 130, 110))
        self.redLineBlockList.setMouseTracking(True)
        self.redLineBlockList.setSelectionRectVisible(True)
        self.redLineBlockList.setObjectName("redLineBlockList")
        self.redLineBlockList.itemActivated.connect(self.updateCurrentBlockLineRed)

        # create green line train list
        self.greenLineTrainLabel = QtWidgets.QLabel(testWindow)
        self.greenLineTrainList = QtWidgets.QListWidget(testWindow)
        self.greenLineTrainList.setGeometry(QtCore.QRect(40, 150, 130, 100))
        self.greenLineTrainList.setMouseTracking(False)
        self.greenLineTrainList.setSelectionRectVisible(False)
        self.greenLineTrainList.setObjectName("greenLineTrainList")
        self.greenLineRemoveTrainButton = QtWidgets.QPushButton(testWindow)
        self.greenLineRemoveTrainButton.setGeometry(QtCore.QRect(40, 250, 130, 20))
        self.greenLineRemoveTrainButton.setObjectName("greenLineRemoveTrainButton")
        self.greenLineRemoveTrainButton.clicked.connect(self.removeGreenLineTrain)
    
        # green line block list
        self.greenLineBlockListLabel = QtWidgets.QLabel(testWindow)
        self.greenLineBlockListLabel.setGeometry(QtCore.QRect(220, 130, 100, 20))
        self.greenLineBlockListLabel.setObjectName("greenLineBlockListLabel")
        self.greenLineBlockList = QtWidgets.QListWidget(testWindow)
        self.greenLineBlockList.setGeometry(QtCore.QRect(220, 150, 130, 110))
        self.greenLineBlockList.setMouseTracking(True)
        self.greenLineBlockList.setSelectionRectVisible(True)
        self.greenLineBlockList.setObjectName("greenLineBlockList")
        self.greenLineBlockList.itemActivated.connect(self.updateCurrentBlockLineGreen)

        # create redLine block list
        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.redLineBlockList.addItem(item)

        # create greenLine block list
        self.greenLineBlocksKeys = greenLineBlocks.keys()
        for key in self.greenLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.greenLineBlockList.addItem(item)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRedLineTrainList)
        self.timer.timeout.connect(self.updateGreenLineTrainList)
        self.timer.start(10)

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
        self.changeTotalPassengersButton.setText(_translate("testWindow", "update"))
        self.redLineRemoveTrainButton.setText(_translate("testWindow", "Remove Train"))
        self.greenLineRemoveTrainButton.setText(_translate("testWindow", "Remove Train"))
        self.changeTotalPassengersLabel.setText(_translate("testWindow", "Total Passengers"))

        # set red line block names
        self.toggleRedCrossingButton.setText(_translate("testWindow", "Red Line X-ing"))
        self.redLineBlockListLabel.setText(_translate("testWindow", "Red Line:"))
        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = self.redLineBlockList.item(redLineBlocks[key].number-1)
            item.setText(_translate("testWindow", key))

        self.redLineBlockList.setSortingEnabled(__sortingEnabled)

        # set green line block names
        self.toggleGreenCrossingButton.setText(_translate("testWindow", "Green Line X-ing"))
        self.greenLineBlockListLabel.setText(_translate("testWindow", "Green Line:"))
        self.greenLineBlocksKeys = greenLineBlocks.keys()
        for key in self.greenLineBlocksKeys:
            item = self.greenLineBlockList.item(greenLineBlocks[key].number-1)
            item.setText(_translate("testWindow", key))

        self.greenLineBlockList.setSortingEnabled(__sortingEnabled)

#################################################################
# End UI generation, start functions
#################################################################

    def updateCurrentBlockLineRed(self):
        self.currentBlockLine = "red"

    def updateCurrentBlockLineGreen(self):
        self.currentBlockLine = "green"

    def toggleFaultState(self):
        if self.currentBlockLine == "red":
            selectedBlock = self.redLineBlockList.currentItem().text()
            redLineBlocks[selectedBlock].toggleFaultState()
        elif self.currentBlockLine == "green":
            selectedBlock = self.greenLineBlockList.currentItem().text()
            greenLineBlocks[selectedBlock].toggleFaultState()

    def toggleOccupancy(self):
        if self.currentBlockLine == "red":
            selectedBlock = self.redLineBlockList.currentItem().text()
            redLineBlocks[selectedBlock].toggleOccupancy()
        elif self.currentBlockLine == "green":
            selectedBlock = self.greenLineBlockList.currentItem().text()
            greenLineBlocks[selectedBlock].toggleOccupancy()

    def toggleMaintenanceState(self):
        if self.currentBlockLine == "red":
            selectedBlock = self.redLineBlockList.currentItem().text()
            redLineBlocks[selectedBlock].toggleMaintenanceState()
        elif self.currentBlockLine == "green":
            selectedBlock = self.greenLineBlockList.currentItem().text()
            greenLineBlocks[selectedBlock].toggleMaintenanceState()

    def toggleRedCrossing(self):
        for key in redLineCrossing.keys():
            if redLineCrossing[key] == "Red":
                redLineCrossing.update({key: "Yellow"})
            elif redLineCrossing[key] == "Yellow":
                redLineCrossing.update({key: "Green"})
            else:
                redLineCrossing.update({key: "Red"})

    def toggleGreenCrossing(self):
        for key in greenLineCrossing.keys():
            if greenLineCrossing[key] == "Red":
                greenLineCrossing.update({key: "Yellow"})
            elif greenLineCrossing[key] == "Yellow":
                greenLineCrossing.update({key: "Green"})
            else:
                greenLineCrossing.update({key: "Red"})

    def changeTotalPassengers(self):
        totalPassengers.update({"totalPassengers": self.passengerSpinBox.text()})


    def updateRedLineTrainList(self):
        self.redLineTrainsKeys = redLineTrains.keys()
        self.currentRedLineTrainList = dict()

        # checking for removed trains
        for i in range(self.redLineTrainList.count()):
            self.currentRedLineTrainList[self.redLineTrainList.item(i).text()] = None

            if ((self.redLineTrainList.item(i).text() in redLineTrains) == False):
                self.redLineTrainList.takeItem(i)
            
        # checking for new trains
        for key in self.redLineTrainsKeys:
            if ((key in self.currentRedLineTrainList) == False):
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.redLineTrainList.addItem(item)

    def updateGreenLineTrainList(self):
        self.greenLineTrainsKeys = greenLineTrains.keys()
        self.currentGreenLineTrainList = dict()

        # checking for removed trains
        for i in range(self.greenLineTrainList.count()):
            self.currentGreenLineTrainList[self.greenLineTrainList.item(i).text()] = None

            if ((self.greenLineTrainList.item(i).text() in greenLineTrains) == False):
                self.greenLineTrainList.takeItem(i)
            
        # checking for new trains
        for key in self.greenLineTrainsKeys:
            if ((key in self.currentGreenLineTrainList) == False):
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.greenLineTrainList.addItem(item)

    def removeRedLineTrain(self):
        self.currentTrain = self.redLineTrainList.currentItem().text()
        redLineTrains.pop(self.currentTrain)

    def removeGreenLineTrain(self):
        self.currentTrain = self.greenLineTrainList.currentItem().text()
        greenLineTrains.pop(self.currentTrain)

class dispatchPopUp(object):
    def setupUi(self, dispatchPopUp):
        dispatchPopUp.setObjectName("dispatchPopUp")
        dispatchPopUp.setGeometry(602, 50, 200, 300)
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
        self.stationList.clear()

        if (self.currentLine == "Red Line"):
            for key in self.redLineStationsKeys:
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.stationList.addItem(item)
        elif (self.currentLine == "Green Line"):
            for key in self.greenLineStationsKeys:
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.stationList.addItem(item)

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