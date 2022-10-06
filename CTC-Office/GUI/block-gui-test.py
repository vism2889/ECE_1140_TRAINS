# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTC-Office-baby.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from lines import redLine, redLineLookup

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")

        self.blockList = QtWidgets.QListWidget(self.centralwidget)
        self.blockList.setGeometry(QtCore.QRect(620, 340, 131, 111))
        self.blockList.setMouseTracking(True)
        self.blockList.setSelectionRectVisible(True)
        self.blockList.setObjectName("blockList")
        self.blockList.itemActivated.connect(self.selectionChanged)
        item = QtWidgets.QListWidgetItem()
        self.blockList.addItem(item)

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.blockList.isSortingEnabled()
        self.blockList.setSortingEnabled(False)
        item = self.blockList.item(0)
        item.setText(_translate("MainWindow", "Block B"))
        self.blockList.setSortingEnabled(__sortingEnabled)
        self.blockInfo.setText(_translate("MainWindow", "Block Information: Block A"))
        self.occupancy.setText(_translate("MainWindow", "Occupied: yes"))
        self.faultState.setText(_translate("MainWindow", "Track Fault: no"))
        self.maintenanceState.setText(_translate("MainWindow", "Under Maintenance: no"))
        self.startMaintenance.setText(_translate("MainWindow", "Start Maintenance"))

    def selectionChanged(self):
        selectedBlock = self.blockList.currentItem().text()
        self.blockInfo.setText("Block Information: " + selectedBlock)

        blockIndex = redLineLookup[selectedBlock]
        self.occupancy.setText("Occupied: " + redLine[blockIndex].getOccupancy())
        self.faultState.setText("Track Fault: " + redLine[blockIndex].getFaultState())
        self.maintenanceState.setText("Under Maintenance: " + redLine[blockIndex].getMaintenanceState())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
