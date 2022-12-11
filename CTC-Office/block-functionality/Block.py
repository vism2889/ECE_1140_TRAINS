import sys

class Block:

    def __init__(self, line, section, number, length, speedLimit, infrastructure):
        self.line = line
        self.section = section
        self.number = number
        self.length = length
        self.infrastructure = infrastructure
        self.speedLimit = speedLimit
        self.occupancy = False
        self.faultState = False
        self.maintenanceState = False
        self.authority = False

    # def getOccupancy(self):
    #     if self.occupancy:
    #         return "yes"
    #     else:
    #         return "no"

    # def getFaultState(self):
    #     if self.faultState:
    #         return "yes"
    #     else:
    #         return "no"

    # def getMaintenanceState(self):
    #     if self.maintenanceState:
    #         return "yes"
    #     else:
    #         return "no"

    # def toggleOccupancy(self):
    #     self.occupancy ^= True

    # def toggleFaultState(self):
    #     self.faultState ^=True

    # def toggleMaintenanceState(self):
    #     self.maintenanceState ^= True



