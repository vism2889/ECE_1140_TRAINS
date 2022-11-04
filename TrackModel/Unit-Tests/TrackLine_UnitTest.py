#!/usr/bin/env python3

##############################################################################
# AUTHOR:   Morgan Visnesky
# DATE:     11/03/2022
# FILENAME: TrackLine_UnitTest.py
# DESCRIPTION:
#       Code for testing the TrackLine.py file and its Dependencies
#
##############################################################################

import sys
import unittest
import time
# tell interpreter where to look for model files
sys.path.insert(0,"../Track-System-Models")
from TrackLine import TrackLine
from TrackSection import TrackSection

class TrackLine_UnitTest(unittest.TestCase):

    def testTrackLineName(self):
        self.trackLine = TrackLine("Test Track Line A")
        self.assertTrue(self.trackLine.name == "Test Track Line A")

    def testTrackLineSections(self):
        self.trackLine = TrackLine("Test Track Line A")
        for i in range(10):
            tempSection = TrackSection("Test Section: " + str(i))
            self.trackLine.sections.append(tempSection)
        
        self.assertTrue(len(self.trackLine.sections)==10)
        
        for i in range(10):
            self.assertTrue(self.trackLine.sections[i].name  == "Test Section: " + str(i))


if __name__ == '__main__':
    print('running unittest')
    unittest.main()