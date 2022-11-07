# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_test_window(object):
    def __init__(self, ref):
        self.main_window = ref

    def setupUi(self, test_window):
        if not test_window.objectName():
            test_window.setObjectName(u"test_window")
        test_window.resize(494, 449)
        self.gridLayout = QGridLayout(test_window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(test_window)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.line_select = QComboBox(self.groupBox)
        self.line_select.addItem("Red")
        self.line_select.addItem("Green")
        self.line_select.setObjectName(u"line_select")
        # self.line_select.connect(self.setBlockList())

        self.horizontalLayout_3.addWidget(self.line_select)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.block_select = QComboBox(self.groupBox_3)
        self.block_select.setObjectName(u"block_select")

        ## TODO Add drop down section for blocks in a line
        if self.line_select.currentText().lower() == "red":
            for i in range(self.main_window.getNumRedLineBlocks()):
                self.block_select.addItem(str(i +1))

        self.horizontalLayout_4.addWidget(self.block_select)


        self.verticalLayout_4.addWidget(self.groupBox_3)


        self.horizontalLayout.addLayout(self.verticalLayout_4)


        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(test_window)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toggle_occupancy = QCheckBox(self.groupBox_4)
        self.toggle_occupancy.setObjectName(u"toggle_occupancy")

        self.toggle_occupancy.connect(self.toggleOccupancy())

        self.verticalLayout.addWidget(self.toggle_occupancy)

        self.toggle_crossing = QCheckBox(self.groupBox_4)
        self.toggle_crossing.setObjectName(u"toggle_crossing")

        self.toggle_crossing.connect(self.toggleCrossing())

        self.verticalLayout.addWidget(self.toggle_crossing)

        self.toggle_switch = QCheckBox(self.groupBox_4)
        self.toggle_switch.setObjectName(u"toggle_switch")

        self.toggle_switch.connect(self.toggle_switch())

        self.verticalLayout.addWidget(self.toggle_switch)

        self.toggle_maintenance = QCheckBox(self.groupBox_4)
        self.toggle_maintenance.setObjectName(u"toggle_maintenance")
        self.toggle_maintenance.connect(self.toggleMaintenance())

        self.verticalLayout.addWidget(self.toggle_maintenance)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.broken_rail = QCheckBox(self.groupBox_4)
        self.broken_rail.setObjectName(u"broken_rail")
        self.broken_rail.connect(self.setFaults())

        self.verticalLayout_2.addWidget(self.broken_rail)

        self.circuit_failure = QCheckBox(self.groupBox_4)
        self.circuit_failure.setObjectName(u"checkBox_6")
        self.circuit_failure.connect(self.setFaults())

        self.verticalLayout_2.addWidget(self.circuit_failure)

        self.power_failure = QCheckBox(self.groupBox_4)
        self.power_failure.setObjectName(u"power_failure")
        self.power_failure.connect(self.setFaults)

        self.verticalLayout_2.addWidget(self.power_failure)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)


        self.retranslateUi(test_window)

        QMetaObject.connectSlotsByName(test_window)

    def retranslateUi(self, test_window):
        test_window.setWindowTitle(QCoreApplication.translate("test_window", u"test_window", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("test_window", u"Block Selection", None))
        self.groupBox.setTitle(QCoreApplication.translate("test_window", u"Select Line", None))

        self.groupBox_3.setTitle(QCoreApplication.translate("test_window", u"Select Block", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("test_window", u"Test Input", None))
        self.toggle_occupancy.setText(QCoreApplication.translate("test_window", u"Occupy Block", None))
        self.toggle_crossing.setText(QCoreApplication.translate("test_window", u"Toggle Crossing", None))
        self.toggle_switch.setText(QCoreApplication.translate("test_window", u"Toggle Switch", None))
        self.toggle_maintenance.setText(QCoreApplication.translate("test_window", u"Maintenance", None))
        self.broken_rail.setText(QCoreApplication.translate("test_window", u"Broken Rail", None))
        self.circuit_failure.setText(QCoreApplication.translate("test_window", u"Circuit Failure", None))
        self.power_failure.setText(QCoreApplication.translate("test_window", u"Power Failure", None))

    def setBlockList(self):
        # self.block_select.clear()
        # self.block_select.
        # if self.line_select.currentText().lower() == 'red':
        #     for i in range(self.main_window.getNumRedLineBlocks()):
        #         self.block_select.addItem(str(i +1))
        # if self.line_select.currentText().lower() == 'green':
        #     for i in range(self.main_window.getNumGreenLineBlocks()):
        #         self.block_select.addItem(str(i +1))
        return

    def toggleOccupancy(self):
        return

    def toggleSwitch(self):
        return

    def toggleCrossing(self):
        return

    def toggleMaintenance(self):
        return

    def setFaults(self):
        return

