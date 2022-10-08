# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/block-functionality/')
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from lines import redLine, redLineLookup, greenLine, greenLineLookup

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

        # create redLine block list
        self.redLineBlockList = QtWidgets.QListWidget(self.centralwidget)
        self.redLineBlockList.setGeometry(QtCore.QRect(330, 50, 181, 331))
        self.redLineBlockList.setMouseTracking(True)
        self.redLineBlockList.setSelectionRectVisible(True)
        self.redLineBlockList.setObjectName("redLineBlockList")
        self.redLineBlockList.itemActivated.connect(self.redSelectionChanged)

        for i in range(0,10):
            item = QtWidgets.QListWidgetItem()
            self.redLineBlockList.addItem(item)

        self.redLineBlockList.setCurrentRow(0)

        # create greenLine block list
        self.greenLineBlockList = QtWidgets.QListWidget(self.centralwidget)
        self.greenLineBlockList.setGeometry(QtCore.QRect(120, 50, 181, 331))
        self.greenLineBlockList.setMouseTracking(True)
        self.greenLineBlockList.setSelectionRectVisible(True)
        self.greenLineBlockList.setObjectName("greenLineBlockList")
        self.greenLineBlockList.itemActivated.connect(self.greenSelectionChanged)
        
        for i in range(0,10):
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

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # set up timer refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateRedLineBlockList)
        self.timer.timeout.connect(self.updateBlockInfo)
        self.timer.start(1000)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.redLineBlockList.isSortingEnabled()
        self.redLineBlockList.setSortingEnabled(False)
        self.greenLineBlockList.setSortingEnabled(False)

        # set red line block names
        for i in range(0,10):
            item = self.redLineBlockList.item(i)
            item.setText(_translate("MainWindow", "Block " + str(redLine[i].name)))

        # set green line block names
        for i in range(0,10):
            item = self.greenLineBlockList.item(i)
            item.setText(_translate("MainWindow", "Block " + str(greenLine[i].name)))

        self.redLineBlockList.setSortingEnabled(__sortingEnabled)
        self.greenLineBlockList.setSortingEnabled(__sortingEnabled)
        self.blockLine.setText(_translate("MainWindow", "Line: Red"))
        self.blockInfo.setText(_translate("MainWindow", "Block Information: Block 1"))
        self.occupancy.setText(_translate("MainWindow", "Occupied: no"))
        self.faultState.setText(_translate("MainWindow", "Track Fault: no"))
        self.maintenanceState.setText(_translate("MainWindow", "Under Maintenance: no"))
        self.startMaintenance.setText(_translate("MainWindow", "Start Maintenance"))

#################################################################
# End UI generation, start functions
#################################################################

    def redSelectionChanged(self):
        # update block information
        selectedBlock = self.redLineBlockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        blockIndex = redLineLookup[selectedBlock]
        self.occupancy.setText("Occupied: " + redLine[blockIndex].getOccupancy())
        self.faultState.setText("Track Fault: " + redLine[blockIndex].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + redLine[blockIndex].getMaintenanceState())
        self.blockLine.setText("Line: Red")

    def greenSelectionChanged(self):
        # update block information
        selectedBlock = self.greenLineBlockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        blockIndex = greenLineLookup[selectedBlock]
        self.occupancy.setText("Occupied: " + greenLine[blockIndex].getOccupancy())
        self.faultState.setText("Track Fault: " + greenLine[blockIndex].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + greenLine[blockIndex].getMaintenanceState())
        self.blockLine.setText("Line: Green")

    def updateRedLineBlockList(self):
        for i in range(0,9):
            item = self.redLineBlockList.item(i)
            selectedBlock = item.text()
            blockIndex = redLineLookup[selectedBlock]

            if (redLine[blockIndex].getMaintenanceState() == "yes"):
                item.setBackground(Qt.yellow)
            elif (redLine[blockIndex].getFaultState() == "yes"):
                item.setBackground(Qt.red)
            elif (redLine[blockIndex].getOccupancy() == "yes"):
                item.setBackground(Qt.green)
            else:
                item.setBackground(Qt.white)

    def updateBlockInfo(self):
        blockLine = self.blockLine.text()
        if (blockLine == "Line: Red"):
            self.redSelectionChanged
        elif (blockLine == "Line: Green"):
            self.greenSelectionChanged


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
        for i in range(0,10):
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
        for blockIndex in range(0,10):
            item = self.redLineBlockList.item(blockIndex)
            item.setText(_translate("MainWindow", "Block " + str(redLine[blockIndex].name)))

        self.redLineBlockList.setSortingEnabled(__sortingEnabled)

#################################################################
# End UI generation, start functions
#################################################################

    def toggleFaultState(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        blockIndex = redLineLookup[selectedBlock]
        redLine[blockIndex].toggleFaultState()

    def toggleOccupancy(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        blockIndex = redLineLookup[selectedBlock]
        redLine[blockIndex].toggleOccupancy()

    def toggleMaintenanceState(self):
        selectedBlock = self.redLineBlockList.currentItem().text()
        blockIndex = redLineLookup[selectedBlock]
        redLine[blockIndex].toggleMaintenanceState()

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

