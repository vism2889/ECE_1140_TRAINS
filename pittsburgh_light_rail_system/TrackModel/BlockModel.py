#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/01/2022
# FILENAME: BlockModel.py
# DESCRIPTION:
#       Code for the blocks that make up the Track Model 
#
##############################################################################

class BlockModel:
    vBlockNumber      = ''
    vSwitchPresence   = ''
    vSwitchState      = ''
    vStation          = ''
    vCrossingPresence = ''
    vGrade            = ''
    vLineName         = ''
    vSignalPresence   = ''
    vSignalState      = ''

    def __init__(self, pBlockNumber, pSwitchPresence, pStation, pCrossingPresence, pGrade):
        vBlockNumber      = pBlockNumber
        vSwitchPresence   = pSwitchPresence
        vStation          = pStation
        vCrossingPresence = pCrossingPresence
        vGrade            = pGrade

    def setBlockNumber(self, pBlockNumber):
        vBlockNumber = pBlockNumber

    def getBlockNumber(self):
        return vBlockNumber

    def setSwitchPresence(self, pSwitchPresence):
        vSwitchPresence = pSwitchPresence

    def getSwitchPresence(self):
        return vSwitchPresence

    def setStation(self, pStation):
        vStation = pStation

    def getStation(self):
        return vStation

    def setCrossingPresence(self, pCrossingPresence):
        vCrossingPresence = pCrossingPresence

    def getCrossingPresence(self):
        return vCrossingPresence

    def setGrade(self, pGrade):
        vGrade = pGrade 

    def getGrade(self):
        return vGrade