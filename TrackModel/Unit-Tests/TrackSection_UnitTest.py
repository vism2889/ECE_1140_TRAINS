#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackSection_UnitTest.py
# DESCRIPTION:
#       Code for testing the TrackSection.py file and its Dependencies
#
##############################################################################

import sys
import unittest
import time
# tell interpreter where to look for model files
sys.path.insert(0,"../Track-System-Models")
from TrackSection import TrackSection
from BlockModel import  BlockModel

class TrackSection_UnitTest(unittest.TestCase):
    
    def testTrackSectionName(self):
        self.trackSection = TrackSection("Test Section A")
        self.assertTrue(self.trackSection.name == "Test Section A")

    def testTrackSectionBlocks(self):
        self.trackSection = TrackSection("Test Section A")
        for i in range(10):
            tempBlock = BlockModel(pLine="green", pSection="BG"+str(i), pBlockNumber=i+1)
            self.trackSection.blocks.append(tempBlock)
        
        self.assertTrue(len(self.trackSection.blocks)==10)
        
        for i in range(10):
            self.assertTrue(self.trackSection.blocks[i].blockNumber  == i+1)
            self.assertTrue(self.trackSection.blocks[i].section == "BG"+str(i))
            self.assertTrue(self.trackSection.blocks[i].line == "green")


if __name__ == '__main__':
    print('running unittest')
    unittest.main()
