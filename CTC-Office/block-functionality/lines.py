import sys
from block import block

redLine = []
greenLine = []

# Create red line
for blockNumber in range(1,6):
    redLine.append( block(blockNumber, 50, 40) )

for blockNumber in range(7,12):
    redLine.append( block(blockNumber, 75, 40) )

redLineLookup = dict()

for blockName in range(1,12):
    redLineLookup["Block " + str(blockName)] = blockName-1

    

# Create green line
for blockNumber in range(1,6):
    greenLine.append( block(blockNumber, 50, 40) )

for blockNumber in range(7,12):
    greenLine.append( block(blockNumber, 75, 40) )

greenLineLookup = dict()

for blockName in range(1,12):
    greenLineLookup["Block " + str(blockName)] = blockName-1