from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget

class Signals(QWidget):
    # Track Message Signals
    occupancySignal     = QtCore.pyqtSignal(list)
    switchStatesSignal  = QtCore.pyqtSignal(list)
    maintenanceSignal   = QtCore.pyqtSignal(list)
    trackFailuresSignal = QtCore.pyqtSignal(list)
    lineSignal          = QtCore.pyqtSignal(str)

    # CTC Office Signals
    dispatchTrainSignal  = QtCore.pyqtSignal(str)
    suggestedSpeedSignal = QtCore.pyqtSignal(list)

    # Train Model Signals
    blockListSignal    = QtCore.pyqtSignal(list)
    blockLengthSignal  = QtCore.pyqtSignal(list)
    gradeSignal        = QtCore.pyqtSignal(list)

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
    powerSignal           = QtCore.pyqtSignal(list)
    lightSignal           = QtCore.pyqtSignal(list)
    doorSignal            = QtCore.pyqtSignal(list)
    temperatureSignal     = QtCore.pyqtSignal(list)
    announcementsSignal   = QtCore.pyqtSignal(list)
    advertisementsSignals = QtCore.pyqtSignal(list)
    serviceBrakeSignal    = QtCore.pyqtSignal(list)
    emergencyBrakeSignal  = QtCore.pyqtSignal(list)

    # Train Controller (HW) Signals




