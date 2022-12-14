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
                pGrade='', pSpeedLimit='', pInfrastructure='NA', pStationSide='NA', 
                pElevation='',  pCumulativeElevation='', pSecsToTraverseBlock='', 
                pForwardBeacon='NA', pReverseBeacon='NA', pBlockDirection = ''):

        # STATIC INSTANCE VARIABLES
        self.line                   = pLine
        self.section                = pSection
        self.blockNumber            = pBlockNumber
        self.blockLength            = pBlockLength
        self.grade                  = pGrade
        self.speedLimit             = pSpeedLimit
        self.infrastructure         = pInfrastructure
        self.stationSide            = pStationSide         # set  to None if a station does not exist
        self.elevation              = pElevation
        self.cumulativeElevation    = pCumulativeElevation
        self.secsToTraverseBlock    = pSecsToTraverseBlock
        self.forwardBeacon          = pForwardBeacon        # Holds beacon information for trains moving in the forward direction
        self.reverseBeacon          = pReverseBeacon        # Holds beacon information for trains moving in the reverse direction
        self.blockDirection         = pBlockDirection
        self.station                = "NA"
        self.switch                 = "NA"
        self.crossingPresence       = False
        self.crossingSignalPresence = False
        self.underground            = False                 # Indicates whether the block is underground or not
        self.switchForward          = None                  # Holds the forward switch state
        self.switchReverse          = None                  # Holds the reverse switch state
        
        # DYNAMIC INSTANCE VARIABLES
        self.boardingPassengers     = 0                     # Number of passengers boarding a train at a given station, if block has no station this will default to zero
        self.leavingPassengers      = 0                     # Number of passengers exiting a train at a given station, if block has no station this will default to zero
        self.ticketSales            = 0                     # Number of tickets sold for a given station, if block has no station this will default to zero
        self.occupancy              = False                 # Indicates whether the current block is occupied or not
        self.switchState            = 'NA'                  # Indicates the state of the switch for a block if a switch exists
        self.heaterState            = False                 # Indicates the state of the track heater.  This changes based on the outside temperature of the rail system
        self.faultPresence          = False                 # Indicates whether a fault is present.
        self.faultsText             = []                    # List of strings indicating all of the faults present on a given block
        self.crossingSignalState    = False                 # Indicates the state of the crossing signal for a block if one is present

    def __str__(self):
        return "Block Number: " + str(self.blockNumber) + " in section " + str(self.section) + " of the " + str(self.line) + " line."