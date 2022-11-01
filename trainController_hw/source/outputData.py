import random
import time
from winserver import winserver
from tc_msg import tc_msg

class OutputData():
    def __init__(self):
        self.node = winserver('my_publisher', "192.168.0.15")
        self.message = tc_msg()
        self.pub = self.node.advertise('my_topic', tc_msg , 1, "192.168.0.10")

    def setCommandedSpeed(self, speed):
        self.message.commandedSpeed = speed

    def setCurrentSpeed(self, speed):
        self.message.currentSpeed = speed

    def setSpeedLimit(self, speed):
        self.message.speedLimit = speed

    def setAnnounceState(self, state):
        self.message.announcements = state

    def setAuthority(self, authority):
        self.message.authority.append(authority)

    def publish(self):
        self.pub.publish(self.message)

    def randomize(self):
        self.message.announcements = random.choice([True, False])

        self.message.authority.clear()        
        for i in range(10):
            self.message.authority.append(random.choice([True, False]))

        self.message.commandedSpeed = random.randint(0,5)
        self.message.currentSpeed = random.randint(0,5)
        self.message.speedLimit = random.randint(0,1000)

if __name__ == '__main__':
    
    outdata = OutputData()
    
    while True:
        outdata.randomize()
        outdata.publish()
        time.sleep(1.0)





    