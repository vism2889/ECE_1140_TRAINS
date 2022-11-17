##############################################################################
# AUTHOR:   Juin Sommer
# DATE:     11/17/2022
# FILENAME: outputData.py
# DESCRIPTION:
# Class to handle Train Controller output data to send to Train Model with
# the winserver using TCP/IP via ethernet.
##############################################################################

import random
import time
from winserver import winserver
import sys
sys.path.append("../server_interfaces")
from out_msg import out_msg

class OutputData():
    def __init__(self):
        self.node = winserver('my_publisher', "192.168.0.15")
        self.message = out_msg()
        self.pub = self.node.advertise('my_topic', out_msg , 1, "192.168.0.10")

    def setPower(self, power):
        self.message.power = power

    def setTemperatureValue(self, temp):
        self.message.temperature = temp

    def setAnnounceState(self, state):
        self.message.announcement_states = state

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

        # print("Power: %5.2f" % self.message.power, end="", flush=True )
        # print("\nTemperature: %2d" % self.message.temperature, end="", flush=True )
        # print("\nService Brake: %i" % self.message.service_brake_command, end="", flush=True )
        # print("\nEmergencyBrake: %i" % self.message.ebrake_command, end="", flush=True )
        # print("\nLeft Door: %i" % self.message.left_door_state, end="", flush=True )
        # print("\nRight Door: %i" % self.message.right_door_state, end="", flush=True )
        # print("\nInternal Lights: %i" % self.message.internal_light_state, end="", flush=True )
        # print("\nExternal Lights: %i" % self.message.external_light_state, end="", flush=True )

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
        time.sleep(.1)





    