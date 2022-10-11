import sys
from block import block

redLineBlocks = dict()
for blockNumber in range(1,12):
    redLineBlocks["Block " + str(blockNumber)] = block(blockNumber, 75, 40)

greenLineBlocks = dict()
for blockNumber in range(1,12):
    greenLineBlocks["Block " + str(blockNumber)] = block(blockNumber, 75, 40)

