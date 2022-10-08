import sys
from block import block

redLine = []
blueLine = []

# Create red line
for blockNumber in range(1,6):
    redLine.append( block(blockNumber, 50, 40) )

for blockNumber in range(7,12):
    redLine.append( block(blockNumber, 75, 40) )

redLineLookup = dict()

for blockName in range(1,12):
    redLineLookup["Block " + blockName] = blockName-1