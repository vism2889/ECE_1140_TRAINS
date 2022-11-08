import random
import time
from winserver import winserver
from out_msg import out_msg

#ours
class OutputData():
    def __init__(self):
        self.node = winserver('my_publisher', "192.168.0.15")
        self.message = out_msg()
        self.pub = self.node.advertise('my_topic', out_msg , 1, "192.168.0.10")

    def setPower(self, power):
        self.message.power = power

    def setTemperature(self, temp):
        self.message.temperature = temp

    def setAnnounceState(self, state):
        self.message.announcement_state = state

    def setServiceBrakeState(self, state):
        self.message.service_brake_command = state

    def setEbrakeState(self, state):
        self.message.ebrake_command = state
    def setLeftDoor(self, state):
        self.message.left_door_state = state

    def setRightDoorState(self, state):
        self.message.right_door_state = state
    
    def setInternalLightState(self, state):
        self.message.internal_light_state = state
    
    def setExternalLightState(self, state):
        self.message.external_light_state = state

    def publish(self):
        self.pub.publish(self.message)

    def randomize(self):
        self.message.announcement_states = random.choice([True, False])
        self.message.power = random.randint(0,5)
        self.message.service_brake_command = random.choice([True, False])
        self.message.ebrake_command = random.choice([True, False])
        self.message.left_door_state = random.choice([True, False])
        self.message.right_door_state = random.choice([True, False])
        self.message.internal_light_state = random.choice([True, False])
        self.message.external_light_state = random.choice([True, False])
        self.message.temperature = random.randint(0,100)

if __name__ == '__main__':
    
    outdata = OutputData()
    
    while True:
        outdata.randomize()
        outdata.publish()
        time.sleep(1.0)