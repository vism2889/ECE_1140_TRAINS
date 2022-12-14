import unittest
from Block import Block
from BlockDictionary import BlockDictionary

class BlockTest(unittest.TestCase):
    def setUp(self):
        self.block = Block("BLUE", "A", 1, 10, 10, "STATION; STATION NAME")

    def test_init(self):
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

    def test_init(self):
        self.assertEqual(self.blockDict.blockList, {})
        self.assertEqual(self.blockDict.stationList, {})
        self.assertEqual(self.blockDict.switchList, {})
        self.assertEqual(self.blockDict.crossingList, {})

    def test_addBlock(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.addBlock(self.block2)
        self.blockDict.addBlock(self.block3)
        self.assertEqual(len(self.blockDict.blockList), 3)
        self.assertEqual(len(self.blockDict.stationList), 1)
        self.assertEqual(len(self.blockDict.switchList), 1)
        self.assertEqual(len(self.blockDict.crossingList), 1)

    def test_setOccupancy(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.setOccupancy(self.block1.number, True)
        self.assertTrue(self.blockDict.getOccupancy(self.block1.number))

    def test_toggleMaintenanceState(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.toggleMaintenanceState(self.block1.number)
        self.assertTrue(self.blockDict.getMaintenanceState(self.block1.number))

    def test_toggleFaultState(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.toggleFaultState(self.block1.number)
        self.assertTrue(self.blockDict.getFaultState(self.block1.number))

    def test_setSwitchState(self):
        self.blockDict.addBlock(self.block2)
        self.blockDict.setSwitchState(self.block2.number, False)
        self.assertFalse(self.blockDict.getSwitchState(self.block2.number)[1])

    def test_setAuthority(self):
        self.blockDict.addBlock(self.block1)
        self.blockDict.setAuthority(self.block1.number, True)
        self.assertTrue(self.blockDict.getAuthority(self.block1.number))

    def test_getStation(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.getStation(self.block1.number), "STATION NAME")

    def test_getLine(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.getLine(self.block1.number), "BLUE")

    def test_keys(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(list(self.blockDict.keys()), [1])

    def test_stations(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.stations(), {1: "STATION NAME"})

    def test_station(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.station(1), "STATION NAME")

    def test_switch(self):
        self.blockDict.addBlock(self.block2)
        self.assertEqual(self.blockDict.switch(2), [self.block2.infrastructure.split(' ',1)[1], True])

    def test_crossing(self):
        self.blockDict.addBlock(self.block3)
        self.assertEqual(self.blockDict.crossing(3), "red")

    def test_len(self):
        self.blockDict.addBlock(self.block1)
        self.assertEqual(self.blockDict.len(), 1)

if __name__ == '__main__':
    unittest.main()