import sys
sys.path.append('../train-functionality/')
sys.path.append('../CTC-Office/train-functionality/')
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import QTimer, QTime, Qt

from TrainDictionary import TrainDictionary

class DispatchPopUp(object):

    def __init__(self, signals):
        super().__init__()
        self.signals = signals

    def setupUi(self, dispatchPopUp, redLineStations, greenLineStations, redLineTrains, greenLineTrains):
        dispatchPopUp.setGeometry(450, 50, 150, 200)
        self.trainNameEntry = QtWidgets.QLineEdit(dispatchPopUp)
        self.trainNameEntry.setGeometry(QtCore.QRect(20, 10, 100, 21))
        self.lineSelection = QtWidgets.QComboBox(dispatchPopUp)
        self.lineSelection.setGeometry(QtCore.QRect(20, 40, 100, 23))
        self.lineSelection.addItem("")
        self.lineSelection.addItem("")
        self.stationList = QtWidgets.QListWidget(dispatchPopUp)
        self.stationList.setGeometry(QtCore.QRect(20, 70, 111, 71))
        self.stationList.setMouseTracking(True)
        self.stationList.setSelectionRectVisible(True)
        self.stationList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.dispatch = QtWidgets.QPushButton(dispatchPopUp)
        self.dispatch.setGeometry(QtCore.QRect(20, 150, 100, 31))
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

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(dispatchPopUp)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.lineSelection.setItemText(0, _translate("MainWindow", "Red Line"))
        self.lineSelection.setItemText(1, _translate("MainWindow", "Green Line"))
        __sortingEnabled = self.stationList.isSortingEnabled()
        self.stationList.setSortingEnabled(False)
        self.stationList.setSortingEnabled(__sortingEnabled)
        self.dispatch.setText(_translate("MainWindow", "Dispatch"))
        self.trainNameEntry.clear()

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
                self.redLineTrains.toggleDestination(self.trainName, destination.text(), False)
            elif (self.currentLine == "Green Line"):
                self.greenLineTrains.toggleDestination(self.trainName, destination.text(), False)

        self.signals.dispatchTrainSignal.emit([self.trainName, self.currentLine])

