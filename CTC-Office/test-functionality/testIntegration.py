import unittest
from PyQt5 import QtWidgets
from CTCOffice import CTCOffice
from Signals import Signals

class TestCTCOffice(unittest.TestCase):

    def setUp(self):
        # Create a QApplication instance that can be used to create
        # GUI elements in the test cases.
        self.app = QtWidgets.QApplication([])

        # Create a CTCOffice instance that will be tested.
        self.ctc = CTCOffice()

    def testLayout(self):
        # Test that the setupLayout method correctly parses the track layout file
        # and initializes the list of blocks for each train line.
        self.ctc.setupLayout()
        self.assertTrue(len(self.ctc.redLineBlocks) > 0)
        self.assertTrue(len(self.ctc.greenLineBlocks) > 0)

    def testUi(self):
        # Test that the setupUi method correctly sets up the GUI elements
        # and arranges them in the correct layout.
        self.ctc.setupUi()
        # Check that the window title is set to "CTC Office".
        self.assertEqual(self.ctc.windowTitle(), "CTC Office")
        # Check that the window has the expected size.
        self.assertEqual(self.ctc.size(), QSize(1200, 800))
        # Check that the dispatch button is present and has the expected text.
        self.assertTrue(self.ctc.dispatchButton)
        self.assertEqual(self.ctc.dispatchButton.text(), "Dispatch")

    def testOccupancySignal(self):
        # Test that the readOccupancySignal method correctly updates the GUI
        # to show the current occupancy status of each block.
        # Set up the GUI.
        self.ctc.setupUi()
        # Emit a signal with the occupancy status of some blocks.
        self.ctc.signals.globalOccupancyFromTrackModelSignal.emit({
            "Red": {
                "1": True,
                "2": False,
            },
            "Green": {
                "3": True,
                "4": False,
            }
        })
        # Check that the GUI shows the correct occupancy status for each block.
        self.assertEqual(self.ctc.blockList["Red"]["1"].text(), "OCCUPIED")
        self.assertEqual(self.ctc.blockList["Red"]["2"].text(), "UNOCCUPIED")
        self.assertEqual(self.ctc.blockList["Green"]["3"].text(), "OCCUPIED")
        self.assertEqual(self.ctc.blockList["Green"]["4"].text(), "UNOCCUPIED")

    def testSwitchState(self):
        # Test that the updateSwitchState method correctly updates the GUI
        # to show the current state of each switch.
        # Set up the GUI.
        self.ctc.setupUi()
        # Emit a signal with the state of some switches.
        self.ctc.signals.switchState.emit({
            "Red": {
                "1": True,
                "2": False,
            },
            "Green": {
                "3": True,
                "4": False,
            }
        })
        # Check that the GUI shows the correct state for each switch.
        self.assertEqual(self.ctc.switchList["Red"]["1"].text(), "CLOSED")
        self.assertEqual(self.ctc.switchList["Red"]["2"].text(), "OPEN")
        self.assertEqual(self.ctc.switchList["Green"]["3"].text(), "CLOSED")
        self.assertEqual(self.ctc.switchList["Green"]["4"].text(), "OPEN")

    def testClockSpeed(self):
        # Test that the changeClockSpeed method correctly updates the clock
        # display in the GUI to show the current simulation time.
        # Set up the GUI.
        self.ctc.setupUi()
        # Emit a signal with the current simulation time.
        self.ctc.signals.clockSpeedSignal.emit("12:34:56")
        # Check that the GUI shows the correct simulation time.
        self.assertEqual(self.ctc.clockDisplay.text(), "12:34:56")

    def testAuthority(self):
        # Test that the showAuthority method correctly updates the GUI
        # to show the current authority granted to each train.
        # Set up the GUI.
        self.ctc.setupUi()
        # Emit a signal with the authority granted to some trains.
        self.ctc.signals.waysideAuthority.emit({
            "Red": {
                "1": 50,
                "2": 75,
            },
            "Green": {
                "3": 100,
                "4": 125,
            }
        })
        # Check that the GUI shows the correct authority for each train.
        self.assertEqual(self.ctc.trainAuthority["Red"]["1"].text(), "50")
        self.assertEqual(self.ctc.trainAuthority["Red"]["2"].text(), "75")
        self.assertEqual(self.ctc.trainAuthority["Green"]["3"].text(), "100")
        self.assertEqual(self.ctc.trainAuthority["Green"]["4"].text(), "125")

    def testFaults(self):
        # Test that the readFaultSignal method correctly updates the GUI
        # to show any track failures in the system.
        # Set up the GUI.
        self.ctc.setupUi()
        # Emit a signal with some track failures.
        self.ctc.signals.trackFailuresSignal.emit({
            "Red": ["1", "2"],
            "Green": ["3"],
        })
        # Check that the GUI shows the correct track failures for each train line.
        self.assertEqual(self.ctc.trackFailures["Red"].text(), "1, 2")
        self.assertEqual(self.ctc.trackFailures["Green"].text(), "3")

    def testDispatchSignal(self):
        # Test that the dispatchSignal signal is emitted when the dispatch
        # button is clicked.
        # Set up the GUI.
        self.ctc.setupUi()
        # Create a mock object that will be used to receive the signal.
        mock = unittest.mock.Mock()
        # Connect the signal to the mock object.
        self.ctc.dispatchSignal.connect(mock)
        # Click the dispatch button.
        QTest.mouseClick(self.ctc.dispatchButton, Qt.LeftButton)
        # Check that the signal was emitted.
        self.assertTrue(mock.called)

    def testAddTrain(self):
        # Test that the addTrain method correctly adds a new train to the GUI.
        # Set up the GUI.
        self.ctc.setupUi()
        # Add a new train to the GUI.
        self.ctc.addTrain("Red", "1", "2")
        # Check that the new train is present in the GUI.
        self.assertEqual(self.ctc.trainList["Red"]["1"].text(), "2")

    def testRemoveTrain(self):
        # Test that the removeTrain method correctly removes a train from the GUI.
        # Set up the GUI.
        self.ctc.setupUi()
        # Add a new train to the GUI.
        self.ctc.addTrain("Red", "1", "2")
        # Remove the train from the GUI.
        self.ctc.removeTrain("Red", "1")
        # Check that the train is no longer present in the GUI.
        self.assertFalse("1" in self.ctc.trainList["Red"])

    def testUpdateTrainPosition(self):
        # Test that the updateTrainPosition method correctly updates
        # the position of a train in the GUI.
        # Set up the GUI.
        self.ctc.setupUi()
        # Add a new train to the GUI.
        self.ctc.addTrain("Red", "1", "2")
        # Update the position of the train.
        self.ctc.updateTrainPosition("Red", "1", "3")
        # Check that the GUI shows the correct position for the train.
        self.assertEqual(self.ctc.trainList["Red"]["1"].text(), "3")


if __name__ == '__main__':
    unittest.main()

