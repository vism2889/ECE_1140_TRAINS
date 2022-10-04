#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/01/2022
# FILENAME: RailLineModel.py
# DESCRIPTION:
#       Code for the rail lines that make up the light rail system
# **NOTE This model may not be needed
##############################################################################

class RailLineModel:
    vRailLineName = '' # the string name of the rail line
    vTrackBlocks  = [] # a list of BlockModel objects that make up this rail line

    def __init__(self, pRailLineName):
        vRailLineName = pRailLineName

    def addBlockToLine(self, pBlock):
        vTrackBlocks.append(pBlock)
