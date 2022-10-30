import unittest
from control import Control as c
from manualControl import ManualControl as mc

class Test_commandedSpeed(unittest.TestCase):

    def test_speedBelowLimit(self):
        c.__init__(c)
        c.setSpeedLimit(c, 60)
        c.setSpeed(c, 50)
        self.assertIs(c.getSpeed(c), 50)

    def test_speedAboveLimit(self):
        c.__init__(c)
        c.setSpeedLimit(c, 60)
        c.setSpeed(c, 50)
        c.setSpeed(c, 70)
        self.assertIs(c.getSpeed(c), 50)

class Test_restrictions(unittest.TestCase):

    def test_getAuthority(self):
        c.__init__(c)
        c.setAuthority(c, 10)
        self.assertIs(c.getAuthority(c), 10)

    def test_speedLimit(self):
        c.__init__(c)
        c.setSpeedLimit(c, 60)
        self.assertTrue(c.limitSpeed(c, 50))
        self.assertFalse(c.limitSpeed(c, 70))
        

if __name__ == '__main__':
    unittest.main()