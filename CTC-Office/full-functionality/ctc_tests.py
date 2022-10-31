import unittest
from lines import *
from trains import *

class TestBlockFaults() {

    def testSetFault(self):
        redLineBlocks[1].toggleFaultState()

        # pop up will also appear and color will be red
        self.assertIs(redLineBlocks[1].faultState, true)


}

class TestBlockOccupancy() {

    def testOccupancies(self):
        redLineBlocks[1].toggleOccupancy()
        # color should be green
        self.assertIs(redLineBlocks[1].occupancy, true)

        redLineBlocks[1].toggleOccupancy()
        # color should be white
        self.assertIs(redLineBlocks[1].occupancy, false)

}

class TestCrossingStates() {
    
    def testCrossingState(self):

        # colors should match statesa
        redLineBlocks[47].toggleCrossingState()
        self.assertIs(redLineBlocks[47].crossingState, "Yellow")

        redLineBlocks[47].toggleCrossingState()
        self.assertIs(redLineBlocks[47].crossingState, "Red")

        redLineBlocks[47].toggleCrossingState()
        self.assertIs(redLineBlocks[47].crossingState, "Green")

}