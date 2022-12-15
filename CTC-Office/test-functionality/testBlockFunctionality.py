import unittest
from Block import Block
from BlockDictionary import BlockDictionary

class BlockTest(unittest.TestCase):
    def setUp(self):
        self.block = Block("BLUE", "A", 1, 10, 10, "STATION; STATION NAME")

    def testInit(self):
        self.assertEqual(self.block.line, "BLUE")
        self.assertEqual(self.block.section, "A")
        self.assertEqual(self.block.number, 1)
        self.assertEqual(self.block.length, 10)
        self.assertEqual(self.block.speedLimit, 10)
        self.assertEqual(self.block.infrastructure, "STATION; STATION NAME")
        self.assertFalse(self.block.occupancy)
        self.assertFalse(self.block.faultState)
        self.assertFalse(self.block.maintenanceState)
        self.assertFalse(self.block.authority)

class BlockDictionaryTest(unittest.TestCase):
    def setUp(self):
        self.blockDict = BlockDictionary()
        self.block1 = Block("BLUE", "A", 1, 10, 10, "STATION; STATION NAME")
        self.block2 = Block("BLUE", "A", 2, 10, 10, "SWITCH; SWITCH NAME")
        self.block3 = Block("BLUE", "A", 3, 10, 10, "CROSSING; CROSSING NAME")

    def testInit(self):
        self.assertEqual(self.blockDict.blockList, {})
        self.assertEqual(self.blockDict.stationList, {})
        self.assertEqual(self.blockDict.switchList, {})
        self.assertEqual(self.blockDict.crossingList, {})

    def testAddBlock(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.addBlock(self.block2)
        self.blockDict.addBlock(self.block3)
        self.assertEqual(len(self.blockDict.blockList), 3)
        self.assertEqual(len(self.blockDict.stationList), 1)
        self.assertEqual(len(self.blockDict.switchList), 1)
        self.assertEqual(len(self.blockDict.crossingList), 1)

    def testSetOccupancy(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.setOccupancy(self.block1.number, True)
        self.assertTrue(self.blockDict.getOccupancy(self.block1.number))

    def testToggleMaintenanceState(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.toggleMaintenanceState(self.block1.number)
        self.assertTrue(self.blockDict.getMaintenanceState(self.block1.number))

    def testToggleFaultState(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.toggleFaultState(self.block1.number)
        self.assertTrue(self.blockDict.getFaultState(self.block1.number))

    def testSetSwitchState(self):
        self.blockDict.addBlock(self.block2)
        self.blockDict.setSwitchState(self.block2.number, False)
        self.assertFalse(self.blockDict.getSwitchState(self.block2.number)[1])

    def testSetAuthority(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.setAuthority(self.block1.number, True)
        self.assertTrue(self.blockDict.getAuthority(self.block1.number))

    def testGetStation(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.getStation(self.block1.number), "STATION NAME")

    def testGetLine(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.getLine(self.block1.number), "BLUE")

    def testKeys(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(list(self.blockDict.keys()), [1])

    def testStations(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.stations(), {1: "STATION NAME"})

    def testStation(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.station(1), "STATION NAME")

    def testSwitch(self):
        self.blockDict.addBlock(self.block2)
        self.assertEqual(self.blockDict.switch(2), [self.block2.infrastructure.split(' ',1)[1], True])

    def testCrossing(self):
        self.blockDict.addBlock(self.block3)
        self.assertEqual(self.blockDict.crossing(3), "red")

    def testLen(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.len(), 1)

if __name__ == '__main__':
    unittest.main()