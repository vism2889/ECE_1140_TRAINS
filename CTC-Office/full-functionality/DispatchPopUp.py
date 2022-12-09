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
        self.currentLine = "Red Line"

    def setupUi(self, dispatchPopUp, redLineStations, greenLineStations, redLineTrains, greenLineTrains, trainCount):
        dispatchPopUp.setGeometry(400, 50, 220, 250)

        self.redLineStations = redLineStations
        self.greenLineStations = greenLineStations
        self.redLineTrains = redLineTrains
        self.greenLineTrains = greenLineTrains
        self.trainCount = trainCount

        font = QtGui.QFont()
        font.setPointSize(14)
        self.clockLabel = QtWidgets.QLabel(dispatchPopUp)
        self.clockLabel.setGeometry(QtCore.QRect(110,31,110,23))
        self.clockLabel.setStyleSheet("background-color: gray; border: 1px solid black")
        self.clockLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clockLabel.setFont(font)

        self.clockSpinBox = QtWidgets.QSpinBox(dispatchPopUp)
        self.clockSpinBox.setGeometry(QtCore.QRect(110,31,110,23))
        self.clockSpinBox.setRange(0,23)
        self.clockSpinBox.hide()

        self.lineSelection = QtWidgets.QComboBox(dispatchPopUp)
        self.lineSelection.setGeometry(QtCore.QRect(0,30,110,25))
        self.lineSelection.addItem("")
        self.lineSelection.addItem("")

        self.timeSelection = QtWidgets.QRadioButton(dispatchPopUp)
        self.timeSelection.setGeometry(5,2,125,25)
        self.timeSelection.setText("Set Dispatch Time")
        self.timeSelection.clicked.connect(self.setTimeSelection)

        self.stationTable = QtWidgets.QTableWidget(dispatchPopUp)
        self.stationTable.setGeometry(0,55,220,170)
        self.stationTable.setMouseTracking(True)
        self.stationTable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.stationTable.setRowCount(len(self.redLineStations))
        self.stationTable.setColumnCount(3)
        self.stationTable.setColumnWidth(1, 58)
        self.stationTable.setColumnWidth(2, 45)
        self.stationTable.setHorizontalHeaderLabels(['Station', 'TTS(min)', 'Arrival'])
        self.stationTable.verticalHeader().hide()

        self.dispatch = QtWidgets.QPushButton(dispatchPopUp)
        self.dispatch.setGeometry(QtCore.QRect(0, 225, 220, 25))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(dispatchPopUp)
        self.lineSelection.activated.connect(self.updateDestinationList)
        self.dispatch.clicked.connect(self.dispatchTrain)
        self.signals.timeSignal.connect(self.showTime)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.lineSelection.setItemText(0, _translate("MainWindow", "Red Line"))
        self.lineSelection.setItemText(1, _translate("MainWindow", "Green Line"))
        self.dispatch.setText(_translate("MainWindow", "Dispatch"))

        # set red line destination list 
        self.index = 0
        self.destinationList = self.redLineStations
        self.trainList = self.redLineTrains
        for key in self.redLineStations.keys():
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate("MainWindow", key))
            self.stationTable.setItem(self.index, 0, item)
            spinBox = QtWidgets.QSpinBox()
            spinBox.setRange(2,5)
            self.stationTable.setCellWidget(self.index, 1, spinBox)
            self.index += 1

    def setTimeSelection(self):
        if self.timeSelection.isChecked():
            self.clockSpinBox.show()
            self.clockLabel.hide()
        else:
            self.clockSpinBox.hide()
            self.clockLabel.show()

    def showTime(self, msg):
        mins = ('%02d' % msg[1])
        hours = ('%02d' % msg[0])
        time = hours + ":" + mins
        self.clockLabel.setText(time)
        if (self.currentLine == "Red Line"):
            self.destinationList = self.redLineStations
            self.stationTable.setRowCount(len(self.redLineStations))

            self.index = 0
            for key in self.redLineStations.keys():
                TTS = self.stationTable.cellWidget(self.index, 1).value()
                hours, mins = self.getArrivalTime(int(hours), int(mins), TTS)
                item = QtWidgets.QTableWidgetItem()
                item.setText(hours + ":" + mins)
                self.stationTable.setItem(self.index, 2, item)
                self.index += 1

        elif (self.currentLine == "Green Line"):
            self.destinationList = self.greenLineStations
            self.stationTable.setRowCount(len(self.greenLineStations))
            
            self.index = 0
            for key in self.greenLineStations.keys():
                TTS = self.stationTable.cellWidget(self.index, 1).value()
                hours, mins = self.getArrivalTime(int(hours), int(mins), TTS)
                item = QtWidgets.QTableWidgetItem()
                item.setText(hours + ":" + mins)
                self.stationTable.setItem(self.index, 2, item)
                self.index += 1

    def getArrivalTime(self, hours, mins, TTS):
        mins = mins + TTS
        if mins > 59:
            mins = mins % 60
            hours += 1
        if hours > 23:
            hours = 0

        mins = ('%02d' % mins)
        hours = ('%02d' % hours)
        return hours, mins

    def updateDestinationList(self):
        self.currentLine = self.lineSelection.currentText()
        self.stationTable.clear()
        self.stationTable.setHorizontalHeaderLabels(['Station', 'TTS', 'Arrival'])

        if (self.currentLine == "Red Line"):
            self.trainList = self.redLineTrains
            self.destinationList = self.redLineStations
            self.stationTable.setRowCount(len(self.redLineStations))

            self.index = 0
            for key in self.redLineStations.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                self.stationTable.setItem(self.index, 0, item)
                spinBox = QtWidgets.QSpinBox()
                spinBox.setRange(2,5)
                self.stationTable.setCellWidget(self.index, 1, spinBox)
                self.index += 1

        elif (self.currentLine == "Green Line"):
            self.trainList = self.greenLineTrains
            self.destinationList = self.greenLineStations
            self.stationTable.setRowCount(len(self.greenLineStations))
            
            self.index = 0
            for key in self.greenLineStations.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                self.stationTable.setItem(self.index, 0, item)
                spinBox = QtWidgets.QSpinBox()
                spinBox.setRange(2,5)
                self.stationTable.setCellWidget(self.index, 1, spinBox)
                self.index += 1
        

    def dispatchTrain(self):
        self.currentLine = self.lineSelection.currentText()
        self.selectedDestinations = self.stationTable.selectedItems()
        self.trainName = "Train " + str(self.trainCount)
        self.totalTTS = 0

        for row in range(0,self.stationTable.rowCount()):
            spinBox = self.stationTable.cellWidget(row, 1)
            TTS = spinBox.value()
            self.totalTTS += int(TTS)

        self.trainList.addTrain(self.trainName, self.destinationList, 0, 0)
        self.trainList.setSuggestedSpeed(self.trainName, self.totalTTS)
        self.suggestedSpeed = self.trainList.getSuggestedSpeed(self.trainName)

        # add dispatch destinations to list
        for destination in self.selectedDestinations:
            self.trainList.toggleDestination(self.trainName, destination.text(), False)

        self.trainList.sendAuthority(self.trainName, self.signals)
        self.signals.dispatchTrainSignal.emit([self.trainName, self.currentLine, self.suggestedSpeed])
        

