import sys
from block import block

redLine = []
blueLine = []

redLine.append( block('A') )
redLine.append( block('B') )
redLine.append( block('C') )

blueLine.append( block('A') )
blueLine.append( block('B') )
blueLine.append( block('C') )

redLineLookup = {
    'Block A': 0,
    'Block B': 1,
    'Block C': 2
}