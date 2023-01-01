# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gaugeWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 565)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.speedometer = AnalogGaugeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.speedometer.sizePolicy().hasHeightForWidth())
        self.speedometer.setSizePolicy(sizePolicy)
        self.speedometer.setMinimumSize(QtCore.QSize(100, 100))
        self.speedometer.setMaximumSize(QtCore.QSize(400, 400))
        self.speedometer.setBaseSize(QtCore.QSize(200, 200))
        self.speedometer.setStyleSheet("")
        self.speedometer.setObjectName("speedometer")

        self.powerGauge = AnalogGaugeWidget(self.speedometer)
        self.powerGauge.setGeometry(QtCore.QRect(150, 170, 301, 261))
        self.powerGauge.setSizePolicy(sizePolicy)
        self.powerGauge.setMinimumSize(QtCore.QSize(100, 100))
        self.powerGauge.setMaximumSize(QtCore.QSize(250, 250))
        self.powerGauge.setBaseSize(QtCore.QSize(200, 200))
        self.powerGauge.setStyleSheet("")
        self.powerGauge.setObjectName("powerGauge")
        self.verticalLayout.addWidget(self.speedometer)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.label_mph = QtWidgets.QLabel(self.centralwidget)
        self.label_mph.setGeometry(QtCore.QRect(320, 270, 81, 51))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_mph.setFont(font)
        self.label_mph.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mph.setObjectName("label_mph")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, 190, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label_power")
            
        MainWindow.setCentralWidget(self.centralwidget)

        self.powerGauge.move(75, 75)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AnalogGaugeWidget_Demo"))
        self.label_mph.setText(_translate("MainWindow", "MPH"))
        self.label.setText(_translate("MainWindow", "HP"))
from analoggaugewidget import AnalogGaugeWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
