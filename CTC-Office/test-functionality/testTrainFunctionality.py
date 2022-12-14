import sys
sys.path.append('../train-functionality/')

import copy
import unittest
from Train import Train
from TrainDictionary import TrainDictionary


class TrainDictionaryTest(unittest.TestCase):

    def setUp(self):
        self.testTrainDict = TrainDictionary()

    def test_addTrain(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addTrain('Train1', destinations, 10, 20)
        self.assertEqual(self.testTrainDict.trainList['Train1'].destinations, destinations)
        self.assertEqual(self.testTrainDict.trainList['Train1'].suggestedSpeed, 10)
        self.assertEqual(self.testTrainDict.trainList['Train1'].authority, 20)

    def test_addScheduledTrain(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addScheduledTrain('Train2',destinations, 10, 20)
        self.assertEqual(self.testTrainDict.backLog['Train2'].destinations, destinations)
        self.assertEqual(self.testTrainDict.backLog['Train2'].suggestedSpeed, 10)
        self.assertEqual(self.testTrainDict.backLog['Train2'].authority, 20)

    def test_dispatchScheduledTrain(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addScheduledTrain('Train2', destinations, 10, 20)
        self.testTrainDict.dispatchScheduledTrain('Train2', 'Train3')
        self.assertEqual(self.testTrainDict.trainList['Train3'].destinations, destinations)
        self.assertEqual(self.testTrainDict.trainList['Train3'].suggestedSpeed, 10)
        self.assertEqual(self.testTrainDict.trainList['Train3'].authority, 20)

class TrainDictionaryTest(unittest.TestCase):

    def setUp(self):
        self.testTrainDict = TrainDictionary()

    def test_addTrain(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addTrain('Train1', destinations, 10, 20)
        self.assertEqual(self.testTrainDict.trainList['Train1'].destinations, destinations)
        self.assertEqual(self.testTrainDict.trainList['Train1'].suggestedSpeed, 10)
        self.assertEqual(self.testTrainDict.trainList['Train1'].authority, 20)

    def test_addScheduledTrain(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addScheduledTrain('Train2', destinations, 10, 20)
        self.assertEqual(self.testTrainDict.backLog['Train2'].destinations, destinations)
        self.assertEqual(self.testTrainDict.backLog['Train2'].suggestedSpeed, 10)
        self.assertEqual(self.testTrainDict.backLog['Train2'].authority, 20)

    def test_dispatchScheduledTrain(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addScheduledTrain('Train2', destinations, 10, 20)
        self.testTrainDict.dispatchScheduledTrain('Train2', 'Train3')
        self.assertEqual(self.testTrainDict.trainList['Train3'].destinations, destinations)
        self.assertEqual(self.testTrainDict.trainList['Train3'].suggestedSpeed, 10)
        self.assertEqual(self.testTrainDict.trainList['Train3'].authority, 20)

    def test_setSuggestedSpeed(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addTrain('Train1', destinations, 10, 20)
        self.testTrainDict.setSuggestedSpeed('Train1', 10, 'Green Line', False)
        self.assertEqual(self.testTrainDict.getSuggestedSpeed('Train1'), 24.254333333333335)

    def test_toggleDestination(self):
        destinations = {'A':[1, False], 'B':[2, True], 'C':[3, False]}
        self.testTrainDict.addTrain('Train1', destinations, 10, 20)
        self.testTrainDict.toggleDestination('Train1', 'A', False)
        self.assertTrue(self.testTrainDict.trainList['Train1'].destinations['A'][1])

if __name__ == '__main__':
    unittest.main()