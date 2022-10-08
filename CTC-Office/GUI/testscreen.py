# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/garrett/git/ECE_1140_TRAINS/CTC-Office/block-functionality')
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from lines import redLine, redLineLookup



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
        self.blockList = QtWidgets.QListWidget(self.centralwidget)
        self.blockList.setGeometry(QtCore.QRect(330, 50, 181, 331))
        self.blockList.setMouseTracking(True)
        self.blockList.setSelectionRectVisible(True)
        self.blockList.setObjectName("blockList")
        self.blockList.itemActivated.connect(self.selectionChanged)

        for i in range(0,10):
            item = QtWidgets.QListWidgetItem()
            self.blockList.addItem(item)

        self.blockList.setCurrentRow(0)

        # creating block information chart
        self.blockInfo = QtWidgets.QLabel(self.centralwidget)
        self.blockInfo.setGeometry(QtCore.QRect(350, 430, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.blockInfo.setFont(font)
        self.blockInfo.setObjectName("blockInfo")
        self.occupancy = QtWidgets.QLabel(self.centralwidget)
        self.occupancy.setGeometry(QtCore.QRect(350, 460, 101, 17))
        self.occupancy.setObjectName("occupancy")
        self.faultState = QtWidgets.QLabel(self.centralwidget)
        self.faultState.setGeometry(QtCore.QRect(350, 480, 101, 17))
        self.faultState.setObjectName("faultState")
        self.maintenanceState = QtWidgets.QLabel(self.centralwidget)
        self.maintenanceState.setGeometry(QtCore.QRect(350, 500, 171, 17))
        self.maintenanceState.setObjectName("maintenanceState")
        self.startMaintenance = QtWidgets.QPushButton(self.centralwidget)
        self.startMaintenance.setGeometry(QtCore.QRect(350, 520, 171, 31))
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
        self.timer.timeout.connect(self.updateOccupancies)
        self.timer.timeout.connect(self.selectionChanged)
        self.timer.start(1000)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.blockList.isSortingEnabled()
        self.blockList.setSortingEnabled(False)

        # set red line block names
        for i in range(0,10):
            item = self.blockList.item(i)
            item.setText(_translate("MainWindow", "Block " + str(redLine[i].name)))

        self.blockList.setSortingEnabled(__sortingEnabled)
        self.blockInfo.setText(_translate("MainWindow", "Block Information: Block 1"))
        self.occupancy.setText(_translate("MainWindow", "Occupied: no"))
        self.faultState.setText(_translate("MainWindow", "Track Fault: no"))
        self.maintenanceState.setText(_translate("MainWindow", "Under Maintenance: no"))
        self.startMaintenance.setText(_translate("MainWindow", "Start Maintenance"))

#################################################################
# End UI generation, start functions
#################################################################

    def selectionChanged(self):
        # update block information
        selectedBlock = self.blockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        blockIndex = redLineLookup[selectedBlock]
        self.occupancy.setText("Occupied: " + redLine[blockIndex].getOccupancy())
        self.faultState.setText("Track Fault: " + redLine[blockIndex].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + redLine[blockIndex].getMaintenanceState())

    def updateOccupancies(self):
        for i in range(0,9):
            item = self.blockList.item(i)
            selectedBlock = item.text()
            blockIndex = redLineLookup[selectedBlock]

            if (redLine[blockIndex].getOccupancy() == "yes"):
                item.setBackground(Qt.green)


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
        self.blockList = QtWidgets.QListWidget(testWindow)
        self.blockList.setGeometry(QtCore.QRect(220, 120, 131, 111))
        self.blockList.setMouseTracking(True)
        self.blockList.setSelectionRectVisible(True)
        self.blockList.setObjectName("blockList")

        # create redLine block list
        for i in range(0,10):
            item = QtWidgets.QListWidgetItem()
            self.blockList.addItem(item)

        self.retranslateUi(testWindow)
        QtCore.QMetaObject.connectSlotsByName(testWindow)

    def retranslateUi(self, testWindow):
        _translate = QtCore.QCoreApplication.translate
        testWindow.setWindowTitle(_translate("testWindow", "Form"))
        self.toggleOccupancyButton.setText(_translate("testWindow", "Toggle Occupancy"))
        self.toggleFaultStateButton.setText(_translate("testWindow", "Toggle Fault State"))
        self.toggleMaintenanceStateButton.setText(_translate("testWindow", "Toggle Maintenance"))
        __sortingEnabled = self.blockList.isSortingEnabled()
        self.blockList.setSortingEnabled(False)

        # set red line block names
        for blockIndex in range(0,10):
            item = self.blockList.item(blockIndex)
            item.setText(_translate("MainWindow", "Block " + str(redLine[blockIndex].name)))

        self.blockList.setSortingEnabled(__sortingEnabled)

#################################################################
# End UI generation, start functions
#################################################################

    def toggleFaultState(self):
        selectedBlock = self.blockList.currentItem().text()
        blockIndex = redLineLookup[selectedBlock]
        redLine[blockIndex].toggleFaultState()

    def toggleOccupancy(self):
        selectedBlock = self.blockList.currentItem().text()
        blockIndex = redLineLookup[selectedBlock]
        redLine[blockIndex].toggleOccupancy()

    def toggleMaintenanceState(self):
        selectedBlock = self.blockList.currentItem().text()
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

