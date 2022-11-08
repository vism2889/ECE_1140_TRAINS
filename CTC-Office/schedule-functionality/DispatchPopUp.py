import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import QTimer, QTime, Qt

from TrainDictionary import TrainDictionary
from scheduleParser import readSchedule

class DispatchPopUp(object):
    def setupUi(self, dispatchPopUp, redLineStations, greenLineStations, redLineTrains, greenLineTrains):
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
        self.redLineStations = redLineStations
        self.greenLineStations = greenLineStations
        self.lineSelection.activated.connect(self.updateDestinationList)
        self.dispatch.clicked.connect(self.dispatchTrain)
        self.redLineTrains = redLineTrains
        self.greenLineTrains = greenLineTrains


        # add items to destinationList
        for key in self.redLineStations.keys():
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
        self.destinationList = self.redLineStations
        for key in self.redLineStations.keys():
            item = self.stationList.item(self.index)
            item.setText(_translate("MainWindow", key))
            self.index += 1

    def updateDestinationList(self):
        self.currentLine = self.lineSelection.currentText()
        self.stationList.clear()

        if (self.currentLine == "Red Line"):
            self.destinationList = self.redLineStations
            for key in self.redLineStations.keys():
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.stationList.addItem(item)
        elif (self.currentLine == "Green Line"):
            self.destinationList = self.greenLineStations
            for key in self.greenLineStations.keys():
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.stationList.addItem(item)

    def dispatchTrain(self):
        self.currentLine = self.lineSelection.currentText()
        self.selectedDestinations = self.stationList.selectedItems()
        self.trainName = self.trainNameEntry.text()

        if (self.currentLine == "Red Line"):
            self.redLineTrains.addTrain(self.trainName, self.destinationList, 0, 0)
        elif (self.currentLine == "Green Line"):
            self.greenLineTrains.addTrain(self.trainName, self.destinationList, 0, 0)

        # add dispatch destinations to list
        for destination in self.selectedDestinations:
            if (self.currentLine == "Red Line"):
                self.redLineTrains.toggleDestination(self.trainName, destination.text())
            elif (self.currentLine == "Green Line"):
                self.greenLineTrains.toggleDestination(self.trainName, destination.text())
