#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/13/2022
# FILENAME: occupancySignalSender.py
# DESCRIPTION:
#   Used to send signal communications to the TrackModel UI
#   Emulates:
#       - Occupancy
#       - Track Faults
#       - Block Maintenance
##############################################################################

import time
import random
import threading

class SendOccupancy():
    def __init__(self, signals):
        super().__init__()
        self.signals         = signals
        self.blocks          = [i for i in range(150)]
        self.blockLens       = [random.randint(10,25) for i in range(150)]
        self.distance        = 0
        self.currBlockIndex  = 0
        self.timerr          = 0
        
        self.occupancy       = [0 for i in range(150)]
        self.faults          = [0 for i in range(150)]
        self.maintenance     = [0 for i in range(150)]
        self.line            = "Green"

        self.signals.trackFailuresSignal.connect(self.updateFaults)
        self.occupancyThread = threading.Thread(target=self.timer)
        self.occupancyThread.start()
        
    def timer(self):
        while self.currBlockIndex < 15:
            speed = 50
            self.timerr += .01
            self.distance = speed*self.timerr
            print("distance:", self.distance)
            self.getOccupancy()
            time.sleep(0.1)

    def updateFaults(self, faults):
        self.faults = faults

    def getOccupancy(self):
        if self.distance >= self.blockLens[self.currBlockIndex]:
            self.currBlockIndex += 1
            self.distance                         = 0
            self.timerr                           = 0
            self.occupancy[self.currBlockIndex-1] = 0
            self.occupancy[self.currBlockIndex]   = 1
            
            print("NEW OCCUPANCY:", self.currBlockIndex)
        self.signals.occupancySignal.emit(self.occupancy)
        
        print("Train on Block:", self.currBlockIndex+1)
        print("FAULTS:\n", self.faults)