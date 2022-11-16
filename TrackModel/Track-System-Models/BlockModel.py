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
    '''
    Class Description here
    '''
    def __init__(self, pLine='', pSection='', pBlockNumber='', pBlockLength='',
                pGrade='', pSpeedLimit='', pInfrastructure='', pStationSide='', 
                pElevation='',  pCumulativeElevation='', pSecsToTraverseBlock=''):
        self.line                = pLine
        self.section             = pSection
        self.blockNumber         = pBlockNumber
        self.blockLength         = pBlockLength
        self.grade               = pGrade
        self.speedLimit          = pSpeedLimit
        self.infrastructure      = pInfrastructure
        self.stationSide         = pStationSide         # set  to None if a station does not exist
        self.elevation           = pElevation
        self.cumulativeElevation = pCumulativeElevation
        self.secsToTraverseBlock = pSecsToTraverseBlock

        self.occupancy              = False
        self.faultPresence          = False
        self.faultsText             = []
        self.station                = ""
        self.switch                 = ""
        self.crossingPresence       = False
        self.crossingSignalPresence = False
        self.crossingSignalState    = False
        self.underground            = False



        # values needed to receive for Wayside Controller
        # values needed to send to Train Model

    def __str__(self):
        return "Block Number: " + str(self.blockNumber) + " in section " + str(self.section) + " of the " + str(self.line) + " line."