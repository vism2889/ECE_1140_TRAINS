import sys
import re

from Block import Block

class BlockDictionary:

    def __init__(self):
        self.blockList = dict()
        self.stationList = dict()
        self.switchList = dict()
        self.crossingList = dict()

    def addBlock(self, newBlock):
        self.blockList[newBlock.number] = newBlock

        if (newBlock.infrastructure != '' and newBlock.infrastructure != 'UNDERGROUND'):
            type = re.split('; | |: ', newBlock.infrastructure)[0]

            if type == "STATION":
                try:
                    re.split('; |: ', newBlock.infrastructure)[1]
                except:
                    print("Missing station name on block", newBlock.number)
                    return
                station = re.split('; |: ', newBlock.infrastructure)[1]
                self.stationList[newBlock.number] = station
            elif type == "SWITCH":
                noUnderground = re.split('UNDERGROUND', newBlock.infrastructure)[0]
                switch = noUnderground.split(' ',1)[1]
                self.switchList[newBlock.number] = [switch, True]
            elif type == "RAILWAY":
                self.crossingList[newBlock.number] = "red"

    def toggleOccupancy(self, blockNum):
        self.blockList[blockNum].occupancy = not self.blockList[blockNum].occupancy

        # TODO use this speed limit to send suggested speed and make everything work
        if self.blockList[blockNum].occupancy:
            return self.blockList[blockNum].speedLimit

    def toggleMaintenanceState(self, blockNum):
        self.blockList[blockNum].maintenanceState = not self.blockList[blockNum].maintenanceState

    def toggleFaultState(self, blockNum):
        self.blockList[blockNum].faultState = not self.blockList[blockNum].faultState

    def getLine(self, blockNum):
        return self.blockList[blockNum].line
    
    def getOccupancy(self, blockNum):
        return self.blockList[blockNum].occupancy

    def getFaultState(self, blockNum):
        return self.blockList[blockNum].faultState

    def getMaintenanceState(self, blockNum):
        return self.blockList[blockNum].maintenanceState

    def keys(self):
        return self.blockList.keys()

    def stations(self):
        return self.stationList

    def station(self, key):
        try:
            return self.stationList[key]
        except KeyError as K:
            return 0

    def switch(self, key):
        try:
            return self.switchList[key]
        except KeyError as K:
            return 0

    def crossing(self, key):
        try:
            return self.crossingList[key]
        except KeyError as K:
            return 0

    def len(self):
        return len(self.blockList)