#!/usr/bin/env python3

##############################################################################
# AUTHOR(S):    Morgan Visnesky, Garrett Marcinak
# DATE:         11/13/2022
# FILENAME:     occupancySignalSender.py
# DESCRIPTION:
#   Used to hold all signals used for inter-module communications in the 
#   Pittsburgh Light Rail Track System
##############################################################################

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget

class Signals(QWidget):
    # Track Message Signals
    trackModelLayoutLoadedSignal = QtCore.pyqtSignal(list) # Lets other modules know that the TrackLayout has been successfully loaded
    occupancySignal              = QtCore.pyqtSignal(list) # List of booleans, length of a single trackline
    switchStatesSignal           = QtCore.pyqtSignal(list) # List of integers, length of a single trackline
    maintenanceSignal            = QtCore.pyqtSignal(list) # List of booleans, length of a single trackline
    trackFailuresSignal          = QtCore.pyqtSignal(list) # List of booleans, length of a single trackline
    lineSignal                   = QtCore.pyqtSignal(str)  # String Name of trackline
    # Above could be a single list signal formatted as below: 
    # ["TrackLineName", [lineOccupancy], [lineSwitchStates], [lineMaintenance], [lineFailures]]


    # CTC Office Signals
    dispatchTrainSignal      = QtCore.pyqtSignal(list)
    suggestedSpeedSignal     = QtCore.pyqtSignal(list)

    # Train Model Signals
    blockListSignal          = QtCore.pyqtSignal(list)
    blockLengthSignal        = QtCore.pyqtSignal(list)
    gradeSignal              = QtCore.pyqtSignal(list)

    # Wayside Controller Signals

    # Train Controller (SW) Inputs Signals
    authoritySignal          = QtCore.pyqtSignal(list)
    commandedSpeedSignal     = QtCore.pyqtSignal(list)
    speedLimitSignal         = QtCore.pyqtSignal(list)
    trainFailuresSignal      = QtCore.pyqtSignal(list)
    beaconSignal             = QtCore.pyqtSignal(list)        # Next Station and Station Side
    infrastructureSignal     = QtCore.pyqtSignal(list)        # Underground
    currentSpeedOfTrainModel = QtCore.pyqtSignal(list)
    
    # Train Controller (SW) Ouputs to Train Model Signals
    powerSignal              = QtCore.pyqtSignal(list)
    lightSignal              = QtCore.pyqtSignal(list)
    doorSignal               = QtCore.pyqtSignal(list)
    temperatureSignal        = QtCore.pyqtSignal(list)
    announcementsSignal      = QtCore.pyqtSignal(list)
    advertisementsSignals    = QtCore.pyqtSignal(list)
    serviceBrakeSignal       = QtCore.pyqtSignal(list)
    emergencyBrakeSignal     = QtCore.pyqtSignal(list)

    # Train Controller (HW) Signals




