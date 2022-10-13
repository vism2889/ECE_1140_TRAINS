# -*- coding: utf-8 -*-

import sys

sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/block-functionality/')
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/train-functionality/')
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/schedule-functionality/')
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import QTimer, QTime, Qt
from lines import *
from trains import *
from lines import redLineBlocks, greenLineBlocks, redLineSwitches, toggleRedLineSwitch, greenLineSwitches, toggleGreenLineSwitch
from trains import redLineTrains, greenLineTrains, redLineBacklog, greenLineBacklog
from trains import redLineStations, greenLineStations, addRedLineTrain, addGreenLineTrain
from scheduleParser import readSchedule

class Ui_MainWindow(object):

#################################################################
# Start UI generation and setup
#################################################################

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(10, 10, 800, 613)
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        # throughput label
        self.throughputLabel = QtWidgets.QLabel(self.centralwidget)
        self.throughputLabel.setGeometry(QtCore.QRect(620, 10, 101, 20))
        self.throughputLabel.setObjectName("throughputLabel")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.throughputLabel.setFont(font)

        self.clockLabel = QtWidgets.QLabel(self.centralwidget)
        self.clockLabel.setGeometry(QtCore.QRect(360, 5, 80, 20))
        self.clockLabel.setObjectName("clockLabel")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clockLabel.setStyleSheet("background-color: gray; border: 1px solid black")
        self.clockLabel.setFont(font)

        # create dispatch buttons
        self.dispatchTrain = QtWidgets.QPushButton(self.centralwidget)
        self.dispatchTrain.setGeometry(QtCore.QRect(620, 60, 130, 30))
        self.dispatchTrain.setObjectName("dispatchTrain")
        self.dispatchTrain.clicked.connect(self.launchDispatchPopUp)
        self.uploadScheduleButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadScheduleButton.setGeometry(QtCore.QRect(620, 100, 130, 30))
        self.uploadScheduleButton.setObjectName("uploadScheduleButton")
        self.uploadScheduleButton.clicked.connect(self.uploadSchedule)

        # create dispatch pop up widget
        self.dispatchWidget = QtWidgets.QWidget()
        self.dispatchPopUp = dispatchPopUp()

        # create redLine block list
        self.redLineBlockListLabel = QtWidgets.QLabel(self.centralwidget)
        self.redLineBlockListLabel.setGeometry(QtCore.QRect(330, 40, 100, 17))
        self.redLineBlockListLabel.setObjectName("redLineBlockListLabel")
        self.redLineBlockList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineBlockList.setGeometry(QtCore.QRect(330, 60, 100, 331))
        self.redLineBlockList.setMouseTracking(True)
        self.redLineBlockList.setSelectionRectVisible(True)
        self.redLineBlockList.setObjectName("redLineBlockList")
        self.redLineBlockList.itemActivated.connect(self.redSelectionChanged)

        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.redLineBlockList.addItem(item)

        self.redLineBlockList.setCurrentRow(0)

        # create redLine switch list
        self.redLineSwitchListLabel = QtWidgets.QLabel(self.centralwidget)
        self.redLineSwitchListLabel.setGeometry(QtCore.QRect(440, 60, 100, 20))
        self.redLineSwitchListLabel.setObjectName("redLineSwitchListLabel")
        self.redLineSwitchList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineSwitchList.setGeometry(QtCore.QRect(440, 80, 150, 100))
        self.redLineSwitchList.setMouseTracking(True)
        self.redLineSwitchList.setSelectionRectVisible(True)
        self.redLineSwitchList.setObjectName("redLineSwitchList")
        self.redLineSwitchList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.toggleRedLineSwitchButton = QtWidgets.QPushButton(self.centralwidget)
        self.toggleRedLineSwitchButton.setGeometry(QtCore.QRect(440, 185, 100, 20))
        self.toggleRedLineSwitchButton.hide()
        self.toggleRedLineSwitchButton.clicked.connect(self.toggleRedLineSwitchState)

        self.redLineSwitchKeys = redLineSwitches.keys()
        for key in self.redLineSwitchKeys:
            item = QtWidgets.QListWidgetItem()
            item.setText(key + ": " + redLineSwitches[key])
            self.redLineSwitchList.addItem(item)

        # create train list
        self.redLineTrainLabel = QtWidgets.QLabel(self.centralwidget)
        self.redLineTrainLabel.setGeometry(QtCore.QRect(440, 200, 100, 20))
        self.redLineTrainLabel.setObjectName("redLineTrainLabel")
        self.redLineTrainList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineTrainList.setGeometry(QtCore.QRect(440, 220, 130, 100))
        self.redLineTrainList.setMouseTracking(True)
        self.redLineTrainList.setSelectionRectVisible(True)
        self.redLineTrainList.setObjectName("redLineTrainList")
        self.redLineTrainList.itemActivated.connect(self.redLineTrainSelectionChanged)

        # create red line back log
        self.redLineBacklogLabel = QtWidgets.QLabel(self.centralwidget)
        self.redLineBacklogLabel.setGeometry(620, 140, 130, 20)
        self.redLineBacklogLabel.setObjectName("redLineBacklogLabel")
        self.redLineBacklogList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineBacklogList.setGeometry(QtCore.QRect(620, 160, 130, 100))
        self.redLineBacklogList.setMouseTracking(True)
        self.redLineBacklogList.setSelectionRectVisible(True)
        self.redLineBacklogList.setObjectName("redLineBacklogList")
        self.redLineBacklogListKeys = redLineBacklog.keys()

        # create greenLine block list
        self.greenLineBlockListLabel = QtWidgets.QLabel(self.centralwidget)
        self.greenLineBlockListLabel.setGeometry(QtCore.QRect(60, 40, 100, 17))
        self.greenLineBlockListLabel.setObjectName("greenLineBlockListLabel")
        self.greenLineBlockList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineBlockList.setGeometry(QtCore.QRect(60, 60, 100, 331))
        self.greenLineBlockList.setMouseTracking(True)
        self.greenLineBlockList.setSelectionRectVisible(True)
        self.greenLineBlockList.setObjectName("greenLineBlockList")
        self.greenLineBlockList.itemActivated.connect(self.greenSelectionChanged)
        
        self.greenLineBlocksKeys = greenLineBlocks.keys()
        for key in self.greenLineBlocksKeys:
            item = QtWidgets.QListWidgetItem()
            self.greenLineBlockList.addItem(item)

        # create greenLine switch list
        self.greenLineSwitchListLabel = QtWidgets.QLabel(self.centralwidget)
        self.greenLineSwitchListLabel.setGeometry(QtCore.QRect(170, 60, 100, 20))
        self.greenLineSwitchListLabel.setObjectName("greenLineSwitchListLabel")
        self.greenLineSwitchList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineSwitchList.setGeometry(QtCore.QRect(170, 80, 150, 100))
        self.greenLineSwitchList.setMouseTracking(True)
        self.greenLineSwitchList.setSelectionRectVisible(True)
        self.greenLineSwitchList.setObjectName("greenLineSwitchList")
        self.greenLineSwitchList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.toggleGreenLineSwitchButton = QtWidgets.QPushButton(self.centralwidget)
        self.toggleGreenLineSwitchButton.setGeometry(QtCore.QRect(170, 185, 100, 20))
        self.toggleGreenLineSwitchButton.hide()
        self.toggleGreenLineSwitchButton.clicked.connect(self.toggleGreenLineSwitchState)

        self.greenLineSwitchKeys = greenLineSwitches.keys()
        for key in self.greenLineSwitchKeys:
            item = QtWidgets.QListWidgetItem()
            item.setText(key + ": " + greenLineSwitches[key])
            self.greenLineSwitchList.addItem(item)

        # create green line train list
        self.greenLineTrainLabel = QtWidgets.QLabel(self.centralwidget)
        self.greenLineTrainLabel.setGeometry(QtCore.QRect(170, 200, 100, 20))
        self.greenLineTrainLabel.setObjectName("greenLineTrainLabel")
        self.greenLineTrainList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineTrainList.setGeometry(QtCore.QRect(170, 220, 130, 100))
        self.greenLineTrainList.setMouseTracking(False)
        self.greenLineTrainList.setSelectionRectVisible(False)
        self.greenLineTrainList.setObjectName("greenLineTrainList")
        self.greenLineTrainList.itemActivated.connect(self.greenLineTrainSelectionChanged)

        # create green line back log
        self.greenLineBacklogLabel = QtWidgets.QLabel(self.centralwidget)
        self.greenLineBacklogLabel.setGeometry(620, 260, 130, 20)
        self.greenLineBacklogLabel.setObjectName("greenLineBacklogLabel")
        self.greenLineBacklogList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineBacklogList.setGeometry(QtCore.QRect(620, 280, 130, 100))
        self.greenLineBacklogList.setMouseTracking(False)
        self.greenLineBacklogList.setSelectionRectVisible(False)
        self.greenLineBacklogList.setObjectName("greenLineBacklogList")
        self.greenLineBacklogListKeys = greenLineBacklog.keys()


        # creating block information chart
        self.blockInfo = QtWidgets.QLabel(self.centralwidget)
        self.blockInfo.setGeometry(QtCore.QRect(450, 435, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.blockInfo.setFont(font)
        self.blockInfo.setObjectName("blockInfo")
        self.blockLine = QtWidgets.QLabel(self.centralwidget)
        self.blockLine.setGeometry(QtCore.QRect(450, 460, 101, 17))
        self.blockLine.setObjectName("blockLine")
        self.occupancy = QtWidgets.QLabel(self.centralwidget)
        self.occupancy.setGeometry(QtCore.QRect(450, 480, 101, 17))
        self.occupancy.setObjectName("occupancy")
        self.faultState = QtWidgets.QLabel(self.centralwidget)
        self.faultState.setGeometry(QtCore.QRect(450, 500, 101, 17))
        self.faultState.setObjectName("faultState")
        self.maintenanceState = QtWidgets.QLabel(self.centralwidget)
        self.maintenanceState.setGeometry(QtCore.QRect(450, 520, 171, 17))
        self.maintenanceState.setObjectName("maintenanceState")
        self.startMaintenanceButton = QtWidgets.QPushButton(self.centralwidget)
        self.startMaintenanceButton.setGeometry(QtCore.QRect(450, 540, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.startMaintenanceButton.setFont(font)
        self.startMaintenanceButton.setObjectName("startMaintenanceButton")
        self.startMaintenanceButton.clicked.connect(self.toggleMaintenance)

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
        self.destinationList.setGeometry(QtCore.QRect(200, 480, 240, 71))
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

        # commanded speed button
        self.setCommandedSpeedButton = QtWidgets.QPushButton(self.centralwidget)
        self.setCommandedSpeedButton.setGeometry(QtCore.QRect(60, 510, 131, 21))
        self.setCommandedSpeedButton.setObjectName("setCommandedSpeed")
        self.setCommandedSpeedButton.clicked.connect(self.setCommandedSpeed)

        # authority button
        self.setAuthorityButton = QtWidgets.QPushButton(self.centralwidget)
        self.setAuthorityButton.setGeometry(QtCore.QRect(60, 530, 131, 21))
        self.setAuthorityButton.setObjectName("setAuthority")
        self.setAuthorityButton.clicked.connect(self.setAuthority)

        # create dispatch button
        self.toggleDestinationsButton = QtWidgets.QPushButton(self.centralwidget)
        self.toggleDestinationsButton.setGeometry(QtCore.QRect(200, 555, 131, 31))
        self.toggleDestinationsButton.setObjectName("toggleDestinationsButtons")
        self.toggleDestinationsButton.clicked.connect(self.toggleDestinations)

        self.destinationsLabel = QtWidgets.QLabel(self.centralwidget)
        self.destinationsLabel.setGeometry(QtCore.QRect(200, 460, 91, 17))
        self.destinationsLabel.setObjectName("destinations")

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
        self.timer.timeout.connect(self.updateRedLineSwitchList)
        self.timer.timeout.connect(self.updateGreenLineSwitchList)
        self.timer.timeout.connect(self.showTime)
        self.timer.timeout.connect(self.updateRedLineBacklog)
        self.timer.timeout.connect(self.checkForScheduledTrains)
        self.timer.start(10)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.redLineBlockList.isSortingEnabled()
        self.redLineBlockList.setSortingEnabled(False)
        self.greenLineBlockList.setSortingEnabled(False)
        self.dispatchTrain.setText(_translate("MainWindow", "Dispatch Train"))
        self.uploadScheduleButton.setText(_translate("MainWindow", "Upload Schedule"))
        self.throughputLabel.setText(_translate("MainWindow", "ThroughPut: "))

        # set red line block names
        self.redLineBlockListLabel.setText(_translate("MainWindow", "Red Line:"))
        for key in self.redLineBlocksKeys:
            item = self.redLineBlockList.item(redLineBlocks[key].number-1)
            item.setText(_translate("MainWindow", key))

        self.redLineSwitchListLabel.setText(_translate("MainWindow", "Switches:"))
        self.toggleRedLineSwitchButton.setText(_translate("MainWindow", "Toggle Switches"))
        self.redLineTrainLabel.setText(_translate("MainWindow", "Trains:"))
        self.redLineBacklogLabel.setText(_translate("MainWindow", "Red Line Backlog:"))

        # set green line block names
        self.greenLineBlockListLabel.setText(_translate("MainWindow", "Green Line:"))
        for key in self.greenLineBlocksKeys:
            item = self.greenLineBlockList.item(greenLineBlocks[key].number-1)
            item.setText(_translate("MainWindow", key))

        self.greenLineSwitchListLabel.setText(_translate("MainWindow", "Switches:"))
        self.toggleGreenLineSwitchButton.setText(_translate("MainWindow", "Toggle Switches"))
        self.greenLineTrainLabel.setText(_translate("MainWindow", "Trains:"))
        self.greenLineBacklogLabel.setText(_translate("MainWindow", "Green Line Backlog:"))

        # set block info text
        self.redLineBlockList.setSortingEnabled(__sortingEnabled)
        self.greenLineBlockList.setSortingEnabled(__sortingEnabled)
        self.blockLine.setText(_translate("MainWindow", "Line: Red"))
        self.blockInfo.setText(_translate("MainWindow", "Block Information: Block 1"))
        self.occupancy.setText(_translate("MainWindow", "Occupied: no"))
        self.faultState.setText(_translate("MainWindow", "Track Fault: no"))
        self.maintenanceState.setText(_translate("MainWindow", "Under Maintenance: no"))
        self.startMaintenanceButton.setText(_translate("MainWindow", "Start Maintenance"))

        # set train info test
        self.trainInfo.setText(_translate("MainWindow", "Train Information: "))
        self.trainName.setText(_translate("MainWindow", "N/A"))
        self.trainLine.setText(_translate("MainWindow", "Line: N/A"))
        self.commandedSpeed.setText(_translate("MainWindow", "Comm. Speed (mph): N/A"))
        self.authority.setText(_translate("MainWindow", "Authority (mi): N/A"))
        self.setCommandedSpeedButton.setText(_translate("MainWindow", "Command Speed"))
        self.setAuthorityButton.setText(_translate("MainWindow", "Set Authority"))
        self.toggleDestinationsButton.setText(_translate("MainWindow", "Toggle Destinations"))
        self.destinationsLabel.setText(_translate("MainWindow", "Destinations"))
        __sortingEnabled = self.destinationList.isSortingEnabled()
        self.destinationList.setSortingEnabled(False)
        item = self.destinationList.item(0)
        item.setText(_translate("MainWindow", "N/A"))
        self.destinationList.setSortingEnabled(__sortingEnabled)

#################################################################
# End UI generation, start functions
#################################################################

    def showTime(self):
        current_time = QTime.currentTime()
        self.label_time = current_time.toString('hh:mm:ss')
        self.clockLabel.setText(self.label_time)

# block methods
    def redSelectionChanged(self):
        # update block information
        selectedBlock = self.redLineBlockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        self.occupancy.setText("Occupied: " + redLineBlocks[selectedBlock].getOccupancy())
        self.faultState.setText("Track Fault: " + redLineBlocks[selectedBlock].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + redLineBlocks[selectedBlock].getMaintenanceState())
        self.blockLine.setText("Line: Red")
        if (redLineBlocks[selectedBlock].getMaintenanceState() == "yes"):
            self.startMaintenanceButton.setText("Stop Maintenance")
        elif (redLineBlocks[selectedBlock].getMaintenanceState() == "no"):
            self.startMaintenanceButton.setText("Start Maintenance")

    def greenSelectionChanged(self):
        # update block information
        selectedBlock = self.greenLineBlockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        self.occupancy.setText("Occupied: " + greenLineBlocks[selectedBlock].getOccupancy())
        self.faultState.setText("Track Fault: " + greenLineBlocks[selectedBlock].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + greenLineBlocks[selectedBlock].getMaintenanceState())
        self.blockLine.setText("Line: Green")
        if (greenLineBlocks[selectedBlock].getMaintenanceState() == "yes"):
            self.startMaintenanceButton.setText("Stop Maintenance")
        elif (greenLineBlocks[selectedBlock].getMaintenanceState() == "no"):
            self.startMaintenanceButton.setText("Start Maintenance")

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
        self.blockLineText = self.blockLine.text()
        if (self.blockLineText == "Line: Red"):
            self.redSelectionChanged()
        elif (self.blockLineText == "Line: Green"):
            self.greenSelectionChanged()

    def toggleMaintenance(self):
        if (self.blockLineText == "Line: Red"):
            self.toggleRedLineMaintenance()
        elif (self.blockLineText == "Line: Green"):
            self.toggleGreenLineMaintenance()

    def toggleGreenLineMaintenance(self):
        selectedBlock = self.greenLineBlockList.currentItem().text()
        greenLineBlocks[selectedBlock].toggleMaintenanceState()
        self.greenLineMaintenance = False
        for key in self.greenLineBlocksKeys:
            if greenLineBlocks[key].getMaintenanceState() == "yes":
                self.greenLineMaintenance = True

        if self.greenLineMaintenance:
            self.toggleGreenLineSwitchButton.show()
        else:
            self.toggleGreenLineSwitchButton.hide()

    def toggleRedLineMaintenance(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        redLineBlocks[selectedBlock].toggleMaintenanceState()
        self.redLineMaintenance = False
        for key in self.redLineBlocksKeys:
            if redLineBlocks[key].getMaintenanceState() == "yes":
                self.redLineMaintenance = True

        if self.redLineMaintenance:
            self.toggleRedLineSwitchButton.show()
        else:
            self.toggleRedLineSwitchButton.hide()

    def toggleRedLineSwitchState(self):
        self.selectedSwitches = self.redLineSwitchList.selectedItems()
        for switch in self.selectedSwitches:
            toggleRedLineSwitch(switch.text().split(":")[0])

    def toggleGreenLineSwitchState(self):
        self.selectedSwitches = self.greenLineSwitchList.selectedItems()
        for switch in self.selectedSwitches:
            toggleGreenLineSwitch(switch.text().split(":")[0])

    def updateRedLineSwitchList(self):
        self.index = 0
        for key, value in redLineSwitches.items():
            self.redLineSwitchList.item(self.index).setText(key + ": " + value)
            self.index += 1

    def updateGreenLineSwitchList(self):
        self.index = 0
        for key, value in greenLineSwitches.items():
            self.greenLineSwitchList.item(self.index).setText(key + ": " + value)
            self.index += 1

# train methods
    def launchDispatchPopUp(self):
        self.dispatchPopUp.setupUi(self.dispatchWidget)
        self.dispatchWidget.show()

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

    def setAuthority(self):
        if self.setAuthorityValue.text() == "":
            return
        self.selectedTrain = self.trainName.text()

        if self.trainLine.text() == "Line: Red":
            redLineTrains[self.selectedTrain].setAuthority(self.setAuthorityValue.text())
        elif self.trainLine.text() == "Line: Green":
            greenLineTrains[self.selectedTrain].setAuthority(self.setAuthorityValue.text())
        self.updateTrainInfo()
    
    def setCommandedSpeed(self):
        if self.setCommandedSpeedValue.text() == "":
            return
        self.selectedTrain = self.trainName.text()

        if self.trainLine.text() == "Line: Red":
            redLineTrains[self.selectedTrain].setCommandedSpeed(self.setCommandedSpeedValue.text())
        elif self.trainLine.text() == "Line: Green":
            greenLineTrains[self.selectedTrain].setCommandedSpeed(self.setCommandedSpeedValue.text())
        self.updateTrainInfo()

    def toggleDestinations(self):
        self.selectedTrain = self.trainName.text()
        self.selectedDestinations = self.destinationList.selectedItems()

        if self.trainLine.text() == "Line: Red":
            for destination in self.selectedDestinations:
                redLineTrains[self.selectedTrain].toggleDestination(destination.text().split(":")[0])
        elif self.trainLine.text() == "Line: Green":
            for destination in self.selectedDestinations:
                greenLineTrains[self.selectedTrain].toggleDestination(destination.text().split(":")[0])
        self.updateTrainInfo()

    def updateTrainInfo(self):
        if self.trainLine.text() == "Line: Red":
            self.redLineTrainSelectionChanged()
        elif self.trainLine.text() == "Line: Green":
            self.greenLineTrainSelectionChanged()

    def uploadSchedule(self):
        self.fileName = QFileDialog.getOpenFileName(QtWidgets.QStackedWidget(), 'open file', '/home/garrett/git/ECE_1140_TRAINS/CTC-Office', 'xlsx files (*.xlsx)')
        print(self.fileName[0])
        readSchedule(self.fileName[0])

    def updateRedLineBacklog(self):
        self.currentRedLineBackLog = dict()

        # checking for removed trains
        for i in range(self.redLineBacklogList.count()):
            self.currentRedLineBackLog[self.redLineBacklogList.item(i).text()] = None

            if ((self.redLineBacklogList.item(i).text() in redLineBacklog) == False):
                self.redLineBacklogList.takeItem(i)
            
        # checking for new trains
        for key in self.redLineBacklogListKeys:
            if ((key in self.currentRedLineBackLog) == False):
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.redLineBacklogList.addItem(item)

    def updateGreenLineBacklog(self):
        self.currentGreenLineBackLog = dict()

        # checking for removed trains
        for i in range(self.greenLineBacklogList.count()):
            self.currentGreenLineBackLog[self.greenLineBacklogList.item(i).text()] = None

            if ((self.greenLineBacklogList.item(i).text() in greenLineBacklog) == False):
                self.greenLineBacklogList.takeItem(i)
            
        # checking for new trains
        for key in self.greenLineBacklogListKeys:
            if ((key in self.currentGreenLineBackLog) == False):
                item = QtWidgets.QListWidgetItem()
                item.setText(key)
                self.greenLineBacklogList.addItem(item)

    def checkForScheduledTrains(self):
        for key in self.redLineBacklogListKeys:
            if key == self.clockLabel.text():
                redLineTrains[key] = redLineBacklog[key]
                redLineBacklog.pop(key)

        for key in self.greenLineBacklogListKeys:
            if key == self.clockLabel.text():
                greenLineTrains[key] = greenLineBacklog[key]
                greenLineBacklog.pop(key)


class Ui_testWindow(object):

#################################################################
# Start UI generation and setup
#################################################################
    
    def setupUi(self, testWindow):
        testWindow.setObjectName("testWindow")
        testWindow.resize(400, 400)
        self.toggleOccupancyButton = QtWidgets.QPushButton(testWindow)
        self.toggleOccupancyButton.setGeometry(QtCore.QRect(220, 280, 130, 20))
        self.toggleOccupancyButton.setObjectName("toggleOccupancyButton")
        self.toggleOccupancyButton.clicked.connect(self.toggleOccupancy)
        self.toggleFaultStateButton = QtWidgets.QPushButton(testWindow)
        self.toggleFaultStateButton.setGeometry(QtCore.QRect(220, 310, 130, 20))
        self.toggleFaultStateButton.setObjectName("toggleFaultStateButton")
        self.toggleFaultStateButton.clicked.connect(self.toggleFaultState)
        self.toggleMaintenanceStateButton = QtWidgets.QPushButton(testWindow)
        self.toggleMaintenanceStateButton.setGeometry(QtCore.QRect(220, 340, 130, 20))
        self.toggleMaintenanceStateButton.setObjectName("toggleMaintenanceStateButton")
        self.toggleMaintenanceStateButton.clicked.connect(self.toggleMaintenanceState)

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
        self.redLineBlockListLabel.setText(_translate("testWindow", "Red Line:"))
        self.redLineBlocksKeys = redLineBlocks.keys()
        for key in self.redLineBlocksKeys:
            item = self.redLineBlockList.item(redLineBlocks[key].number-1)
            item.setText(_translate("testWindow", key))

        self.redLineBlockList.setSortingEnabled(__sortingEnabled)

        # set green line block names
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
