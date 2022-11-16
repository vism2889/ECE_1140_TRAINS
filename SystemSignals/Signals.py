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
    # Track Model Signals
    
    # List of length N where N is the number of blocks in the track
    ## Track Failure = 0x01, Circuit Failure = 0x02, Power Failure = 0x04 
    #   - any combination of the three should be logically OR'd together (i.e. TF + CF = 0x03)
    blockFailures                       = QtCore.pyqtSignal(list) 

    globalOccupancyFromTrackModelSignal = QtCore.pyqtSignal(list)
    trackModelLayoutLoadedSignal        = QtCore.pyqtSignal(list) # Lets other modules know that the TrackLayout has been successfully loaded
    occupancyFromTrainSignal            = QtCore.pyqtSignal(list) # List of booleans, length of a single trackline
    switchStatesSignal                  = QtCore.pyqtSignal(list) # List of integers, length of a single trackline
    maintenanceSignal                   = QtCore.pyqtSignal(list) # List of booleans, length of a single trackline
    trackFailuresSignal                 = QtCore.pyqtSignal(list) # List of booleans, length of a single trackline
    lineSignal                          = QtCore.pyqtSignal(str)  # String Name of trackline
          
    trackBlocksToTrainModelSignal       = QtCore.pyqtSignal(list) # List of block objects, sent to train
    greenLineTrackBlockSignal           = QtCore.pyqtSignal(list) # List of integer block numbers in the correct order for the green line.
    
    # Above could be a single list signal formatted as below: 
    # ["TrackLineName", [lineOccupancy], [lineSwitchStates], [lineMaintenance], [lineFailures]]


    # CTC Office Signals
    dispatchTrainSignal      = QtCore.pyqtSignal(list)
    suggestedSpeedSignal     = QtCore.pyqtSignal(list)

    # Wayside Controller Signals
    switchState              = QtCore.pyqtSignal(list) # List of length two indicating a block and it's switch state [block #, boolean state]
    crossingState            = QtCore.pyqtSignal(list) # List of length two indicating a block and it's crossing state [block #, boolean state]
    blockFailures            = QtCore.pyqtSignal(list) # List of length N where N is the number of blocks in the track
                                            ## Track Failure = 0x01, Circuit Failure = 0x02, Power Failure = 0x04 
                                            #   - any combination of the three should be logically OR'd together (i.e. TF + CF = 0x03)
    waysideAuthority         = QtCore.pyqtSignal(list) # List of variable length N. Each index holds a block number identifying that block as a "do not pass" mark

    # Train Model Signals
    blockListSignal          = QtCore.pyqtSignal(list)
    blockLengthSignal        = QtCore.pyqtSignal(list)
    gradeSignal              = QtCore.pyqtSignal(list)


    # Train Controller (SW) Inputs Signals
    authoritySignal          = QtCore.pyqtSignal(list)
    commandedSpeedSignal     = QtCore.pyqtSignal(list)
    speedLimitSignal         = QtCore.pyqtSignal(list)
    trainFailuresSignal      = QtCore.pyqtSignal(list)
    beaconSignal             = QtCore.pyqtSignal(list)        # Next Station and Station Side
    infrastructureSignal     = QtCore.pyqtSignal(list)        # Underground
    currentSpeedOfTrainModel = QtCore.pyqtSignal(float)
    
    # Train Controller (SW) Ouputs to Train Model Signals
    powerSignal              = QtCore.pyqtSignal(dict)
    lightSignal              = QtCore.pyqtSignal(list)
    doorSignal               = QtCore.pyqtSignal(list)
    temperatureSignal        = QtCore.pyqtSignal(list)
    announcementsSignal      = QtCore.pyqtSignal(list)
    advertisementsSignals    = QtCore.pyqtSignal(list)
    serviceBrakeSignal       = QtCore.pyqtSignal(list)
    emergencyBrakeSignal     = QtCore.pyqtSignal(list)

    # Train Controller (HW) Signals




