import random
from time import sleep
from winserver import winserver
from TrackMsg import TrackMsg ## Generated Message

class MyPub:
    def __init__(self):
        
        self.node = winserver('TrackMsg Publisher')
        
        self.msg  = TrackMsg()

        self.pub  = self.node.advertise('TrackMsg Topic', TrackMsg, 1)

    def publishRand(self):
        self.msg.occupancy = []
        self.msg.switchStates = []
        self.msg.maintenance = []
        self.msg.failures = []
        ## Randomize a list of booleans
        for i in range(150):
            self.msg.occupancy.append(random.choice([True, False]))
            self.msg.switchStates.append(random.choice([True, False]))
            self.msg.maintenance.append(random.choice([True, False]))
            self.msg.failures.append(random.choice([0,1,2]))
        self.msg.line = "Green"

        ## Publish the message to any subscribers
        self.pub.publish(self.msg)


if __name__ == '__main__':

    mp = MyPub()

    while True:
        mp.publishRand()        
        sleep(1.0) ## Publish every 1.0 seconds