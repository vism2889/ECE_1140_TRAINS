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

sys.path.append("../train_model")
from trainmodel_ui import TrainModel


# Signal IMPORTS
sys.path.append("../SystemSignals") 
from Signals import Signals

# Train Controller IMPORTS
sys.path.append("../trainController_sw/")
from trainControllerSoftware_MainWindow import Ui_TrainControllerSW_MainWindow

class PittsburghLightRail():
    def __init__(self):
        self.signals    = Signals()
        self.trackModel = TrackModel(self.signals)
        self.CTCOffice = CTCOffice(self.signals)
        #self.trainController = Ui_TrainControllerSW_MainWindow(self.signals)

        #train model
        file = r"C:\Users\12159\Documents\GitHub\ECE_1140_TRAINS\train_model\train.ui"
        self.trainModel = TrainModel(file)
        

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PittsburghLightRail()
    sys.exit(app.exec_())
