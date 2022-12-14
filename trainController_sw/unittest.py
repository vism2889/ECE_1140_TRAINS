import unittest
from PyQt5.QtWidgets import QApplication

class TestTrainControllerSW_MainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = Ui_TrainControllerSW_MainWindow()

    def tearDown(self):
        self.window = None
        self.app.quit()

    def test_setTrainIDSignal(self):
        self.window.setTrainIDSignal('T1')
        self.assertEqual(self.window.trainID, 'T1')

    def test_setCurrentSpeedSignal(self):
        self.window.setCurrentSpeedSignal(40)
        self.assertEqual(self.window.currentSpeed, 40)

    def test_setAuthoritySignal(self):
        self.window.setAuthoritySignal(400)
        self.assertEqual(self.window.authority, 400)

    def test_setBlockFailuresSignal(self):
        self.window.setBlockFailuresSignal(True)
        self.assertTrue(self.window.blockFailures)

    def test_setSpeedLimitSignal(self):
        self.window.setSpeedLimitSignal(60)
        self.assertEqual(self.window.speedLimit, 60)

    def test_setCommandedSpeedSignal(self):
        self.train_controller.setCommandedSpeedSignal(100)
        self.assertEqual(self.train_controller.commandedSpeedSignal, 100)
        self.train_controller.setCommandedSpeedSignal(50)
        self.assertEqual(self.train_controller.commandedSpeedSignal, 50)

    def test_setTrainFailuresSignal(self):
        self.train_controller.setTrainFailuresSignal('Train failure')
        self.assertEqual(self.train_controller.trainFailuresSignal, 'Train failure')
        self.train_controller.setTrainFailuresSignal('Power failure')
        self.assertEqual(self.train_controller.trainFailuresSignal, 'Power failure')

    def test_setBeaconSignal(self):
        self.assertEqual(self.ui.setBeaconSignal("Beacon signal received"), "Beacon signal received")

    def test_checkCurrentSpeed(self):
        self.assertEqual(self.ui.checkCurrentSpeed("40"), "40")

    def test_checkFailures(self):
        self.assertTrue(self.ui.checkFailures())

    def test_setAutoCommandedSpeed(self):
        self.assertEqual(self.ui.setAutoCommandedSpeed("50"), "50")

    def test_setAutoSpeedLimit(self):
        self.assertEqual(self.ui.setAutoSpeedLimit("60"), "60")

    def test_setAutoServiceBrake(self):
        self.assertEqual(self.ui.setAutoServiceBrake("On"), "On")

    def test_setAutoTemperature(self):
        self.assertEqual(self.ui.setAutoTemperature("70"), "70")

    def test_setAutoLights(self):
        self.assertEqual(self.ui.setAutoLights("On"), "On")

    def test_setAutoDoors(self):
        self.train_controller.setAutoDoors(True)
        self.assertTrue(self.train_controller.auto_doors)
        self.train_controller.setAutoDoors(False)
        self.assertFalse(self.train_controller.auto_doors)

    def test_setStationName(self):
        self.train_controller.setStationName("Test Station")
        self.assertEqual(self.train_controller.station_name, "Test Station")

    def test_setBlockFailures(self):
        self.train_controller.setBlockFailures("Test failure message")
        self.assertEqual(self.train_controller.block_failures, "Test failure message")

    def test_setManualControl_CommandedSpeed(self):
        self.train_controller.setManualControl_CommandedSpeed(100)
        self.assertEqual(self.train_controller.commanded_speed, 100)

    def test_setManualControl_ServiceBrake(self):
        self.train_controller.setManualControl_ServiceBrake(True)
        self.assertTrue(self.train_controller.service_brake)
        self.train_controller.setManualControl_ServiceBrake(False)
        self.assertFalse(self.train_controller.service_brake)

    def test_setManualControl_EmergencyBrake(self):
        self.ui.setManualControl_EmergencyBrake(True)
        self.signals.send.assert_called_with('emergency_brake', True)

    def test_setManualControl_Temperature(self):
        self.train_controller.setManualControl_Temperature(20)
        self.assertEqual(self.signals.temperature, 20)

    def test_setManualControl_Lights(self):
        self.train_controller.setManualControl_Lights(True)
        self.assertEqual(self.signals.lights, True)

    def test_setManualControl_Doors(self):
        self.train_controller.setManualControl_Doors(True)
        self.assertEqual(self.signals.doors, True)

    def test_setManualControl_Advertisements(self):
        self.train_controller.setManualControl_Advertisements(True)
        self.assertEqual(self.signals.advertisements, True)

    def test_setManualControl_Announcements(self):
        self.train_controller.setManualControl_Announcements(True)
        self.assertEqual(self.signals.announcements, True)



write a test suite in python for the same class above that tests setCommandedSpeedSignal(self, msg), setTrainFailuresSignal(self, msg), setBeaconSignal(self, msg), checkCurrentSpeed(self, msg), checkFailures(self), setAutoCommandedSpeed(self), setAutoSpeedLimit(self), setAutoServiceBrake(self), setAutoTemperature(self), setAutoLights(self), setAutoDoors(self), setStationName(self), setBlockFailures(self, msg), setManualControl_CommandedSpeed(self), setManualControl_ServiceBrake(self), setManualControl_EmergencyBrake(self), setManualControl_Temperature(self), setManualControl_Lights(self), setManualControl_Doors(self), setManualControl_Advertisements(self), setManualControl_Announcements(self), ActivateEmergencyBrake(self), setPID(self), setAuthority(self), safeBrakingDistance(self)

