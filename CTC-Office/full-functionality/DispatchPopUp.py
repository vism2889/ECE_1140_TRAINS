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
        dispatchPopUp.setGeometry(400, 50, 200, 250)
        self.trainNameEntry = QtWidgets.QLineEdit(dispatchPopUp)
        self.trainNameEntry.setGeometry(QtCore.QRect(20, 10, 100, 21))

        self.redLineStations = redLineStations
        self.greenLineStations = greenLineStations
        self.redLineTrains = redLineTrains
        self.greenLineTrains = greenLineTrains

        self.lineSelection = QtWidgets.QComboBox(dispatchPopUp)
        self.lineSelection.setGeometry(QtCore.QRect(20, 40, 100, 23))
        self.lineSelection.addItem("")
        self.lineSelection.addItem("")

        self.stationTable = QtWidgets.QTableWidget(dispatchPopUp)
        self.stationTable.setGeometry(20,70,150,130)
        self.stationTable.setMouseTracking(True)
        self.stationTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.stationTable.setRowCount(len(self.redLineStations))
        self.stationTable.setColumnCount(2)
        self.stationTable.setColumnWidth(1, 12)
        self.stationTable.horizontalHeader().hide()
        self.stationTable.verticalHeader().hide()

        self.dispatch = QtWidgets.QPushButton(dispatchPopUp)
        self.dispatch.setGeometry(QtCore.QRect(20, 210, 100, 25))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(dispatchPopUp)
        self.lineSelection.activated.connect(self.updateDestinationList)
        self.dispatch.clicked.connect(self.dispatchTrain)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.lineSelection.setItemText(0, _translate("MainWindow", "Red Line"))
        self.lineSelection.setItemText(1, _translate("MainWindow", "Green Line"))
        self.dispatch.setText(_translate("MainWindow", "Dispatch"))
        self.trainNameEntry.clear()

        # set red line destination list 
        self.index = 0
        self.destinationList = self.redLineStations
        for key in self.redLineStations.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate("MainWindow", key))
            self.stationTable.setItem(self.index, 0, item)
            spinBox = QtWidgets.QSpinBox()
            spinBox.setRange(3,5)
            self.stationTable.setCellWidget(self.index, 1, spinBox)
            self.index += 1

    def updateDestinationList(self):
        self.currentLine = self.lineSelection.currentText()
        self.stationTable.clear()

        if (self.currentLine == "Red Line"):
            self.destinationList = self.redLineStations
            self.stationTable.setRowCount(len(self.redLineStations))

            self.index = 0
            for key in self.redLineStations.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                self.stationTable.setItem(self.index, 0, item)
                spinBox = QtWidgets.QSpinBox()
                spinBox.setRange(3,5)
                self.stationTable.setCellWidget(self.index, 1, spinBox)
                self.index += 1

        elif (self.currentLine == "Green Line"):
            self.destinationList = self.greenLineStations
            self.stationTable.setRowCount(len(self.greenLineStations))
            
            self.index = 0
            for key in self.greenLineStations.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                self.stationTable.setItem(self.index, 0, item)
                spinBox = QtWidgets.QSpinBox()
                spinBox.setRange(3,5)
                self.stationTable.setCellWidget(self.index, 1, spinBox)
                self.index += 1

    def dispatchTrain(self):
        self.currentLine = self.lineSelection.currentText()
        self.selectedDestinations = self.stationTable.selectedItems()
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

