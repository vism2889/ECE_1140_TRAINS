#!/usr/bin/env python3

##############################################################################
# AUTHOR(S):    Morgan Visnesky, Garrett Marcinak, Nathaniel Mallick
# DATE:         11/13/2022
# FILENAME:     occupancySignalSender.py
# DESCRIPTION:
#   Used to hold all signals used for inter-module communications in the
#   Pittsburgh Light Rail Track System
# Last Updated: 12/7/2022 - Nathaniel Mallick
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


    beaconFromTrackModelSignal          = QtCore.pyqtSignal(list) # List containing information from beacon

    # Above could be a single list signal formatted as below:
    # ["TrackLineName", [lineOccupancy], [lineSwitchStates], [lineMaintenance], [lineFailures]]

    # CTC Office Signals
    dispatchTrainSignal      = QtCore.pyqtSignal(list) # List of lenfth 3 [(string) train id,  (string) line, (int) suggested speed]
    suggestedSpeedSignal     = QtCore.pyqtSignal(list) # List of length 2 [(string) train id, (int) suggested speed]
    ctcAuthoritySignal       = QtCore.pyqtSignal(list) # List of length 2 [(string) train id, [(int) stops 1, (int), stop 2, ..., (int) stop n]]
    clockSpeedSignal         = QtCore.pyqtSignal(int)  # Integer value of clock speed
    signalMaintenance        = QtCore.pyqtSignal(list) # List of length 3 [(int) line, (int) block #, (bool) maintenance state]
    timeSignal               = QtCore.pyqtSignal(list) # List of length 3 [(int) hours, (int) mins, (int) secs]
    ctcSwitchState           = QtCore.pyqtSignal(list) # List of length 3 [(int) line, (int) block #, (bool) switch state]

    # Wayside Controller Signals
    switchState              = QtCore.pyqtSignal(list) # List of length two indicating a block and it's switch state [(int) block #, (bool) state]
    crossingState            = QtCore.pyqtSignal(list) # List of length two indicating a block and it's crossing state [(int) block #, (bool) state]
    waysideAuthority         = QtCore.pyqtSignal(list) # List of length 3 that specifices the authority for an individual train [(int) line,(...) train id, (list) blocks[]]
    blockMaintenance         = QtCore.pyqtSignal(list) # List of length 3 that specifies the maintenance state of a block [(int) line, (int) block #, (bool) state]

    # Train Model Signals
    blockListSignal          = QtCore.pyqtSignal(list)
    blockLengthSignal        = QtCore.pyqtSignal(list)
    gradeSignal              = QtCore.pyqtSignal(list)
    trainLocation            = QtCore.pyqtSignal(list) # List of length 4 that identifies a unique trains location in the track [(int) line, (int) train id, (int) previos block, (int) current block]
    stationStop              = QtCore.pyqtSignal(dict) #List of length 2[(string) train id, (bool) stationStop]
    # Train Controller (SW) Input Signals
    authoritySignal          = QtCore.pyqtSignal(list) #List of length 2 [(string) train id, (float) authority]
    commandedSpeedSignal     = QtCore.pyqtSignal(list) #List of length 2 [(string) train id, (float) commanded speed]
    speedLimitSignal         = QtCore.pyqtSignal(list) #List of length 2 [(string) train id, (float) speed limit]
    trainFailuresSignal      = QtCore.pyqtSignal(list) #List of length 2 [(string) train id, (list, length 3) [(bool) train engine, (bool) signal pickup, (bool) brake]]
    beaconSignal             = QtCore.pyqtSignal(list)        # Next Station and Station Side
    infrastructureSignal     = QtCore.pyqtSignal(list)        # Underground
    currentSpeedOfTrainModel = QtCore.pyqtSignal(list)

    # Train Controller (SW) Ouputs to Train Model Signals
    powerSignal              = QtCore.pyqtSignal(dict) # Dictionary containing 'trainID' and 'power' 
    brakeDictSignal          = QtCore.pyqtSignal(dict) # Dictionary containing 'serviceBrake', 'emergencyBrake', and 'trainID'
    nonVitalDictSignal       = QtCore.pyqtSignal(dict) # Dictionary containing 'int_lights', 'ext_lights', 'temperature', 'left_doors', 'right_doors', 'announceState', 'advertisementState', and 'trainID'

    # Train Controller (HW) Signals





