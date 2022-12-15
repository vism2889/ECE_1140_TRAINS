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
        dispatchPopUp.setGeometry(400, 50, 220, 275)
        dispatchPopUp.setStyleSheet("background-color: #747c8a;")

        self.redLineStations = redLineStations
        self.greenLineStations = greenLineStations
        self.redLineTrains = redLineTrains
        self.greenLineTrains = greenLineTrains
        self.trainCount = trainCount
        self.scheduledTime = False
        self.currentStationList = self.redLineStations

        font = QtGui.QFont()
        font.setPointSize(14)
        self.clockLabel = QtWidgets.QLabel(dispatchPopUp)
        self.clockLabel.setGeometry(QtCore.QRect(110,31,110,23))
        self.clockLabel.setStyleSheet("background-color: #7b8fb0; border: 1px solid black")
        self.clockLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.clockLabel.setFont(font)

        self.scheduledTimeLabel = QtWidgets.QLabel(dispatchPopUp)
        self.scheduledTimeLabel.setGeometry(QtCore.QRect(110,31,80,23))
        self.scheduledTimeLabel.setStyleSheet("background-color: #7b8fb0; border: 1px solid black")
        self.scheduledTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.scheduledTimeLabel.setFont(font)
        self.scheduledTimeLabel.hide()

        self.hourSpinBox = QtWidgets.QSpinBox(dispatchPopUp)
        self.hourSpinBox.setGeometry(QtCore.QRect(190,31,15,23))
        self.hourSpinBox.setRange(0,23)
        self.hourSpinBox.hide()

        self.minuteSpinBox = QtWidgets.QSpinBox(dispatchPopUp)
        self.minuteSpinBox.setGeometry(QtCore.QRect(205,31,15,23))
        self.minuteSpinBox.setRange(0,60)
        self.minuteSpinBox.hide()

        self.lineSelection = QtWidgets.QComboBox(dispatchPopUp)
        self.lineSelection.setGeometry(QtCore.QRect(0,30,110,25))
        self.lineSelection.addItem("")
        self.lineSelection.addItem("")

        self.timeSelection = QtWidgets.QRadioButton(dispatchPopUp)
        self.timeSelection.setGeometry(5,2,125,25)
        self.timeSelection.setText("Set Dispatch Time")
        self.timeSelection.clicked.connect(self.setTimeSelection)

        self.blockDispatch = QtWidgets.QCheckBox(dispatchPopUp)
        self.blockDispatch.setGeometry(5,225,125,25)
        self.blockDispatch.setText("Dispatch to Block")
        self.blockDispatch.clicked.connect(self.setTimeSelection)

        self.blockDispatchSpinBox = QtWidgets.QSpinBox(dispatchPopUp)
        self.blockDispatchSpinBox.setGeometry(135,225,85,25)
        self.blockDispatchSpinBox.setRange(1,76)

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
        self.dispatch.setGeometry(QtCore.QRect(0, 250, 220, 25))
        self.dispatch.setStyleSheet("background-color: #e8c33c;")

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
            spinBox.setRange(1,5)
            self.stationTable.setCellWidget(self.index, 1, spinBox)
            self.index += 1

    def setTimeSelection(self):
        if self.timeSelection.isChecked():
            self.scheduledTime = True
            self.scheduledTimeLabel.show()
            self.hourSpinBox.show()
            self.minuteSpinBox.show()
            self.clockLabel.hide()
            self.dispatch.setText("Schedule")
        else:
            self.scheduledTime = False
            self.scheduledTimeLabel.hide()
            self.hourSpinBox.hide()
            self.minuteSpinBox.hide()
            self.clockLabel.show()
            self.dispatch.setText("Dispatch")

    def showTime(self, msg):
        # set time values
        if not self.scheduledTime:
            mins = ('%02d' % msg[1])
            hours = ('%02d' % msg[0])
        else:
            self.scheduledMins = self.minuteSpinBox.value()
            self.scheduledHours = self.hourSpinBox.value()
            mins = ('%02d' % self.scheduledMins)
            hours = ('%02d' % self.scheduledHours)
            self.showScheduledTime()
        time = hours + ":" + mins
        self.clockLabel.setText(time)

        # update dispatch/arrival times
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

    def showScheduledTime(self):
        mins = ('%02d' % self.scheduledMins)
        hours = ('%02d' % self.scheduledHours)
        time = hours + ":" + mins
        self.scheduledTime = time
        self.scheduledTimeLabel.setText(time)

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
            self.blockDispatchSpinBox.setRange(1,76)
            self.currentStationList = self.redLineStations

            self.index = 0
            for key in self.redLineStations.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                self.stationTable.setItem(self.index, 0, item)
                spinBox = QtWidgets.QSpinBox()
                spinBox.setRange(1,5)
                self.stationTable.setCellWidget(self.index, 1, spinBox)
                self.index += 1

        elif (self.currentLine == "Green Line"):
            self.trainList = self.greenLineTrains
            self.destinationList = self.greenLineStations
            self.stationTable.setRowCount(len(self.greenLineStations))
            self.blockDispatchSpinBox.setRange(1,150)
            self.currentStationList = self.greenLineStations

            self.index = 0
            for key in self.greenLineStations.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setText(key)
                self.stationTable.setItem(self.index, 0, item)
                spinBox = QtWidgets.QSpinBox()
                spinBox.setRange(1,5)
                self.stationTable.setCellWidget(self.index, 1, spinBox)
                self.index += 1


    def dispatchTrain(self):
        self.currentLine = self.lineSelection.currentText()
        self.selectedDestinations = self.stationTable.selectedItems()
        self.trainName = "Train " + str(self.trainCount)
        self.totalTTS = 0
        block = str(self.blockDispatchSpinBox.value())

        for row in range(0,self.stationTable.rowCount()):
            spinBox = self.stationTable.cellWidget(row, 1)
            TTS = spinBox.value()
            self.totalTTS += int(TTS)

        if self.scheduledTime:
            self.trainList.addScheduledTrain(self.scheduledTime, self.destinationList, 0, 0)
            self.trainList.setSuggestedSpeed(self.scheduledTime, self.totalTTS, self.currentLine, True)

            for destination in self.selectedDestinations:
                if not(':' in destination.text()):
                    self.trainList.toggleDestination(self.scheduledTime, destination.text(), True)

            if self.blockDispatch.isChecked():
                self.trainList.addBlockStop(self.scheduledTime, block, True)
        else:
            self.trainList.addTrain(self.trainName, self.destinationList, 0, 0)
            self.trainList.setSuggestedSpeed(self.trainName, self.totalTTS, self.currentLine, False)
            self.suggestedSpeed = self.trainList.getSuggestedSpeed(self.trainName)

            # add dispatch destinations to list
            for destination in self.selectedDestinations:
                if not(':' in destination.text()):
                    self.trainList.toggleDestination(self.trainName, destination.text(), False)

            if self.blockDispatch.isChecked():
                self.trainList.addBlockStop(self.trainName, block, False)

            self.signals.dispatchTrainSignal.emit([self.trainName, self.currentLine, self.suggestedSpeed])
            self.trainList.sendAuthority(self.trainName, self.signals)


