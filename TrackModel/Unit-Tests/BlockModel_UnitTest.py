#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: BlockModel_UnitTest.py
# DESCRIPTION:
#       Code for testing the BlockModel.py file and its Dependencies
#
##############################################################################

import sys
# tell interpreter where to look for model files
sys.path.insert(0,"../Track-System-Models")
from BlockModel import BlockModel

class BlockModel_UnitTest(unittest.TestCase):
    def setUp(self):
        self.block = BlockModel()

    def test_blockNumber(self):
        self.block.blockNumber = 1
        self.assertEqual(self.block.blockNumber, 1)

    def test_blockLength(self):
        self.block.blockLength = 1
        self.assertEqual(self.block.blockLength, 1)
    
    def test_grade(self):
        self.block.grade = 1
        self.assertEqual(self.block.grade, 1)

    def test_speedLimit(self):
        self.block.speedLimit = 1
        self.assertEqual(self.block.speedLimit, 1)

    def test_infrastructure(self):
        self.block.infrastructure = 'NA'
        self.assertEqual(self.block.infrastructure, 'NA')

    def test_stationSide(self):
        self.block.stationSide = 'NA'
        self.assertEqual(self.block.stationSide, 'NA')

    def test_elevation(self):
        self.block.elevation = 1
        self.assertEqual(self.block.elevation, 1)

    def test_cumulativeElevation(self):
        self.block.cumulativeElevation = 1
        self.assertEqual(self.block.cumulativeElevation, 1)

    def test_secsToTraverseBlock(self):
        self.block.secsToTraverseBlock = 1
        self.assertEqual(self.block.secsToTraverseBlock, 1)

    def test_forwardBeacon(self):
        self.block.forwardBeacon = 'NA'
        self.assertEqual(self.block.forwardBeacon, 'NA')

    def test_reverseBeacon(self):
        self.block.reverseBeacon = 'NA'
        self.assertEqual(self.block.reverseBeacon, 'NA')

    def test_blockDirection(self):
        self.block.blockDirection = 'NA'
        self.assertEqual(self.block.blockDirection, 'NA')

    def test_station(self):
        self.block.station = 'NA'
        self.assertEqual(self.block.station, 'NA')

    def test_switch(self):
        self.block.switch = 'NA'
        self.assertEqual(self.block.switch, 'NA')

    def test_crossingPresence(self):
        self.block.crossingPresence = False
        self.assertEqual(self.block.crossingPresence, False)

    def test_crossingSignalPresence(self):
        self.block.crossingSignalPresence = False
        self.assertEqual(self.block.crossingSignalPresence, False)

    def test_underground(self):
        self.block.underground = False
        self.assertEqual(self.block.underground, False)

    def test_switchForward(self):
        self.block.switchForward = None
        self.assertEqual(self.block.switchForward, None)

    def test_switchReverse(self):
        self.block.switchReverse = None
        self.assertEqual(self.block.switchReverse, None)

    def test_boardingPassengers(self):
        self.block.boardingPassengers = 0
        self.assertEqual(self.block.boardingPassengers, 0)

    def test_leavingPassengers(self):
        self.block.leavingPassengers = 0
        self.assertEqual(self.block.leavingPassengers, 0)

    def test_ticketSales(self):
        self.block.ticketSales = 0
        self.assertEqual(self.block.ticketSales, 0)

    def test_occupancy(self):
        self.block.occupancy = False
        self.assertEqual(self.block.occupancy, False)

    def test_switchState(self):
        self.block.switchState = 'NA'
        self.assertEqual(self.block.switchState, 'NA')

    def test_heaterState(self):
        self.block.heaterState = False
        self.assertEqual(self.block.heaterState, False)

    def test_faultPresence(self):
        self.block.faultPresence = False
        self.assertEqual(self.block.faultPresence, False)

    def test_faultsText(self):
        self.block.faultsText = []
        self.assertEqual(self.block.faultsText, [])

    def test_crossingSignalState(self):
        self.block.crossingSignalState = False
        self.assertEqual(self.block.crossingSignalState, False)

    def test_str(self):
        self.block.line = 'Red'
        self.block.section = 'A'
        self.block.blockNumber = 1
        self.assertEqual(str(self.block), "Block Number: 1 in section A of the Red line.")