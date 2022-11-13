from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
import time
import random

class dummyTrain():
    #occupancySignal  = QtCore.pyqtSignal(list)  # <-- This is the sub window's signal
    def __init__(self):
        super().__init__()

        self.blocks    = [i for i in range(10)]
        self.blockLens = [random.randint(10,25) for i in range(10)]
        print(self.blocks)
        print(self.blockLens)
        self.distance = 0
        self.currBlockIndex = 0
        self.timerr = 0
        self.occupancy = [0 for i in range(10)]

    def timer(self):
        while self.currBlockIndex != 24:
            speed = 50
            self.timerr += .01
            self.distance = speed*self.timerr
            print("distance:", self.distance)
            self.getOccupancy()
            time.sleep(0.01)

    def getOccupancy(self):
        
        if self.distance >= self.blockLens[self.currBlockIndex]:
            #print("NEW BLOCK")
            self.currBlockIndex += 1
            self.distance = 0
            self.timerr = 0
            self.occupancy[self.currBlockIndex-1] =0
            self.occupancy[self.currBlockIndex] = 1
            print("OCCUPANCY:", self.occupancy)
           # occupancySignal = self.occupancy
            
            #self.occupancySignal.emit(self.occupancy)
        
        print("currBlock is", self.currBlockIndex)

train = dummyTrain()
train.timer()