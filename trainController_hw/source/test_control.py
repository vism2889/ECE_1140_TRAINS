import unittest
import sys
from control import Control as c

class Test_commandedSpeedBelowLimit(unittest.TestCase):
    def speedBelowLimit(self):
        c.__init__(c)
        c.setSpeedLimit(60)
        c.setSpeed(50)
        self.assertIs(c.getSpeed(), 50)

    def speedAboveLimit(self):
        c.setSpeedLimit(60)
        c.setSpeed(50)
        c.setSpeed(70)
        self.assertIs(c.getSpeed(), 50)
