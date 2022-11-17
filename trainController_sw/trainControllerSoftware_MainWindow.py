# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trainControllerSoftware_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from functools import partial
from trainControllerSoftware_TestSecondWindow import Ui_Test_SecondWindow
from manualControl import ManualControl
from Control import Control
from simple_pid import PID
from signalSender import signalSender


class Ui_TrainControllerSW_MainWindow(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        self.setupUi()
        self.timer = QtCore.QTimer()
        #self.connect()
        #self.ManualControl_Connect()
        
        self.show()
        

    def setupUi(self):
        ##
        self.c = Control()
        self.mc = ManualControl()
        self.internal_light_state = True        
        self.external_light_state = True
        self.left_door_state = False
        self.right_door_state = False
        self.announce_state = False
        self.advertisement_state = False
        self.service_brake = False
        self.emergency_brake = False
        self.temperature = 72
        self.speed_display_value = 0
        self.power_failure_value = 0
        
        ## Variables for incoming data
        self.authority = 0
        self.current_speed = 0
        self.nextStation = "Station"
        
        ## Initialize PID
        self.commanded_speed = 30 / 2.23694 # commanded speed input as mph
        self.kp = 24000
        self.ki = 100
        self.pid = PID(self.kp, self.ki, 0, setpoint=self.commanded_speed)
        self.pid.output_limits = (0, 120000) #clamp at 120W
        
        self.setObjectName("self")
        self.resize(835, 423)
        self.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(545, 170, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.currentSpeed_lcdDisplay = QtWidgets.QLCDNumber(self.centralwidget)
        self.currentSpeed_lcdDisplay.setGeometry(QtCore.QRect(740, 30, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.currentSpeed_lcdDisplay.setFont(font)
        self.currentSpeed_lcdDisplay.setObjectName("currentSpeed_lcdDisplay")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1360, 20, 71, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.TabWigets = QtWidgets.QTabWidget(self.centralwidget)
        self.TabWigets.setGeometry(QtCore.QRect(20, 10, 521, 381))
        self.TabWigets.setObjectName("TabWigets")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.ManualMode_GroupBox = QtWidgets.QGroupBox(self.tab)
        self.ManualMode_GroupBox.setGeometry(QtCore.QRect(10, 10, 501, 321))
        self.ManualMode_GroupBox.setObjectName("ManualMode_GroupBox")
        self.VitalControlFrame_2 = QtWidgets.QFrame(self.ManualMode_GroupBox)
        self.VitalControlFrame_2.setGeometry(QtCore.QRect(20, 30, 201, 271))
        self.VitalControlFrame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.VitalControlFrame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.VitalControlFrame_2.setObjectName("VitalControlFrame_2")
        self.label_11 = QtWidgets.QLabel(self.VitalControlFrame_2)
        self.label_11.setGeometry(QtCore.QRect(0, 0, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.Auto_SpeedDisplay = QtWidgets.QLCDNumber(self.VitalControlFrame_2)
        self.Auto_SpeedDisplay.setGeometry(QtCore.QRect(110, 50, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Auto_SpeedDisplay.setFont(font)
        self.Auto_SpeedDisplay.setObjectName("Auto_SpeedDisplay")
        self.label_13 = QtWidgets.QLabel(self.VitalControlFrame_2)
        self.label_13.setGeometry(QtCore.QRect(10, 50, 91, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.VitalControlFrame_2)
        self.label_14.setGeometry(QtCore.QRect(10, 150, 91, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.Auto_CommandedSpeedDisplay = QtWidgets.QLCDNumber(self.VitalControlFrame_2)
        self.Auto_CommandedSpeedDisplay.setGeometry(QtCore.QRect(110, 100, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Auto_CommandedSpeedDisplay.setFont(font)
        self.Auto_CommandedSpeedDisplay.setObjectName("Auto_CommandedSpeedDisplay")
        self.Auto_BrakingDisplay = QtWidgets.QLCDNumber(self.VitalControlFrame_2)
        self.Auto_BrakingDisplay.setGeometry(QtCore.QRect(110, 150, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Auto_BrakingDisplay.setFont(font)
        self.Auto_BrakingDisplay.setObjectName("Auto_BrakingDisplay")
        self.label_15 = QtWidgets.QLabel(self.ManualMode_GroupBox)
        self.label_15.setGeometry(QtCore.QRect(30, 130, 101, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_15.setFont(font)
        self.label_15.setWordWrap(True)
        self.label_15.setObjectName("label_15")
        self.VitalControlFrame = QtWidgets.QFrame(self.ManualMode_GroupBox)
        self.VitalControlFrame.setGeometry(QtCore.QRect(250, 30, 231, 271))
        self.VitalControlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.VitalControlFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.VitalControlFrame.setObjectName("VitalControlFrame")
        self.label_16 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_16.setGeometry(QtCore.QRect(-10, 0, 251, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_18 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_18.setGeometry(QtCore.QRect(10, 70, 101, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.Temperature_DisplayBox = QtWidgets.QLCDNumber(self.VitalControlFrame)
        self.Temperature_DisplayBox.setGeometry(QtCore.QRect(130, 230, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Temperature_DisplayBox.setFont(font)
        self.Temperature_DisplayBox.setObjectName("Temperature_DisplayBox")
        self.label_20 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_20.setGeometry(QtCore.QRect(10, 100, 101, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.InternalLights_DisplayBox = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.InternalLights_DisplayBox.setGeometry(QtCore.QRect(180, 50, 31, 24))
        self.InternalLights_DisplayBox.setText("")
        self.InternalLights_DisplayBox.setObjectName("InternalLights_DisplayBox")
        self.InternalLights_DisplayCheck_3 = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.InternalLights_DisplayCheck_3.setGeometry(QtCore.QRect(320, 70, 31, 24))
        self.InternalLights_DisplayCheck_3.setText("")
        self.InternalLights_DisplayCheck_3.setObjectName("InternalLights_DisplayCheck_3")
        self.label_19 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_19.setGeometry(QtCore.QRect(10, 40, 101, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_21 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_21.setGeometry(QtCore.QRect(10, 130, 101, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.ExternalLights_DisplayBox = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.ExternalLights_DisplayBox.setGeometry(QtCore.QRect(180, 80, 31, 24))
        self.ExternalLights_DisplayBox.setText("")
        self.ExternalLights_DisplayBox.setObjectName("ExternalLights_DisplayBox")
        self.LeftDoors_DisplayBox = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.LeftDoors_DisplayBox.setGeometry(QtCore.QRect(180, 110, 31, 24))
        self.LeftDoors_DisplayBox.setText("")
        self.LeftDoors_DisplayBox.setObjectName("LeftDoors_DisplayBox")
        self.RightDoors_DisplayBox = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.RightDoors_DisplayBox.setGeometry(QtCore.QRect(180, 140, 31, 24))
        self.RightDoors_DisplayBox.setText("")
        self.RightDoors_DisplayBox.setObjectName("RightDoors_DisplayBox")
        self.Advertisements_DisplayBox = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.Advertisements_DisplayBox.setGeometry(QtCore.QRect(180, 170, 31, 24))
        self.Advertisements_DisplayBox.setText("")
        self.Advertisements_DisplayBox.setObjectName("Advertisements_DisplayBox")
        self.Announcements_DisplayBox = QtWidgets.QCheckBox(self.VitalControlFrame)
        self.Announcements_DisplayBox.setGeometry(QtCore.QRect(180, 200, 31, 24))
        self.Announcements_DisplayBox.setText("")
        self.Announcements_DisplayBox.setObjectName("Announcements_DisplayBox")
        self.label_22 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_22.setGeometry(QtCore.QRect(10, 160, 111, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_24 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_24.setGeometry(QtCore.QRect(10, 190, 111, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.label_23 = QtWidgets.QLabel(self.VitalControlFrame)
        self.label_23.setGeometry(QtCore.QRect(10, 220, 111, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.TabWigets.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.Manual_Frame = QtWidgets.QGroupBox(self.tab_2)
        self.Manual_Frame.setGeometry(QtCore.QRect(10, 10, 471, 321))
        self.Manual_Frame.setObjectName("Manual_Frame")
        self.Manual_Advertisements_CheckBox = QtWidgets.QCheckBox(self.Manual_Frame)
        self.Manual_Advertisements_CheckBox.setGeometry(QtCore.QRect(390, 150, 61, 23))
        self.Manual_Advertisements_CheckBox.setObjectName("Manual_Advertisements_CheckBox")
        self.label_10 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_10.setGeometry(QtCore.QRect(150, 100, 91, 41))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.speed_Slider = QtWidgets.QSlider(self.Manual_Frame)
        self.speed_Slider.setGeometry(QtCore.QRect(20, 80, 121, 22))
        self.speed_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.speed_Slider.setObjectName("speed_Slider")
        self.speed_Slider.setMaximum(70);
        self.label_3 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_3.setGeometry(QtCore.QRect(240, 70, 67, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.Manual_Annoucements_CheckBox = QtWidgets.QCheckBox(self.Manual_Frame)
        self.Manual_Annoucements_CheckBox.setGeometry(QtCore.QRect(390, 180, 61, 23))
        self.Manual_Annoucements_CheckBox.setObjectName("Manual_Annoucements_CheckBox")
        self.Manual_temperature_box = QtWidgets.QDoubleSpinBox(self.Manual_Frame)
        self.Manual_temperature_box.setGeometry(QtCore.QRect(360, 30, 91, 32))
        self.Manual_temperature_box.setMinimum(0.0)
        self.Manual_temperature_box.setMaximum(90.0)
        self.Manual_temperature_box.setProperty("value", 0.0)
        self.Manual_temperature_box.setObjectName("Manual_temperature_box")
        self.braking_Slider = QtWidgets.QSlider(self.Manual_Frame)
        self.braking_Slider.setGeometry(QtCore.QRect(20, 150, 121, 22))
        self.braking_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.braking_Slider.setObjectName("braking_Slider")
        self.braking_Slider.setMaximum(1)
        self.Manual_Braking_lcdDisplay = QtWidgets.QLCDNumber(self.Manual_Frame)
        self.Manual_Braking_lcdDisplay.setGeometry(QtCore.QRect(150, 140, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Manual_Braking_lcdDisplay.setFont(font)
        self.Manual_Braking_lcdDisplay.setObjectName("Manual_Braking_lcdDisplay")
        self.Manual_CommandedSpeed_lcdDisplay = QtWidgets.QLCDNumber(self.Manual_Frame)
        self.Manual_CommandedSpeed_lcdDisplay.setGeometry(QtCore.QRect(150, 60, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Manual_CommandedSpeed_lcdDisplay.setFont(font)
        self.Manual_CommandedSpeed_lcdDisplay.setObjectName("Manual_CommandedSpeed_lcdDisplay")
        self.line = QtWidgets.QFrame(self.Manual_Frame)
        self.line.setGeometry(QtCore.QRect(230, 30, 20, 271))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.Manual_lights_ComboBox = QtWidgets.QComboBox(self.Manual_Frame)
        self.Manual_lights_ComboBox.setGeometry(QtCore.QRect(360, 70, 91, 26))
        self.Manual_lights_ComboBox.setObjectName("Manual_lights_ComboBox")
        self.Manual_lights_ComboBox.addItem("")
        self.Manual_lights_ComboBox.addItem("")
        self.Manual_lights_ComboBox.addItem("")
        self.Manual_lights_ComboBox.addItem("")
        self.Manual_doors_ComboBox = QtWidgets.QComboBox(self.Manual_Frame)
        self.Manual_doors_ComboBox.setGeometry(QtCore.QRect(360, 110, 91, 26))
        self.Manual_doors_ComboBox.setObjectName("Manual_doors_ComboBox")
        self.Manual_doors_ComboBox.addItem("")
        self.Manual_doors_ComboBox.addItem("")
        self.Manual_doors_ComboBox.addItem("")
        self.Manual_doors_ComboBox.addItem("")
        self.label_4 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_4.setGeometry(QtCore.QRect(240, 110, 67, 17))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_8.setGeometry(QtCore.QRect(240, 180, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_2 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_2.setGeometry(QtCore.QRect(80, 20, 161, 41))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_12 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_12.setGeometry(QtCore.QRect(240, 150, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_9 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_9.setGeometry(QtCore.QRect(240, 30, 111, 22))
        font = QtGui.QFont()
        font.setBold(True)
        font.setKerning(False)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.ManuLebrake_button = QtWidgets.QPushButton(self.Manual_Frame)
        self.ManuLebrake_button.setGeometry(QtCore.QRect(50, 200, 141, 91))
        font = QtGui.QFont()
        font.setBold(True)
        self.ManuLebrake_button.setFont(font)
        self.ManuLebrake_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ManuLebrake_button.setStyleSheet("background-color : red")
        self.ManuLebrake_button.setAutoFillBackground(False)
        self.ManuLebrake_button.setObjectName("ManuLebrake_button")
        self.label_6 = QtWidgets.QLabel(self.Manual_Frame)
        self.label_6.setGeometry(QtCore.QRect(510, 50, 161, 41))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.TabWigets.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.EngineerMode_Frame = QtWidgets.QGroupBox(self.tab_3)
        self.EngineerMode_Frame.setGeometry(QtCore.QRect(10, 10, 371, 80))
        self.EngineerMode_Frame.setObjectName("EngineerMode_Frame")
        self.label_31 = QtWidgets.QLabel(self.EngineerMode_Frame)
        self.label_31.setGeometry(QtCore.QRect(200, 40, 63, 20))
        self.label_31.setObjectName("label_31")       
        self.PowerOutput_lcdDisplay = QtWidgets.QLCDNumber(self.centralwidget)
        self.PowerOutput_lcdDisplay.setGeometry(QtCore.QRect(740, 130, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.PowerOutput_lcdDisplay.setFont(font)
        self.PowerOutput_lcdDisplay.setObjectName("PowerOutput_lcdDisplay")
        
        self.setKp_Box = QtWidgets.QDoubleSpinBox(self.EngineerMode_Frame)
        self.setKp_Box.setGeometry(QtCore.QRect(90, 30, 91, 32))
        self.setKp_Box.setMinimum(0.0)
        self.setKp_Box.setMaximum(90.0)
        self.setKp_Box.setProperty("value", 0.0)
        self.setKp_Box.setObjectName("setKp_Box")
        self.label = QtWidgets.QLabel(self.EngineerMode_Frame)
        self.label.setGeometry(QtCore.QRect(30, 40, 63, 20))
        self.label.setObjectName("label")
        self.setKi_Box = QtWidgets.QDoubleSpinBox(self.EngineerMode_Frame)
        self.setKi_Box.setGeometry(QtCore.QRect(250, 30, 91, 32))
        self.setKi_Box.setMinimum(00.0)
        self.setKi_Box.setMaximum(90.0)
        self.setKi_Box.setProperty("value", 0.0)
        self.setKi_Box.setObjectName("setKi_Box")
        self.TabWigets.addTab(self.tab_3, "")
        
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(540, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.Authority_lcdDisplay = QtWidgets.QLCDNumber(self.centralwidget)
        self.Authority_lcdDisplay.setGeometry(QtCore.QRect(740, 80, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Authority_lcdDisplay.setFont(font)
        self.Authority_lcdDisplay.setObjectName("Authority_lcdDisplay")
        self.faultsframe = QtWidgets.QFrame(self.centralwidget)
        self.faultsframe.setGeometry(QtCore.QRect(550, 230, 111, 161))
        self.faultsframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.faultsframe.setFrameShadow(QtWidgets.QFrame.Plain)
        self.faultsframe.setObjectName("faultsframe")
        self.label_7 = QtWidgets.QLabel(self.faultsframe)
        self.label_7.setGeometry(QtCore.QRect(0, -10, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_27 = QtWidgets.QLabel(self.faultsframe)
        self.label_27.setGeometry(QtCore.QRect(10, 20, 61, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.label_29 = QtWidgets.QLabel(self.faultsframe)
        self.label_29.setGeometry(QtCore.QRect(10, 50, 51, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.EngineFault_DisplayBox = QtWidgets.QCheckBox(self.faultsframe)
        self.EngineFault_DisplayBox.setGeometry(QtCore.QRect(80, 30, 31, 24))
        self.EngineFault_DisplayBox.setText("")
        self.EngineFault_DisplayBox.setCheckable(False)
        self.EngineFault_DisplayBox.setObjectName("EngineFault_DisplayBox")
        self.PowerFault_DisplayBox = QtWidgets.QCheckBox(self.faultsframe)
        self.PowerFault_DisplayBox.setGeometry(QtCore.QRect(80, 60, 31, 24))
        self.PowerFault_DisplayBox.setText("")
        self.PowerFault_DisplayBox.setCheckable(False)
        self.PowerFault_DisplayBox.setObjectName("PowerFault_DisplayBox")
        self.CircuitFault_DisplayBox = QtWidgets.QCheckBox(self.faultsframe)
        self.CircuitFault_DisplayBox.setGeometry(QtCore.QRect(80, 120, 21, 24))
        self.CircuitFault_DisplayBox.setText("")
        self.CircuitFault_DisplayBox.setCheckable(False)
        self.CircuitFault_DisplayBox.setObjectName("CircuitFault_DisplayBox")
        self.TrackFault_DisplayBox = QtWidgets.QCheckBox(self.faultsframe)
        self.TrackFault_DisplayBox.setGeometry(QtCore.QRect(80, 90, 31, 24))
        self.TrackFault_DisplayBox.setText("")
        self.TrackFault_DisplayBox.setCheckable(False)
        self.TrackFault_DisplayBox.setObjectName("TrackFault_DisplayBox")
        self.label_28 = QtWidgets.QLabel(self.faultsframe)
        self.label_28.setGeometry(QtCore.QRect(10, 80, 61, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.label_30 = QtWidgets.QLabel(self.faultsframe)
        self.label_30.setGeometry(QtCore.QRect(10, 110, 51, 41))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.next_station_label = QtWidgets.QLabel(self.centralwidget)
        self.next_station_label.setGeometry(QtCore.QRect(740, 170, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(False)
        self.next_station_label.setFont(font)
        self.next_station_label.setAutoFillBackground(False)
        self.next_station_label.setWordWrap(True)
        self.next_station_label.setObjectName("next_station_label")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(540, 30, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(545, 125, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        
        font = QtGui.QFont()
        font.setBold(True)
        
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(700, 230, 111, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.EmergencyBrakeDisplayBox = QtWidgets.QCheckBox(self.frame)
        self.EmergencyBrakeDisplayBox.setGeometry(QtCore.QRect(50, 30, 60, 60))
        self.EmergencyBrakeDisplayBox.setText("")
        self.EmergencyBrakeDisplayBox.setCheckable(True)
        self.EmergencyBrakeDisplayBox.setObjectName("EmergencyBrakeDisplayBox")
        self.label_33 = QtWidgets.QLabel(self.frame)
        self.label_33.setGeometry(QtCore.QRect(10, 0, 95, 50))
        self.label_33.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.label_33.setFont(font)
        self.label_33.setWordWrap(True)
        self.label_33.setObjectName("label_33")
        
        self.Manual_lights_ComboBox.setCurrentIndex(3)
        self.Manual_doors_ComboBox.setCurrentIndex(0)
        self.Manual_temperature_box.setValue(self.temperature)
        
        ##
        self.speed_Slider.valueChanged.connect(self.setManualControl_CommandedSpeed)
        self.braking_Slider.valueChanged.connect(self.setManualControl_ServiceBrake)
        self.ManuLebrake_button.clicked.connect(self.setManualControl_EmergencyBrake)
        self.Manual_temperature_box.valueChanged.connect(self.setManualControl_Temperature)
        self.Manual_lights_ComboBox.currentIndexChanged.connect(self.setManualControl_Lights)
        self.Manual_doors_ComboBox.currentIndexChanged.connect(self.setManualControl_Doors)
        self.Manual_Advertisements_CheckBox.stateChanged.connect(self.setManualControl_Advertisements)
        self.Manual_Annoucements_CheckBox.stateChanged.connect(self.setManualControl_Announcements)
        ##
        
        ## Inputs from Train Model
        self.signals.currentSpeedOfTrainModel.connect(self.setPID)
        
        ##
                
        self.retranslateUi()
        self.TabWigets.setCurrentIndex(2)
        self.speed_Slider.valueChanged['int'].connect(self.Manual_CommandedSpeed_lcdDisplay.display)
        self.Manual_temperature_box.valueChanged['double'].connect(self.Manual_temperature_box.setValue)
        self.braking_Slider.valueChanged['int'].connect(self.Manual_Braking_lcdDisplay.display)
        QtCore.QMetaObject.connectSlotsByName(self)
                
        self.powerDict = {
                'power' : self.PowerOutput_lcdDisplay.value()
                }
        self.vitalDict = {
            'serviceBrake' : self.service_brake,
            'emergencyBrake' : self.emergency_brake,
            'commandedSpeed' : self.commanded_speed
        }
        self.nonVitalDict = {
            'int_lights' : self.internal_light_state,
            'ext_lights' : self.external_light_state,
            'temperature' : self.temperature,
            'left_doors' : self.left_door_state,
            'right_doors' : self.right_door_state,
            'announce_state' : self.announce_state,
            'advertisement_state' : self.advertisement_state,
        }

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "MainWindow"))
        self.label_5.setText(_translate("self", "Next Station:"))
        self.pushButton.setText(_translate("self", "I/0"))
        self.ManualMode_GroupBox.setTitle(_translate("self", "Automatic Mode"))
        self.label_11.setText(_translate("self", "Vital Controls"))
        self.label_13.setText(_translate("self", "Speed(MPH)"))
        self.label_14.setText(_translate("self", "Braking"))
        self.label_15.setText(_translate("self", "Commanded Speed(MPH)"))
        self.label_16.setText(_translate("self", "Non-Vital Controls"))
        self.label_18.setText(_translate("self", "External Lights"))
        self.label_20.setText(_translate("self", "Left Doors"))
        self.label_19.setText(_translate("self", "Internal Lights"))
        self.label_21.setText(_translate("self", "Right Doors"))
        self.label_22.setText(_translate("self", "Advertisements"))
        self.label_24.setText(_translate("self", "Announcements"))
        self.label_23.setText(_translate("self", "Temperature (F)"))
        self.TabWigets.setTabText(self.TabWigets.indexOf(self.tab), _translate("self", "Automatic Mode"))
        self.Manual_Frame.setTitle(_translate("self", "Manual Mode"))
        self.Manual_Advertisements_CheckBox.setText(_translate("self", "On/Off"))
        self.label_10.setText(_translate("self", "Braking"))
        self.label_3.setText(_translate("self", "Lights"))
        self.Manual_Annoucements_CheckBox.setText(_translate("self", "On/Off"))
        self.Manual_lights_ComboBox.setItemText(0, _translate("self", "Off"))
        self.Manual_lights_ComboBox.setItemText(1, _translate("self", "Internal"))
        self.Manual_lights_ComboBox.setItemText(2, _translate("self", "External"))
        self.Manual_lights_ComboBox.setItemText(3, _translate("self", "Both"))
        self.Manual_doors_ComboBox.setItemText(0, _translate("self", "Closed"))
        self.Manual_doors_ComboBox.setItemText(1, _translate("self", "Left"))
        self.Manual_doors_ComboBox.setItemText(2, _translate("self", "Right"))
        self.Manual_doors_ComboBox.setItemText(3, _translate("self", "Both"))
        self.label_4.setText(_translate("self", "Doors"))
        self.label_8.setText(_translate("self", "Announcements"))
        self.label_2.setText(_translate("self", "Commanded Speed(MPH)"))
        self.label_12.setText(_translate("self", "Advertisements"))
        self.label_9.setText(_translate("self", "Temperature(F)"))
        self.ManuLebrake_button.setText(_translate("self", "Emergency Brake"))
        self.label_6.setText(_translate("self", "Commanded Speed(MPH)"))
        self.TabWigets.setTabText(self.TabWigets.indexOf(self.tab_2), _translate("self", "Manual/Driver Mode"))
        self.EngineerMode_Frame.setTitle(_translate("self", "Engineer Mode"))
        self.label_31.setText(_translate("self", "Set Ki:"))
        self.label.setText(_translate("self", "Set Kp:"))
        self.TabWigets.setTabText(self.TabWigets.indexOf(self.tab_3), _translate("self", "Engineer Mode"))
        self.label_17.setText(_translate("self", "Authority (miles):"))
        self.label_7.setText(_translate("self", "Faults"))
        self.label_27.setText(_translate("self", "Engine"))
        self.label_29.setText(_translate("self", "Power"))
        self.label_28.setText(_translate("self", "Track"))
        self.label_30.setText(_translate("self", "Circuit"))
        self.next_station_label.setText(_translate("self", "Station Square"))
        self.label_25.setText(_translate("self", "Current Speed(mph):"))
        self.label_26.setText(_translate("self", "Power (hp):"))
        self.label_33.setText(_translate("self", "Emergency Brake"))

        
    def EmergencyBrakeDisplay(self):
        self.EmergencyBrakeDisplayBox.setCheckable(True)
    
    def CurrentSpeed(self, pValue):
        #self.milesValue = pValue * 0.621371
        self.currentSpeed_lcdDisplay.display(self.c.getCurrentSpeed())
    
    def NextStation(self, pValue):
        #self.next_station_label.setText(self.c.getNextStation)
        pass

####### ManualControl Class Sets
    def setManualControl_CommandedSpeed(self):
        self.commanded_speed = (self.speed_Slider.value() / 2.23694)      
        
    def setManualControl_ServiceBrake(self):
        self.service_brake = self.braking_Slider.value()
        self.signals.serviceBrakeSignal.emit(self.service_brake)
    
    def setManualControl_EmergencyBrake(self):
        # if E brake is already set and the button is clicked, then it turns off the e brake
        if(self.EmergencyBrakeDisplayBox.isChecked() == True):
            self.EmergencyBrakeDisplayBox.setCheckState(False)           
            self.emergency_brake = False
            self.signals.emergencyBrakeSignal.emit(False)

        elif(self.EmergencyBrakeDisplayBox.isChecked() == False):
            self.currentSpeed_lcdDisplay.display(0)
            self.speed_Slider.setValue(0)
            self.EmergencyBrakeDisplayBox.setCheckState(True)
            self.emergency_brake = True
            self.signals.emergencyBrakeSignal.emit(True)
        
    def setManualControl_Temperature(self):
        self.temperature = self.Manual_temperature_box.value()
        self.emitNonVital() 
    
    def setManualControl_Lights(self):
        if(self.Manual_lights_ComboBox.currentIndex() == 0):
            self.internal_light_state = False
            self.external_light_state = False
        elif(self.Manual_lights_ComboBox.currentIndex() == 1):
            self.internal_light_state = True
            self.external_light_state = False
        elif(self.Manual_lights_ComboBox.currentIndex() == 2):
            self.internal_light_state = False
            self.external_light_state = True
        elif(self.Manual_lights_ComboBox.currentIndex() == 3):
            self.internal_light_state = True
            self.external_light_state = True    
        self.emitNonVital()           
    
    def setManualControl_Doors(self):
        if(self.Manual_doors_ComboBox.currentIndex() == 0):
            self.left_door_state = False
            self.right_door_state = False
        elif(self.Manual_doors_ComboBox.currentIndex() == 1):
            self.left_door_state = True
            self.right_door_state = False
        elif(self.Manual_doors_ComboBox.currentIndex() == 2):
            self.left_door_state = False
            self.right_door_state = True
        elif(self.Manual_doors_ComboBox.currentIndex() == 3):
            self.left_door_state = True
            self.right_door_state = True
        self.emitNonVital() 
    
    def setManualControl_Advertisements(self):
        self.advertisement_state = self.Manual_Advertisements_CheckBox.checkState()

    def setManualControl_Announcements(self):
        self.announce_state = self.Manual_Annoucements_CheckBox.checkState()

    # Power and Ebrake
    def ActivateEmergencyBrake(self):
        if(self.EmergencyBrakeDisplayBox.isChecked() == True):
            self.EmergencyBrakeDisplayBox.setCheckState(False)
            self.emergency_brake = False
        elif(self.EmergencyBrakeDisplayBox.isChecked() == False):
            self.emergency_brake = True
            self.currentSpeed_lcdDisplay.display(0)
            self.speed_Slider.setValue(0)
            self.EmergencyBrakeDisplayBox.setCheckState(True)
            
    def setKpValue(self):
        self.kp = self.setKp_Box.value()
    
    def setKiValue(self):
        self.ki = self.setKi_Box.value()
        
    def setPID(self, msg):
        # Km/hr to mph
        # msg input as m/s
        # msg = current speed
        self.current_speed = msg
        if((self.EmergencyBrakeDisplayBox.isChecked() == True) or (msg >= self.commanded_speed) or (self.service_brake == 1)):
            self.power = 0
            self.powerDict['power'] = self.power
        else:
            self.pid.setpoint = self.commanded_speed
            self.power = self.pid(msg)
            self.pid.output_limits = (0, 120000)
            self.powerDict['power'] = self.power
        self.currentSpeed_lcdDisplay.display(msg * 2.23694)
        self.PowerOutput_lcdDisplay.display((self.power/1000)*1.34102) #horsepower
        self.emitPower()
    
    # Signals Functions
    def setAuthority(self, msg):
        self.authority = msg
        self.Authority_lcdDisplay.display(self.authority) #need to convert from ? to miles
        if(self.authority <= 2):
            self.signals.serviceBrakeSignal.emit(True) #its a list in the signals class
            self.waitUntilStopped()          
    
    def waitUntilStopped(self):
        while(self.current_speed != 0):
            time.sleep(0.001)
            self.signals.serviceBrakeSignal.emit(True)
        else:
            #wait 30 seconds at station
            time.sleep(30) 
            self.signals.serviceBrakeSignal.emit(False)

    def emitPower(self):
        self.signals.powerSignal.emit(self.powerDict)     
            
    def emitNonVital(self):
        self.nonVitalDict['temperature'] = self.temperature
        self.nonVitalDict['int_lights'] = self.internal_light_state  
        self.nonVitalDict['ext_lights'] = self.external_light_state
        self.nonVitalDict['left_doors'] = self.left_door_state
        self.nonVitalDict['right_doors'] = self.right_door_state
        self.signals.nonVitalDictSignal.emit(self.nonVitalDict) 
 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_TrainControllerSW_MainWindow()
    
    sys.exit(app.exec_())