##############################################################################
# AUTHOR:   Juin Sommer
# DATE:     11/17/2022
# FILENAME: driver_UI.py
# DESCRIPTION:
# Train Driver UI to display necessary information and driving code for 
# Control and ManualControl classes
##############################################################################

from PyQt5 import QtCore, QtGui, QtWidgets
from analoggaugewidget import AnalogGaugeWidget
from PyQt5.QtCore import pyqtSlot, QTimer, pyqtSignal
from control import Control
from manualControl import ManualControl
import threading

class Ui_MainWindow():
    def __init__(self):
        self.c = Control()
        self.mc = ManualControl(self.c)
        self.internal_light_state = False
        self.external_light_state = False
        self.left_door_state = False
        self.right_door_state = False
        self.station = 0
        self.current_speed = 0
        self.commanded_speed = 0
        self.timer = QtCore.QTimer()

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

        self.speedometer.value_max = 50
        self.speedometer.value_min = 0
        self.speedometer.gauge_color_inner_radius_factor = .9
        self.speedometer.set_NeedleColor(R=255, G=0, B=0)
        self.speedometer.set_DisplayValueColor(R=255, G=0, B=0)
        self.speedometer.set_ScaleValueColor(R=255, G=0, B=0)
        self.speedometer.set_CenterPointColor(R=255, G=0, B=0)

        self.powerGauge.value_max = 120e3/745.7
        self.powerGauge.value_min = 0
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AnalogGaugeWidget_Demo"))

    def toggle_lights_manual(self):
        self.mc.lightsButton()

    def toggle_doors_manual(self):
        self.mc.doorsButton()

    def deploy_ebrake_manual(self):
        self.mc.ebrake_button()

    def deploy_serviceBrake_manual(self):
        self.mc.setServiceBrake()

    def setSpeed_manual(self):
        self.mc.setCommandedSpeed()
    
    def calculatePower_manual(self):
        power = self.mc.calculatePower() / 745.7
        if power != None:
            self.powerGauge.update_value(power)

    def announce_manual(self):
        self.mc.announceButton(0)

    def setTemperature_manual(self):
        self.mc.setTemperature_manual()
    
    def checkFailures_manual(self):
        self.mc.checkFailures_manual()
         
    def setCurrentSpeed(self):
        self.current_speed = self.c.setCurrentSpeed()
        #self.c.getSpeedLimit()
        converted_speed = 2.3694 * self.current_speed
        self.speedometer.update_value(converted_speed)

    def setCommandedSpeed(self):
        self.c.setSpeed()

    def toggle_internal_lights(self):
        self.internal_light_state = not self.internal_light_state
        self.c.setInternalLights(self.internal_light_state)

    def toggle_external_lights(self):
        self.external_light_state = not self.external_light_state
        self.c.setExternalLights(self.external_light_state)

    def toggle_left_door(self):
        self.left_door_state = not self.left_door_state
        self.c.setLeftDoor(self.left_door_state)

    def toggle_right_door(self):
        self.right_door_state = not self.right_door_state
        self.c.setRightDoor(self.right_door_state)

    def deployEbrake(self):
        self.c.deployEbrake()

    def checkAuthority(self):
        self.c.checkAuthority()

    def setServiceBrake(self):
        self.c.deployServiceBrake(False)

    def calculatePower(self):
        self.c.getPowerOutput()

    def sendData(self):
        self.c.publish()

    def subscribe(self):
        self.c.subscribe()

    def sendRandom(self):
        self.c.sendRandom()
    
    def manual_connect(self, MainWindow):
        self.timer.timeout.connect(self.subscribe)
        self.timer.timeout.connect(self.checkFailures_manual)
        self.timer.timeout.connect(self.setSpeed_manual)
        self.timer.timeout.connect(self.setCurrentSpeed)
        self.timer.timeout.connect(self.checkAuthority)
        self.timer.timeout.connect(self.calculatePower_manual)
        self.timer.timeout.connect(self.setTemperature_manual)
        self.timer.timeout.connect(self.toggle_lights_manual)
        self.timer.timeout.connect(self.toggle_doors_manual)
        self.timer.timeout.connect(self.deploy_ebrake_manual)
        self.timer.timeout.connect(self.announce_manual)
        self.timer.timeout.connect(self.deploy_serviceBrake_manual)
        self.timer.timeout.connect(self.sendData)
        self.timer.start(10)

    def auto_connect(self, MainWindow):
        self.timer.timeout.connect(self.setCommandedSpeed)
        self.timer.timeout.connect(self.calculatePower)
        self.timer.timeout.connect(self.sendData)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.manual_connect(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
