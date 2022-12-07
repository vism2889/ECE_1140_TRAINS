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
from TrackModelApp import TrackModel

# Wayside IMPORTS
sys.path.append("WaysideController")
sys.path.append("WaysideController/track_layout")
from WaysideController import WaysideController

# TrainModel IMPORTS
sys.path.append("../train_model")
from trainmodel_ui import TrainModel

# Train Controller IMPORTS
sys.path.append("../trainController_sw/")
from trainControllerSoftware_MainWindow import Ui_TrainControllerSW_MainWindow

# Signal IMPORTS
sys.path.append("../SystemSignals")
from Signals import Signals
import sys

class PittsburghLightRail():
    def __init__(self, hw):
        self.signals    = Signals()
        self.trackModel = TrackModel(self.signals)
        self.CTCOffice = CTCOffice(self.signals)

        ## Launch Wayside Controller
        self.WaysideController = WaysideController(self.signals)

        if not hw:
            self.trainController = Ui_TrainControllerSW_MainWindow(self.signals)

        #train model
        file = f'{os.getcwd()}/train.ui'
        self.trainModel = TrainModel(file, hw, self.signals)
        self.globalOcc = []

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
