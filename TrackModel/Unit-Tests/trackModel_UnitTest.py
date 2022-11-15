#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     10/29/2022
# FILENAME: TestTrackModel.py
# DESCRIPTION:
#       Code for testing the TrackModel and its Dependencies
#
##############################################################################

from LayoutParser import LayoutParser as LP
import unittest
import time

class TestTrackModel(unittest.TestCase):

    #startup
    def test_uploadcsv_lines(self):
        self.parser = LP("")
        lineNames, lines = parser.process()
        print("testing testing csv tracklayout upload: Line Test")
        self.assertTrue(len(lineNames) == 2) # there should be 2 lines
        self.assertTrue(len(lines) == 2) # there should be 2 line names


    def test_uploadcsv_sections(self):
        self.parser = LP("")
        lineNames, lines = parser.process()
        print("testing testing csv tracklayout upload: Section Test")
        self.assertTrue(len(lines[0]) == 20) #redline should have 20 sections
        self.assertTrue(len(lines[1]) == 26) #greenline should have 26 sections

    def test_uploadcsv_blocks(self):
        self.parser = LP("")
        lineNames, lines = parser.process()
        print("testing testing csv tracklayout upload: Block Test")
        self.assertTrue(len(lines[0][0]) == 3) #redline first section should have 3 blocks
        self.assertTrue(len(lines[1][0]) == 3) #greenline first section should have 3 blocks
    
    def test_uploadcsv_blockdata(self):
        self.parser = LP("")
        lineNames, lines = parser.process()
        print("testing testing csv tracklayout upload: Block Data Test")
        block = lines[0][0][0] #redline,section A, block 1
        self.assertTrue(block.line == "red")
        self.assertTrue(block.section == "A")
        self.assertTrue(block.blockNumber == "1")
        self.assertTrue(block.blockLength == "50")
        self.assertTrue(block.grade == "0.5")
        self.assertTrue(block.speedLimit == "40")
        self.assertTrue(block.infrastructuree != "")
        self.assertTrue(block.stationSide == "")
        self.assertTrue(block.elevation == "0.25")
        self.assertTrue(block.cumulativeElevation == "0.25")
        self.assertTrue(block.secsToTraverseBlock == "")

if __name__ == '__main__':
    print('running unittest')
    unittest.main()