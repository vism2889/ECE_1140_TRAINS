from time import sleep
from winserver import winserver
from track_msg import track_msg

class PublisherCTC:
    def __init__(self):
        self.node = winserver('PublisherCTC')
        self.trackMsg = track_msg()
        self.trackPub = self.node.advertise('trackMsg', track_msg, 1)
    
    def publishTrackMsg(self):
        self.trackMsg.occupancy.append(True)
        self.trackMsg.switchStates.append(True)
        self.trackMsg.maintenance.append(True)
        self.trackMsg.failures.append(28)
        self.line = "red"
        self.trackPub.publish(self.trackMsg)

if __name__ == '__main__':
    mp = PublisherCTC()

    while True:
        mp.publishTrackMsg()
        sleep(1)