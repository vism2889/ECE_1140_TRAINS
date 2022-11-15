import unittest
import sys
from trainControllerSoftware_MainWindow import Ui_TrainControllerSW_MainWindow as test
#from trainControllerSoftware_TestSecondWindow import Ui_Test_SecondWindow as test

class TestAuthority(unittest.TestCase):
    def test_getAuthority(self):
        test.__init__(test)
        test.setAuthorityDisplayValue(test, 10)
        self.assertIs(test.getAuthorityDisplayValue(test), 10)

class TestSpeedLimit(unittest.TestCase):
    def test_setSpeedLimit(self):
        test.__init__(test)
        test.setPowerFailureDisplayValue(test, False)
        test.setSpeedLimitDisplayValue(test, 60)
        self.assertTrue(test.getSpeedLimitDisplayValue(test), 60)
        
class TestPowerFailure(unittest.TestCase):
    def test_PowerFailureTrue(self):
        test.__init__(test)
        test.setPowerFailureDisplayValue(test, True)
        test.setSpeedLimitDisplayValue(test, 60)
        test.setSpeedDisplayValue(test, 40)
        self.assertTrue(test.getSpeedDisplayValue(test), 0)
        
    def test_PowerFailureFalse(self):
        test.__init__(test)
        test.setPowerFailureDisplayValue(test, True)
        test.setSpeedLimitDisplayValue(test, 60)
        test.setSpeedDisplayValue(test, 40)
        self.assertTrue(test.getSpeedDisplayValue(test), 40)
        
class TestCommandedSpeed(unittest.TestCase):
    def test_speedBelowLimit(self):
        test.__init__(test)
        test.setSpeedLimitDisplayValue(test, 60)
        test.setSpeedDisplayValue(test, 50)
        self.assertIs(test.getSpeedDisplayValue(test), 50)
    
    def test_speedAboveLimit(self):
        test.__init__(test)
        test.setSpeedLimitDisplayValue(test, 60)
        test.setSpeedDisplayValue(test, 70)
        self.assertIs(test.getSpeedDisplayValue(test), 60)
    

if __name__ == '__main__':
    unittest.main()