# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trainController_testUI_hw.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DriverTestUI(object):
    def setupUi(self, DriverTestUI):
        DriverTestUI.setObjectName("DriverTestUI")
        DriverTestUI.resize(907, 553)
        DriverTestUI.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(DriverTestUI)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 90, 71, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.currentSpeed_slider = QtWidgets.QSlider(self.centralwidget)
        self.currentSpeed_slider.setGeometry(QtCore.QRect(570, 200, 71, 201))
        self.currentSpeed_slider.setOrientation(QtCore.Qt.Vertical)
        self.currentSpeed_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.currentSpeed_slider.setTickInterval(0)
        self.currentSpeed_slider.setObjectName("currentSpeed_slider")
        self.lcd_power = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_power.setGeometry(QtCore.QRect(20, 130, 111, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcd_power.setFont(font)
        self.lcd_power.setObjectName("lcd_power")
        self.lights_internal_button = QtWidgets.QPushButton(self.centralwidget)
        self.lights_internal_button.setGeometry(QtCore.QRect(570, 470, 89, 25))
        self.lights_internal_button.setObjectName("lights_internal_button")
        self.lights_external_button = QtWidgets.QPushButton(self.centralwidget)
        self.lights_external_button.setGeometry(QtCore.QRect(570, 500, 89, 25))
        self.lights_external_button.setObjectName("lights_external_button")
        self.doors_left_button = QtWidgets.QPushButton(self.centralwidget)
        self.doors_left_button.setGeometry(QtCore.QRect(720, 470, 89, 25))
        self.doors_left_button.setObjectName("doors_left_button")
        self.doors_right_button = QtWidgets.QPushButton(self.centralwidget)
        self.doors_right_button.setGeometry(QtCore.QRect(720, 500, 89, 25))
        self.doors_right_button.setObjectName("doors_right_button")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(580, 440, 67, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(730, 440, 67, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.e_brake_button = QtWidgets.QPushButton(self.centralwidget)
        self.e_brake_button.setGeometry(QtCore.QRect(240, 300, 131, 121))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.e_brake_button.setFont(font)
        self.e_brake_button.setAutoFillBackground(False)
        self.e_brake_button.setObjectName("e_brake_button")
        self.announce_start_button = QtWidgets.QPushButton(self.centralwidget)
        self.announce_start_button.setGeometry(QtCore.QRect(420, 470, 89, 25))
        self.announce_start_button.setObjectName("announce_start_button")
        self.announce_stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.announce_stop_button.setGeometry(QtCore.QRect(420, 500, 89, 25))
        self.announce_stop_button.setObjectName("announce_stop_button")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(420, 440, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 90, 91, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.speed_slider = QtWidgets.QSlider(self.centralwidget)
        self.speed_slider.setGeometry(QtCore.QRect(430, 200, 71, 201))
        self.speed_slider.setOrientation(QtCore.Qt.Vertical)
        self.speed_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.speed_slider.setObjectName("speed_slider")
        self.lcd_speed = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_speed.setGeometry(QtCore.QRect(420, 130, 101, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcd_speed.setFont(font)
        self.lcd_speed.setObjectName("lcd_speed")
        self.temperature_box = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.temperature_box.setGeometry(QtCore.QRect(820, 360, 71, 32))
        self.temperature_box.setMinimum(50.0)
        self.temperature_box.setMaximum(90.0)
        self.temperature_box.setProperty("value", 72.0)
        self.temperature_box.setObjectName("temperature_box")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(820, 330, 71, 22))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(600, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.lcd_curredSpeed = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_curredSpeed.setGeometry(QtCore.QRect(550, 130, 101, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcd_curredSpeed.setFont(font)
        self.lcd_curredSpeed.setObjectName("lcd_curredSpeed")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(540, 90, 151, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.lcd_suggested = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_suggested.setGeometry(QtCore.QRect(190, 130, 101, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lcd_suggested.setFont(font)
        self.lcd_suggested.setObjectName("lcd_suggested")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(170, 90, 181, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(110, 40, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(740, 230, 31, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.ki_spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ki_spinBox.setGeometry(QtCore.QRect(820, 270, 71, 32))
        self.ki_spinBox.setObjectName("ki_spinBox")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(840, 230, 31, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.kp_spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.kp_spinBox.setGeometry(QtCore.QRect(720, 270, 71, 32))
        self.kp_spinBox.setObjectName("kp_spinBox")
        self.suggestedSpeed_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.suggestedSpeed_spinBox.setGeometry(QtCore.QRect(720, 360, 71, 31))
        self.suggestedSpeed_spinBox.setProperty("value", 0)
        self.suggestedSpeed_spinBox.setObjectName("suggestedSpeed_spinBox")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(670, 330, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 230, 361, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(350, 0, 20, 241))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 270, 211, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.nextStationTable = QtWidgets.QTableWidget(self.centralwidget)
        self.nextStationTable.setGeometry(QtCore.QRect(10, 300, 201, 121))
        self.nextStationTable.setObjectName("nextStationTable")
        self.nextStationTable.setColumnCount(1)
        self.nextStationTable.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.nextStationTable.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.nextStationTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nextStationTable.setItem(6, 0, item)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(700, 150, 111, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.authority_spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.authority_spinBox.setGeometry(QtCore.QRect(720, 180, 71, 32))
        self.authority_spinBox.setProperty("value", 10.0)
        self.authority_spinBox.setObjectName("authority_spinBox")
        self.serviceBrake_button = QtWidgets.QPushButton(self.centralwidget)
        self.serviceBrake_button.setGeometry(QtCore.QRect(240, 450, 131, 61))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.serviceBrake_button.setFont(font)
        self.serviceBrake_button.setAutoFillBackground(False)
        self.serviceBrake_button.setObjectName("serviceBrake_button")
        DriverTestUI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DriverTestUI)
        self.statusbar.setObjectName("statusbar")
        DriverTestUI.setStatusBar(self.statusbar)

        self.retranslateUi(DriverTestUI)
        self.speed_slider.valueChanged['int'].connect(self.lcd_speed.display)
        self.temperature_box.valueChanged['double'].connect(self.temperature_box.setValue)
        self.currentSpeed_slider.valueChanged['int'].connect(self.lcd_curredSpeed.display)
        self.suggestedSpeed_spinBox.valueChanged['int'].connect(self.lcd_suggested.display)
        QtCore.QMetaObject.connectSlotsByName(DriverTestUI)

    def retranslateUi(self, DriverTestUI):
        _translate = QtCore.QCoreApplication.translate
        DriverTestUI.setWindowTitle(_translate("DriverTestUI", "MainWindow"))
        self.label.setText(_translate("DriverTestUI", "Power(W)"))
        self.lights_internal_button.setText(_translate("DriverTestUI", "Internal"))
        self.lights_external_button.setText(_translate("DriverTestUI", "External"))
        self.doors_left_button.setText(_translate("DriverTestUI", "Left"))
        self.doors_right_button.setText(_translate("DriverTestUI", "Right"))
        self.label_3.setText(_translate("DriverTestUI", "Lights"))
        self.label_4.setText(_translate("DriverTestUI", "Doors"))
        self.e_brake_button.setText(_translate("DriverTestUI", "Emergency Brake"))
        self.announce_start_button.setText(_translate("DriverTestUI", "Start"))
        self.announce_stop_button.setText(_translate("DriverTestUI", "Stop"))
        self.label_8.setText(_translate("DriverTestUI", "Announce"))
        self.label_2.setText(_translate("DriverTestUI", "Speed(MPH)"))
        self.label_9.setText(_translate("DriverTestUI", "Temp(F)"))
        self.label_10.setText(_translate("DriverTestUI", "Test Input"))
        self.label_11.setText(_translate("DriverTestUI", "Current Speed(MPH)"))
        self.label_6.setText(_translate("DriverTestUI", "Suggested Speed(MPH)"))
        self.label_12.setText(_translate("DriverTestUI", "Test Output"))
        self.label_13.setText(_translate("DriverTestUI", "Kp"))
        self.label_14.setText(_translate("DriverTestUI", "Ki"))
        self.label_15.setText(_translate("DriverTestUI", "Suggested Speed(MPH)"))
        self.label_5.setText(_translate("DriverTestUI", "Next Station"))
        item = self.nextStationTable.verticalHeaderItem(0)
        item.setText(_translate("DriverTestUI", "Herron Ave"))
        item = self.nextStationTable.verticalHeaderItem(1)
        item.setText(_translate("DriverTestUI", "Swissvale"))
        item = self.nextStationTable.verticalHeaderItem(2)
        item.setText(_translate("DriverTestUI", "Penn Station"))
        item = self.nextStationTable.verticalHeaderItem(3)
        item.setText(_translate("DriverTestUI", "Steel Plaza"))
        item = self.nextStationTable.verticalHeaderItem(4)
        item.setText(_translate("DriverTestUI", "First Ave"))
        item = self.nextStationTable.verticalHeaderItem(5)
        item.setText(_translate("DriverTestUI", "Station Square"))
        item = self.nextStationTable.verticalHeaderItem(6)
        item.setText(_translate("DriverTestUI", "South Hills Junction"))
        item = self.nextStationTable.horizontalHeaderItem(0)
        item.setText(_translate("DriverTestUI", "Index"))
        __sortingEnabled = self.nextStationTable.isSortingEnabled()
        self.nextStationTable.setSortingEnabled(False)
        item = self.nextStationTable.item(0, 0)
        item.setText(_translate("DriverTestUI", "0"))
        item = self.nextStationTable.item(1, 0)
        item.setText(_translate("DriverTestUI", "1"))
        item = self.nextStationTable.item(2, 0)
        item.setText(_translate("DriverTestUI", "2"))
        item = self.nextStationTable.item(3, 0)
        item.setText(_translate("DriverTestUI", "3"))
        item = self.nextStationTable.item(4, 0)
        item.setText(_translate("DriverTestUI", "4"))
        item = self.nextStationTable.item(5, 0)
        item.setText(_translate("DriverTestUI", "5"))
        item = self.nextStationTable.item(6, 0)
        item.setText(_translate("DriverTestUI", "6"))
        self.nextStationTable.setSortingEnabled(__sortingEnabled)
        self.label_16.setText(_translate("DriverTestUI", "Authority(Mi)"))
        self.serviceBrake_button.setText(_translate("DriverTestUI", "Service Brake"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DriverTestUI = QtWidgets.QMainWindow()
    ui = Ui_DriverTestUI()
    ui.setupUi(DriverTestUI)
    DriverTestUI.show()
    sys.exit(app.exec_())
