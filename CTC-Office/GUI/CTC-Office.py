# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTC-Office.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.dispatchTrain = QtWidgets.QPushButton(self.centralwidget)
        self.dispatchTrain.setGeometry(QtCore.QRect(620, 50, 131, 31))
        self.dispatchTrain.setObjectName("dispatchTrain")
        self.uploadSchedule = QtWidgets.QPushButton(self.centralwidget)
        self.uploadSchedule.setGeometry(QtCore.QRect(620, 120, 131, 31))
        self.uploadSchedule.setObjectName("uploadSchedule")
        self.trainList = QtWidgets.QListWidget(self.centralwidget)
        self.trainList.setGeometry(QtCore.QRect(620, 200, 131, 101))
        self.trainList.setMouseTracking(True)
        self.trainList.setSelectionRectVisible(True)
        self.trainList.setObjectName("trainList")
        item = QtWidgets.QListWidgetItem()
        self.trainList.addItem(item)
        self.blockList = QtWidgets.QListWidget(self.centralwidget)
        self.blockList.setGeometry(QtCore.QRect(620, 340, 131, 111))
        self.blockList.setMouseTracking(True)
        self.blockList.setSelectionRectVisible(True)
        self.blockList.setObjectName("blockList")
        item = QtWidgets.QListWidgetItem()
        self.blockList.addItem(item)
        self.blockInfo = QtWidgets.QLabel(self.centralwidget)
        self.blockInfo.setGeometry(QtCore.QRect(350, 430, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.blockInfo.setFont(font)
        self.blockInfo.setObjectName("blockInfo")
        self.trainInfo = QtWidgets.QLabel(self.centralwidget)
        self.trainInfo.setGeometry(QtCore.QRect(30, 430, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.trainInfo.setFont(font)
        self.trainInfo.setObjectName("trainInfo")
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
        self.startMaintenance.setGeometry(QtCore.QRect(350, 520, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.startMaintenance.setFont(font)
        self.startMaintenance.setObjectName("startMaintenance")
        self.destinationList = QtWidgets.QListWidget(self.centralwidget)
        self.destinationList.setGeometry(QtCore.QRect(200, 480, 111, 71))
        self.destinationList.setMouseTracking(True)
        self.destinationList.setSelectionRectVisible(True)
        self.destinationList.setObjectName("destinationList")
        item = QtWidgets.QListWidgetItem()
        self.destinationList.addItem(item)
        self.destinations = QtWidgets.QLabel(self.centralwidget)
        self.destinations.setGeometry(QtCore.QRect(200, 460, 91, 17))
        self.destinations.setObjectName("destinations")
        self.setCommandedSpeedValue = QtWidgets.QLineEdit(self.centralwidget)
        self.setCommandedSpeedValue.setGeometry(QtCore.QRect(30, 510, 31, 21))
        self.setCommandedSpeedValue.setObjectName("setCommandedSpeedValue")
        self.setAuthorityValue = QtWidgets.QLineEdit(self.centralwidget)
        self.setAuthorityValue.setGeometry(QtCore.QRect(30, 530, 31, 21))
        self.setAuthorityValue.setObjectName("setAuthorityValue")
        self.setCOmmandedSpeed = QtWidgets.QPushButton(self.centralwidget)
        self.setCOmmandedSpeed.setGeometry(QtCore.QRect(60, 510, 131, 21))
        self.setCOmmandedSpeed.setObjectName("setCOmmandedSpeed")
        self.setAuthority = QtWidgets.QPushButton(self.centralwidget)
        self.setAuthority.setGeometry(QtCore.QRect(60, 530, 131, 21))
        self.setAuthority.setObjectName("setAuthority")
        self.authority = QtWidgets.QLabel(self.centralwidget)
        self.authority.setGeometry(QtCore.QRect(30, 490, 141, 17))
        self.authority.setObjectName("authority")
        self.commandedSpeed = QtWidgets.QLabel(self.centralwidget)
        self.commandedSpeed.setGeometry(QtCore.QRect(30, 470, 161, 17))
        self.commandedSpeed.setObjectName("commandedSpeed")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dispatchTrain.setText(_translate("MainWindow", "Dispatch Train"))
        self.uploadSchedule.setText(_translate("MainWindow", "Upload Schedule"))
        __sortingEnabled = self.trainList.isSortingEnabled()
        self.trainList.setSortingEnabled(False)
        item = self.trainList.item(0)
        item.setText(_translate("MainWindow", "Train 1"))
        self.trainList.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.blockList.isSortingEnabled()
        self.blockList.setSortingEnabled(False)
        item = self.blockList.item(0)
        item.setText(_translate("MainWindow", "Block A"))
        self.blockList.setSortingEnabled(__sortingEnabled)
        self.blockInfo.setText(_translate("MainWindow", "Block Information: Block A"))
        self.trainInfo.setText(_translate("MainWindow", "Train Information: Train 1"))
        self.occupancy.setText(_translate("MainWindow", "Occupied: yes"))
        self.faultState.setText(_translate("MainWindow", "Track Fault: no"))
        self.maintenanceState.setText(_translate("MainWindow", "Under Maintenance: no"))
        self.startMaintenance.setText(_translate("MainWindow", "Start Maintenance"))
        __sortingEnabled = self.destinationList.isSortingEnabled()
        self.destinationList.setSortingEnabled(False)
        item = self.destinationList.item(0)
        item.setText(_translate("MainWindow", "Station A"))
        self.destinationList.setSortingEnabled(__sortingEnabled)
        self.destinations.setText(_translate("MainWindow", "Destinations"))
        self.setCOmmandedSpeed.setText(_translate("MainWindow", "Command Speed"))
        self.setAuthority.setText(_translate("MainWindow", "Set Authority"))
        self.authority.setText(_translate("MainWindow", "Authority: 28 mi"))
        self.commandedSpeed.setText(_translate("MainWindow", "Comm. Speed: 25 mph"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
