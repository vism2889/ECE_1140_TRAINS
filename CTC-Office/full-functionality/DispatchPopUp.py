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
