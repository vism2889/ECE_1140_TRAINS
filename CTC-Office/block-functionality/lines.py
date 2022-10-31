import sys
from Block import Block

redLineCrossing = dict()
greenLineCrossing  = dict()

redLineCrossing["47"] = "Red"
greenLineCrossing["20"] = "Red"

redLineSwitches = dict()
redLineSwitches["(15-16; 1-16)"]  = "forward"
redLineSwitches["(27-28; 27-76)"] = "forward"
redLineSwitches["(32-33; 33-72)"] = "forward"
redLineSwitches["(38-39; 38-71)"] = "forward"
redLineSwitches["(43-44; 44-67)"] = "forward"
redLineSwitches["(52-53; 52-66)"] = "forward"

greenLineSwitches = dict()
greenLineSwitches["(15-16; 1-16)"]  = "forward"
greenLineSwitches["(27-28; 27-76)"] = "forward"

totalPassengers = dict()
totalPassengers["totalPassengers"] = 0

def toggleRedLineSwitch(name):
    if redLineSwitches[name] == "forward":
        redLineSwitches.update({name:"reverse"})
    elif redLineSwitches[name] == "reverse":
        redLineSwitches.update({name:"forward"})

def toggleGreenLineSwitch(name):
    if greenLineSwitches[name] == "forward":
        greenLineSwitches.update({name:"reverse"})
    elif greenLineSwitches[name] == "reverse":
        greenLineSwitches.update({name:"forward"})

redLineBlocks = dict()
for blockNumber in range(1,12):
    redLineBlocks["Block " + str(blockNumber)] = Block(blockNumber, 75, 40)

greenLineBlocks = dict()
for blockNumber in range(1,12):
    greenLineBlocks["Block " + str(blockNumber)] = Block(blockNumber, 75, 40)

