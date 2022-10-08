import sys

class block:

    occupancy = False
    faultState = False
    maintenanceState = False

    def __init__(self, name, length, speedLimit):
        self.name = name
        self.length = length
        self.speedLimit = speedLimit

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


