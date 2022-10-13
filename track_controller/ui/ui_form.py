# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_test_window(object):
    def __init__(self, ref):
        self.main_window = ref

    def setupUi(self, test_window):
        test_window.setObjectName("test_window")
        test_window.resize(494, 449)
        self.gridLayout = QtWidgets.QGridLayout(test_window)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(test_window)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.line_select = QtWidgets.QComboBox(self.groupBox)
        self.line_select.setObjectName("line_select")
        self.line_select.addItem("Red")
        self.line_select.addItem("Green")
        self.line_select.activated.connect(lambda: self.setBlockList())

        self.horizontalLayout_3.addWidget(self.line_select)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.block_select = QtWidgets.QComboBox(self.groupBox_3)
        self.block_select.setObjectName("block_select")

        ## TODO Add drop down section for blocks in a line
        if self.line_select.currentText().lower() == "red":
            for i in range(self.main_window.getNumRedLineBlocks()):
                self.block_select.addItem(str(i +1))

        self.horizontalLayout_4.addWidget(self.block_select)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_4 = QtWidgets.QGroupBox(test_window)
        self.groupBox_4.setObjectName("groupBox_4")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.toggle_occupancy = QtWidgets.QCheckBox(self.groupBox_4)
        self.toggle_occupancy.setObjectName("toggle_occupancy")
        self.toggle_occupancy.clicked.connect(lambda: self.toggleOccupancy())
        self.verticalLayout.addWidget(self.toggle_occupancy)

        self.toggle_crossing = QtWidgets.QCheckBox(self.groupBox_4)
        self.toggle_crossing.setObjectName("toggle_crossing")
        self.toggle_crossing.clicked.connect(lambda: self.toggleCrossing())
        self.verticalLayout.addWidget(self.toggle_crossing)

        self.toggle_switch = QtWidgets.QCheckBox(self.groupBox_4)
        self.toggle_switch.setObjectName("toggle_switch")
        self.toggle_switch.clicked.connect(lambda: self.toggleSwitch())
        self.verticalLayout.addWidget(self.toggle_switch)

        self.toggle_maintenance = QtWidgets.QCheckBox(self.groupBox_4)
        self.toggle_maintenance.setObjectName("toggle_maintenance")
        self.toggle_maintenance.clicked.connect(lambda: self.toggleMaintenance())
        self.verticalLayout.addWidget(self.toggle_maintenance)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.broken_rail = QtWidgets.QCheckBox(self.groupBox_4)
        self.broken_rail.setObjectName("broken_rail")
        self.broken_rail.clicked.connect(lambda: self.setFaults())
        self.verticalLayout_2.addWidget(self.broken_rail)

        self.circuilt_failure = QtWidgets.QCheckBox(self.groupBox_4)
        self.circuilt_failure.setObjectName("checkBox_6")
        self.circuilt_failure.clicked.connect(lambda: self.setFaults())
        self.verticalLayout_2.addWidget(self.circuilt_failure)

        self.power_failure = QtWidgets.QCheckBox(self.groupBox_4)
        self.power_failure.setObjectName("power_failure")
        self.power_failure.setObjectName(u"power_failure")
        self.power_failure.clicked.connect(lambda: self.setFaults())

        self.verticalLayout_2.addWidget(self.power_failure)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.retranslateUi(test_window)
        QtCore.QMetaObject.connectSlotsByName(test_window)

    def retranslateUi(self, test_window):
        _translate = QtCore.QCoreApplication.translate
        test_window.setWindowTitle(_translate("test_window", "test_window"))
        self.groupBox_2.setTitle(_translate("test_window", "Block Selection"))
        self.groupBox.setTitle(_translate("test_window", "Select Line"))
        self.groupBox_3.setTitle(_translate("test_window", "Select Block"))
        self.groupBox_4.setTitle(_translate("test_window", "Test Input"))
        self.toggle_occupancy.setText(_translate("test_window", "Occupy Block"))
        self.toggle_crossing.setText(_translate("test_window", "Toggle Crossing"))
        self.toggle_switch.setText(_translate("test_window", "Toggle Switch"))
        self.toggle_maintenance.setText(_translate("test_window", "Maintenance"))
        self.broken_rail.setText(_translate("test_window", "Broken Rail"))
        self.circuilt_failure.setText(_translate("test_window", "Circuit Failure"))
        self.power_failure.setText(_translate("test_window", "Power Failure"))

    def setBlockList(self):
        self.block_select.clear()
        if self.line_select.currentText().lower() == 'red':
            for i in range(self.main_window.getNumRedLineBlocks()):
                self.block_select.addItem(str(i +1))
        if self.line_select.currentText().lower() == 'green':
            for i in range(self.main_window.getNumGreenLineBlocks()):
                self.block_select.addItem(str(i +1))
        return

    def toggleOccupancy(self):
        state = self.toggle_occupancy.isChecked()
        block_num = self.block_select.currentText()
        if self.line_select.currentText().lower() == 'red':
            self.main_window.setBlockState('red', int(block_num), state)
        if self.line_select.currentText().lower() == 'green':
            self.main_window.setBlockState('green', int(block_num), state)

    def toggleSwitch(self):
        state = self.toggle_switch.isChecked()
        block_num = self.block_select.currentText()

        if self.line_select.currentText().lower() == 'red':
            self.main_window.setSwitchState('red', int(block_num), state)
        if self.line_select.currentText().lower() == 'green':
            self.main_window.setSwitchState('green', int(block_num), state)

    def toggleCrossing(self):
        state = self.toggle_crossing.isChecked()
        block_num = self.block_select.currentText()

        if self.line_select.currentText().lower() == 'red':
            self.main_window.setCrossingState('red', int(block_num), state)
        if self.line_select.currentText().lower() == 'green':
            self.main_window.setCrossingState('green', int(block_num), state)

    def toggleMaintenance(self):
        state = self.toggle_maintenance.isChecked()
        block_num = self.block_select.currentText()
        if self.line_select.currentText().lower() == 'red':
            self.main_window.setMaintenance('red', int(block_num), state)
        if self.line_select.currentText().lower() == 'green':
            self.main_window.setMaintenance('green', int(block_num), state)

    def setFaults(self):
        curr_faults = []
        block_num = self.block_select.currentText()
        if self.broken_rail.isChecked():
            curr_faults.append(1)
        if self.circuilt_failure.isChecked():
            curr_faults.append(2)
        if self.power_failure.isChecked():
            curr_faults.append(3)

        if self.line_select.currentText().lower() == 'red':
            self.main_window.setFaultState('red', int(block_num), curr_faults)
        if self.line_select.currentText().lower() == 'green':
            self.main_window.setFaultState('green', int(block_num), curr_faults)