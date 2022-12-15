#!/usr/bin/env python3

##############################################################################
# AUTHOR(S):    Morgan Visnesky
# DATE:         11/13/2022
# FILENAME:     SystemSignals_UnitTest.py
# DESCRIPTION:
#       Code for testing the Signals.py file with TrackModelApp.py
##############################################################################

import sys
import unittest
# tell interpreter where to look for model files
sys.path.insert(0,"../Track-System-Models")
from BlockModel import BlockModel
from Signals import Signals

sys.path.insert(0,"../UI")
from TrackModelApp import TrackModel

class TrackModelAppSignal_UnitTest(unittest.TestCase):
    #write a test here for ../ui/TrackModelApp.py using each signal using above as a reference

    def setUp(self):
        self.signals = Signals()
        self.model = TrackModel(self.signals)

    def test_trackModelLayoutLoadedSignal(self):
        self.signals.trackModelLayoutLoadedSignal.emit([True])
        self.assertEqual(self.model.layoutLoaded, True)

    def test_trackFailuresSignal(self):
        self.signals.trackFailuresSignal.emit([0x01, 0x02, 0x04])
        self.assertEqual(self.model.trackFailures, [0x01, 0x02, 0x04])
    
    def test_globalOccupancyFromTrackModelSignal(self):
        self.signals.globalOccupancyFromTrackModelSignal.emit([True, False, True])
        self.assertEqual(self.model.globalOccupancy, [True, False, True])

    def test_beaconFromTrackModelSignal(self):
        self.signals.beaconFromTrackModelSignal.emit(["StationSide", "Station", "Underground"])
        self.assertEqual(self.model.beacon, ["StationSide", "Station", "Underground"])

    def test_trackBlocksToTrainModelSignal(self):
        self.signals.trackBlocksToTrainModelSignal.emit([])
        self.assertEqual(self.model.trackBlocks, [])

    def test_greenLineTrackBlockSignal(self):
        self.signals.greenLineTrackBlockSignal.emit([1, 2, 3])
        self.assertEqual(self.model.greenLineTrackBlocks, [1, 2, 3])

    def test_passengersToTrainModelSignal(self):
        self.signals.passengersToTrainModelSignal.emit(["Train ID", 5])
        self.assertEqual(self.model.passengers, ["Train ID", 5])
    
    def test_lineTicketSalesToCtcOfficeSignal(self):
        self.signals.lineTicketSalesToCtcOfficeSignal.emit([5, 10])
        self.assertEqual(self.model.lineTicketSales, [5, 10])

    def test_ctcAuthoritySignal(self):
        self.signals.ctcAuthoritySignal.emit(["Train ID", [1, 2, 3]])
        self.assertEqual(self.model.ctcAuthority, ["Train ID", [1, 2, 3]])

    def test_clockSpeedSignal(self):
        self.signals.clockSpeedSignal.emit(5)
        self.assertEqual(self.model.clockSpeed, 5)

    def test_signalMaintenance(self):
        self.signals.signalMaintenance.emit([1, 2, True])
        self.assertEqual(self.model.signalMaintenance, [1, 2, True])

    def test_timeSignal(self):
        self.signals.timeSignal.emit([1, 2, 3])
        self.assertEqual(self.model.time, [1, 2, 3])

    def test_ctcSwitchState(self):
        self.signals.ctcSwitchState.emit([1, 2, True])
        self.assertEqual(self.model.ctcSwitchState, [1, 2, True])

    def test_switchState(self):
        self.signals.switchState.emit([1, True])
        self.assertEqual(self.model.switchState, [1, True])

    def test_crossingState(self):
        self.signals.crossingState.emit([1, True])
        self.assertEqual(self.model.crossingState, [1, True])

    def test_waysideAuthority(self):
        self.signals.waysideAuthority.emit([1, "Train ID", [1, 2, 3]])
        self.assertEqual(self.model.waysideAuthority, [1, "Train ID", [1, 2, 3]])

    def test_blockMaintenance(self):
        self.signals.blockMaintenance.emit([1, 2, True])
        self.assertEqual(self.model.blockMaintenance, [1, 2, True])

    def test_regulatedSpeed(self):
        self.signals.regulatedSpeed.emit([1, "Train ID", 5])
        self.assertEqual(self.model.regulatedSpeed, [1, "Train ID", 5])

    def test_blockListSignal(self):
        self.signals.blockListSignal.emit([1, 2, 3])
        self.assertEqual(self.model.blockList, [1, 2, 3])

    def test_blockLengthSignal(self):
        self.signals.blockLengthSignal.emit([1, 2, 3])
        self.assertEqual(self.model.blockLength, [1, 2, 3])

    def test_gradeSignal(self):
        self.signals.gradeSignal.emit([1, 2, 3])
        self.assertEqual(self.model.grade, [1, 2, 3])

    def test_trainLocation(self):
        self.signals.trainLocation.emit([1, "Train ID", 2, 3])
        self.assertEqual(self.model.trainLocation, [1, "Train ID", 2, 3])

    def test_stationStop(self):
        self.signals.stationStop.emit(["Train ID", True, 1, 2])
        self.assertEqual(self.model.stationStop, ["Train ID", True, 1, 2])

    def test_ctcStopBlock(self):
        self.signals.ctcStopBlock.emit([1, 2])
        self.assertEqual(self.model.ctcStopBlock, [1, 2])