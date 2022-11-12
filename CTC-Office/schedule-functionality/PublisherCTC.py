from time import sleep
from winserver import winserver
from TrackMsg import TrackMsg

class PublisherCTC:
    def __init__(self):
        self.node = winserver('PublisherCTC')
        self.trackMsg = TrackMsg()
        self.trackPub = self.node.advertise('TrackMsg', TrackMsg, 1)
    
    def publishTrackMsg(self, switchStates, maintenance, line):
        self.trackMsg.occupancy = []
        self.trackMsg.switchStates = switchStates
        self.trackMsg.maintenance = maintenance
        self.trackMsg.failures = []
        self.line = line
        self.trackPub.publish(self.trackMsg)

if __name__ == '__main__':
    mp = PublisherCTC()

    while True:
        mp.publishTrackMsg([True, False], [False, True], "red")
        sleep(1)