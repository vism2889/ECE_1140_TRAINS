import sys
from block import block

redLine = []
blueLine = []

redLine.append( block('A') )
redLine.append( block('B') )
redLine.append( block('C') )
redLine[1].toggleOccupancy()

blueLine.append( block('A') )
blueLine.append( block('B') )
blueLine.append( block('C') )

