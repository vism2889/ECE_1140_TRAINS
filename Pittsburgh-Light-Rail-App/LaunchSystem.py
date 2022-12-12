#!/usr/bin/env python3

##############################################################################
# AUTHOR(S):   Morgan Visnesky, ADD YOUR NAMES HERE
# DATE:     11/13/2022
# FILENAME: LaunchSystem.py
# DESCRIPTION:
#   Launches all modules for the Pittsburgh Light Rail Software System
##############################################################################

# PyQt IMPORTS
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Python IMPORTS
import sys
import os
import signal

# Signal IMPORTS
sys.path.append("../SystemSignals")
from Signals import Signals

# CTC Office IMPORTS
sys.path.append("../CTC-Office/full-functionality")
sys.path.append("../CTC-Office/train-functionality")
sys.path.append("../CTC-Office/block-functionality")
sys.path.append("../CTC-Office/schedule-functionality")
from CTCOffice import CTCOffice

# TrackModel IMPORTS
sys.path.append("../TrackModel/UI")
sys.path.append("../TrackModel/Parsers")
sys.path.append("../TrackModel/Track-System-Models")
sys.path.append("../TrackModel/images")
from TrackModelApp import TrackModel

# Wayside IMPORTS
sys.path.append("WaysideController")
sys.path.append("WaysideController/track_layout/")
from WaysideController import WaysideController

# TrainModel IMPORTS
sys.path.append("../train_model")
from trainmodel_ui import TrainModel

# Train Controller IMPORTS
sys.path.append("../trainController_sw/")
from trainControllerSoftware_MainWindow import Ui_TrainControllerSW_MainWindow

class PittsburghLightRail(QWidget):
    def __init__(self, hw):
        super().__init__()
        self.signals    = Signals()
        self.trackModel = TrackModel(self.signals)
        self.CTCOffice  = CTCOffice(self.signals)

        ## Launch Wayside Controller
        self.waysideController = WaysideController(self.signals)

        if not hw:
            self.trainController = Ui_TrainControllerSW_MainWindow(self.signals)

        #train model
        file = f'{os.getcwd()}/train.ui'
        self.trainModel = TrainModel(file, hw, self.signals)
        self.globalOcc = []
        self.signals.timeSignal.connect(self.showTime)
        self.setupUi()

    def setupUi(self):
        self.setGeometry(1630,50,220,330)
        self.setStyleSheet("background-color: #747c8a;")

        font = QFont()
        font.setPointSize(16)
        self.clockLabel = QLabel(self)
        self.clockLabel.setGeometry(QRect(60, 40, 100, 25))
        self.clockLabel.setObjectName("clockLabel")
        self.clockLabel.setStyleSheet("background-color: #7b8fb0; border: 1px solid black")
        self.clockLabel.setAlignment(Qt.AlignCenter)
        self.clockLabel.setFont(font)

        ## Speed Control
        self.speedController = QSlider(Qt.Horizontal,self)
        self.speedController.setGeometry(50,10,120,20)
        self.speedController.setMinimum(1)
        self.speedController.setMaximum(20)
        self.speedController.valueChanged.connect(self.sendClockSpeed)

        ## CTC Offic3
        font.setPointSize(14)
        self.showCTCButton = QPushButton(self)
        self.showCTCButton.setGeometry(35,70,150,25)
        self.showCTCButton.setStyleSheet("background-color: #e8c33c; ")
        self.showCTCButton.clicked.connect(self.CTCOffice.show)
        self.showCTCButton.setText("CTC Office")
        self.showCTCButton.setFont(font)

        ## Wayside Controller
        self.showWaysideControllerButton = QPushButton(self)
        self.showWaysideControllerButton.setGeometry(35,100,150,25)
        self.showWaysideControllerButton.setStyleSheet("background-color: #e8c33c; ")
        self.showWaysideControllerButton.clicked.connect(self.waysideController.show)
        self.showWaysideControllerButton.setText("Track Controller")
        self.showWaysideControllerButton.setFont(font)

        ## Track Model
        self.showTrackModelButton = QPushButton(self)
        self.showTrackModelButton.setGeometry(35,130,150,25)
        self.showTrackModelButton.setStyleSheet("background-color: #e8c33c; ")
        self.showTrackModelButton.clicked.connect(self.trackModel.show)
        self.showTrackModelButton.setText("Track Model")
        self.showTrackModelButton.setFont(font)

        ## Train Model
        self.showTrainModelButton = QPushButton(self)
        self.showTrainModelButton.setGeometry(35,160,150,25)
        self.showTrainModelButton.setStyleSheet("background-color: #e8c33c; ")
        self.showTrainModelButton.clicked.connect(self.trainModel.show)
        self.showTrainModelButton.setText("Train Model")
        self.showTrainModelButton.setFont(font)

        ## Train Controller
        self.showTrainControllerButton = QPushButton(self)
        self.showTrainControllerButton.setGeometry(35,190,150,25)
        self.showTrainControllerButton.setStyleSheet("background-color: #e8c33c; ")
        self.showTrainControllerButton.clicked.connect(self.trainController.show)
        self.showTrainControllerButton.setText("Train Controller")
        self.showTrainControllerButton.setFont(font)

        ## Icons
        self.trainImage          = QLabel(self)
        self.pixmap              = QPixmap('TeamRollingStock.png')
        self.trainImage.setPixmap(self.pixmap)
        self.trainImage.setGeometry(0,220,250,110)

        self.rabbitImage         = QLabel(self)
        self.pixmap              = QPixmap('Rabbit.png')
        self.rabbitImage.setPixmap(self.pixmap)
        self.rabbitImage.setGeometry(175,5,30,30)

        self.turtleImage         = QLabel(self)
        self.pixmap              = QPixmap('Turtle.png')
        self.turtleImage.setPixmap(self.pixmap)
        self.turtleImage.setGeometry(10,5,35,35)

        self.show()

    def showTime(self, msg):
        hours = ('%02d' % int(msg[0]))
        mins = ('%02d' % int(msg[1]))
        secs = ('%02d' % int(msg[2]))
        self.clockLabel.setText(hours + ":" + mins + ":" + secs)

    def sendClockSpeed(self, msg):
        value = int(self.speedController.value())
        self.signals.clockSpeedSignal.emit(value)


## Commandline CTRL-C ##
def handler(signum, frame):
    print("CTRL-C was pressed")
    exit(1)

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        hardWare = True
    else:
        print('Hardware is False')
        hardWare = False

    app = QApplication(sys.argv)
    ex = PittsburghLightRail(hardWare)
    sys.exit(app.exec_())
