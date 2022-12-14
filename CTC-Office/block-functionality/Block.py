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


