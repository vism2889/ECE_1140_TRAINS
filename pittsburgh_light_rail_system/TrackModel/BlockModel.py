#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/01/2022
# FILENAME: BlockModel.py
# DESCRIPTION:
#       Code for the blocks that make up the Track Model 
#
##############################################################################

# Questions:
# How to determine where crossings are.  Is there one at every station that is not underground?

class BlockModel:
    def __init__(self, pLine, pSection, pBlockNumber, pBlockLength,
                pGrade, pSpeedLimit, pInfrastructure, pStationSide, 
                pElevation,  pCumulativeElevation, pSecsToTraverseBlock):
        self.line                = pLine
        self.section             = pSection
        self.blockNumber         = pBlockNumber
        self.blockLength         = pBlockLength
        self.grade               = pGrade
        self.speedLimit          = pSpeedLimit
        self.infrastructure      = pInfrastructure
        self.stationSide         = pStationSide      # set  to None if a station does not exist
        self.elevation           = pElevation
        self.cumulativeElevation = pCumulativeElevation
        self.secsToTraverseBlock = pSecsToTraverseBlock

        self.occupancy = False
        self.faults = [False, False, False]
        self.faultsText =  ""
        # values needed for Wayside and Train Model
        # self.vSwitchPresence   = None #gets set based on infrastructure
        # self.vSwitchState      = None #gets set based on infrastructure
        # self.vStation          = None #gets set based on infrastructure
        # self.vCrossingPresence = None #unknown: maybe is present at every above ground station
        # self.vSignalPresence   = None #unknown
        # self.vSignalState      = None #unknown