import sys

class block:

    def __init__(self, number, length, speedLimit):
        self.number = number
        self.length = length
        self.speedLimit = speedLimit
        self.occupancy = False
        self.faultState = False
        self.maintenanceState = False

    def getOccupancy(self):
        if self.occupancy:
            return "yes"
        else:
            return "no"

    def getFaultState(self):
        if self.faultState:
            return "yes"
        else:
            return "no"

    def getMaintenanceState(self):
        if self.maintenanceState:
            return "yes"
        else:
            return "no"

    def toggleOccupancy(self):
        self.occupancy ^= True

    def toggleFaultState(self):
        self.faultState ^=True

    def toggleMaintenanceState(self):
        self.maintenanceState ^= True



