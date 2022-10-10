# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trainController_testUI_hw.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal
from trainController_hw import Control as c

class Ui_DriverTestUI(object):
    def __init__(self):
        c.__init__(c)

        self.lights_internal_state = False
        self.lights_external_state = False
        self.left_door_state = False
        self.right_door_state = False
        self.timer = QtCore.QTimer()
        
    def setupUi(self, DriverTestUI):
        DriverTestUI.setObjectName("DriverTestUI")
        DriverTestUI.resize(969, 600)
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
        self.e_brake_button.setGeometry(QtCore.QRect(730, 80, 131, 121))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.e_brake_button.setFont(font)
        self.e_brake_button.setAutoFillBackground(False)
        self.e_brake_button.setObjectName("e_brake_button")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(540, 470, 21, 23))
        self.checkBox.setText("")
        self.checkBox.setCheckable(True)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(540, 500, 21, 23))
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(690, 500, 21, 23))
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(690, 470, 21, 23))
        self.checkBox_4.setText("")
        self.checkBox_4.setObjectName("checkBox_4")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(340, -20, 31, 641))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(60, 210, 211, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.Engine_fault = QtWidgets.QCheckBox(self.centralwidget)
        self.Engine_fault.setGeometry(QtCore.QRect(120, 400, 121, 23))
        self.Engine_fault.setCheckable(False)
        self.Engine_fault.setObjectName("Engine_fault")
        self.Power_fault = QtWidgets.QCheckBox(self.centralwidget)
        self.Power_fault.setGeometry(QtCore.QRect(120, 430, 121, 23))
        self.Power_fault.setCheckable(False)
        self.Power_fault.setObjectName("Power_fault")
        self.track_fault = QtWidgets.QCheckBox(self.centralwidget)
        self.track_fault.setGeometry(QtCore.QRect(120, 460, 121, 23))
        self.track_fault.setCheckable(False)
        self.track_fault.setObjectName("track_fault")
        self.announce_start_button = QtWidgets.QPushButton(self.centralwidget)
        self.announce_start_button.setGeometry(QtCore.QRect(410, 470, 89, 25))
        self.announce_start_button.setObjectName("announce_start_button")
        self.announce_stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.announce_stop_button.setGeometry(QtCore.QRect(410, 500, 89, 25))
        self.announce_stop_button.setObjectName("announce_stop_button")
        self.checkBox_12 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_12.setGeometry(QtCore.QRect(380, 500, 21, 23))
        self.checkBox_12.setText("")
        self.checkBox_12.setObjectName("checkBox_12")
        self.checkBox_13 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_13.setGeometry(QtCore.QRect(380, 470, 21, 23))
        self.checkBox_13.setText("")
        self.checkBox_13.setObjectName("checkBox_13")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(410, 440, 81, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(400, 90, 91, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.speed_slider = QtWidgets.QSlider(self.centralwidget)
        self.speed_slider.setGeometry(QtCore.QRect(410, 200, 71, 201))
        self.speed_slider.setOrientation(QtCore.Qt.Vertical)
        self.speed_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.speed_slider.setObjectName("speed_slider")
        self.lcd_speed = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_speed.setGeometry(QtCore.QRect(400, 130, 91, 61))
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
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 240, 281, 51))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(5)
        self.frame.setMidLineWidth(5)
        self.frame.setObjectName("frame")
        self.next_station_label = QtWidgets.QLabel(self.frame)
        self.next_station_label.setGeometry(QtCore.QRect(7, 10, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.next_station_label.setFont(font)
        self.next_station_label.setAutoFillBackground(False)
        self.next_station_label.setObjectName("next_station_label")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(600, 30, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(110, 350, 111, 141))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(0, 0, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.power_button = QtWidgets.QPushButton(self.centralwidget)
        self.power_button.setGeometry(QtCore.QRect(850, 490, 71, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.power_button.setFont(font)
        self.power_button.setObjectName("power_button")
        self.lcd_curredSpeed = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_curredSpeed.setGeometry(QtCore.QRect(560, 130, 91, 61))
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
        self.lcd_suggested.setGeometry(QtCore.QRect(200, 130, 91, 61))
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
        self.frame_2.raise_()
        self.label.raise_()
        self.currentSpeed_slider.raise_()
        self.lcd_power.raise_()
        self.lights_internal_button.raise_()
        self.lights_external_button.raise_()
        self.doors_left_button.raise_()
        self.doors_right_button.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.e_brake_button.raise_()
        self.checkBox.raise_()
        self.checkBox_2.raise_()
        self.checkBox_3.raise_()
        self.checkBox_4.raise_()
        self.line.raise_()
        self.label_5.raise_()
        self.Engine_fault.raise_()
        self.Power_fault.raise_()
        self.track_fault.raise_()
        self.announce_start_button.raise_()
        self.announce_stop_button.raise_()
        self.checkBox_12.raise_()
        self.checkBox_13.raise_()
        self.label_8.raise_()
        self.label_2.raise_()
        self.speed_slider.raise_()
        self.lcd_speed.raise_()
        self.temperature_box.raise_()
        self.label_9.raise_()
        self.frame.raise_()
        self.label_10.raise_()
        self.power_button.raise_()
        self.lcd_curredSpeed.raise_()
        self.label_11.raise_()
        self.lcd_suggested.raise_()
        self.label_6.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.ki_spinBox.raise_()
        self.label_14.raise_()
        self.kp_spinBox.raise_()
        self.suggestedSpeed_spinBox.raise_()
        self.label_15.raise_()
        DriverTestUI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DriverTestUI)
        self.statusbar.setObjectName("statusbar")
        DriverTestUI.setStatusBar(self.statusbar)

        self.retranslateUi(DriverTestUI)
        self.speed_slider.valueChanged['int'].connect(self.lcd_speed.display)
        self.lights_internal_button.clicked.connect(self.checkBox.animateClick)
        self.lights_external_button.clicked.connect(self.checkBox_2.animateClick)
        self.announce_start_button.clicked.connect(self.checkBox_13.animateClick)
        self.announce_stop_button.clicked.connect(self.checkBox_12.animateClick)
        self.doors_left_button.clicked.connect(self.checkBox_4.animateClick)
        self.doors_right_button.clicked.connect(self.checkBox_3.toggle)
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
        self.label_5.setText(_translate("DriverTestUI", "Next Station"))
        self.Engine_fault.setText(_translate("DriverTestUI", "Engine"))
        self.Power_fault.setText(_translate("DriverTestUI", "Power"))
        self.track_fault.setText(_translate("DriverTestUI", "Track"))
        self.announce_start_button.setText(_translate("DriverTestUI", "Start"))
        self.announce_stop_button.setText(_translate("DriverTestUI", "Stop"))
        self.label_8.setText(_translate("DriverTestUI", "Announce"))
        self.label_2.setText(_translate("DriverTestUI", "Speed(MPH)"))
        self.label_9.setText(_translate("DriverTestUI", "Temp(F)"))
        self.next_station_label.setText(_translate("DriverTestUI", "Station Square"))
        self.label_10.setText(_translate("DriverTestUI", "Test Input"))
        self.label_7.setText(_translate("DriverTestUI", "Faults"))
        self.power_button.setText(_translate("DriverTestUI", "I/0"))
        self.label_11.setText(_translate("DriverTestUI", "Current Speed(MPH)"))
        self.label_6.setText(_translate("DriverTestUI", "Suggested Speed(MPH)"))
        self.label_12.setText(_translate("DriverTestUI", "Test Output"))
        self.label_13.setText(_translate("DriverTestUI", "Kp"))
        self.label_14.setText(_translate("DriverTestUI", "Ki"))
        self.label_15.setText(_translate("DriverTestUI", "Suggested Speed(MPH)"))

    def toggle_lights_internal(self):
        self.lights_internal_state = not self.lights_internal_state
        c.setInternalLights(self.lights_internal_state)

    def toggle_lights_external(self):
        self.lights_external_state = not self.lights_external_state
        c.setExternalLights(self.lights_external_state)

    def toggle_left_door(self):
        self.left_door_state = not self.left_door_state
        c.setLeftDoor(self.left_door_state)

    def toggle_right_door(self):
        self.right_door_state = not self.right_door_state
        c.setRightDoor(self.right_door_state)

    def setSpeed(self):
        c.setSpeed(c, self.speed_slider.value())

    def setCurrentSpeed(self):
        c.setCurrentSpeed(c, self.currentSpeed_slider.value())

    def setTemperature(self):
        c.setTemperature(c, self.temperature_box.value())

    def announceStation(self):
        c.announceStation(c, True)

    def stopAnnounce(self):
        c.announceStation(c, False)

    def deployEbrake(self):
        self.speed_slider.setValue(0)
        c.deployEbrake(c)

    def setSuggestedSpeed(self):
        suggested_speed = self.suggestedSpeed_spinBox.value()
        c.setSuggestedSpeed(c, suggested_speed)

    def limitSpeed(self):
        c.limitSpeed(c)
        self.speed_slider.setValue(c.getSpeed(c))
    
    def set_kp_ki(self):
        kp_val = self.kp_spinBox.value()
        ki_val = self.ki_spinBox.value()
        c.set_kp_ki(kp_val, ki_val, c)
        c.initializePID(c, kp_val, ki_val)
    
    def calculatePower(self):
        power = c.getPowerOutput(c)
        self.lcd_power.display(power)
        
    def connect(self, DriverTestUI):
        self.lights_internal_button.clicked.connect(self.toggle_lights_internal)
        self.lights_external_button.clicked.connect(self.toggle_lights_external)
        self.doors_left_button.clicked.connect(self.toggle_left_door)
        self.doors_right_button.clicked.connect(self.toggle_right_door)
        self.speed_slider.valueChanged['int'].connect(self.setSpeed)
        self.currentSpeed_slider.valueChanged['int'].connect(self.setCurrentSpeed)
        self.temperature_box.valueChanged['double'].connect(self.setTemperature)
        self.suggestedSpeed_spinBox.valueChanged.connect(self.setSuggestedSpeed)
        self.e_brake_button.clicked.connect(self.deployEbrake)
        self.timer.timeout.connect(self.limitSpeed)
        self.timer.timeout.connect(self.calculatePower)
        self.kp_spinBox.valueChanged.connect(self.set_kp_ki)
        self.ki_spinBox.valueChanged.connect(self.set_kp_ki)
        self.announce_start_button.clicked.connect(self.announceStation)
        self.announce_stop_button.clicked.connect(self.stopAnnounce)

        self.timer.start(100)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DriverTestUI = QtWidgets.QMainWindow()
    ui = Ui_DriverTestUI()
    ui.setupUi(DriverTestUI)
    ui.connect(DriverTestUI)
    DriverTestUI.show()
    sys.exit(app.exec_())