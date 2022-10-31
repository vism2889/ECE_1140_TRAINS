import sys
import re
from Block import Block

class BlockList:

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
                print(station)
            elif type == "SWITCH":
                print('')
            elif type == "RAILWAY":
                print('')
            
    def len(self):
        return len(self.blockList)