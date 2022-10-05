import sys

class block:
    occupancy = False
    faultState = False
    maintenanceState = False

    def __init__(self, name):
        self.name = name

    def getOccupancy(self):
        return self.occupancy

    def getFaultState(self):
        return self.faultState

    def getMaintenanceState(self):
        return self.maintenanceState

    def toggleOccupancy(self):
        self.occupancy ^= True

    def toggleFaultState(self):
        self.faultState ^=True

    def toggleMaintenanceState(self):
        self.maintenanceState ^= True

