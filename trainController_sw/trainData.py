from winserver import winserver
from in_msg import in_msg
import random 
import time

class TrainData:
    def __init__(self):
        self.node = winserver('my_subscriber')
        self.sub = self.node.subscribe('input', in_msg, self.my_callback, 1)
        self.current_speed = None
        self.commanded_speed = None
        self.suggested_speed = None
        self.temperature = None
        self.speed_limit = None
        self.left_door_state = None
        self.right_door_state = None
        self.internal_light_state = None
        self.external_light_state = None
        self.authority = []
        self.announce_command = None
        self.service_brake_command = None
        self.ebrake_command = None

    def my_callback(self, msg):
        self.current_speed = msg.current_speed
        self.commanded_speed = msg.commanded_speed
        self.suggested_speed = msg.suggested_speed
        self.temperature = msg.temperature_command
        self.speed_limit = msg.speed_limit
        self.left_door_state = msg.left_door_command
        self.right_door_state = msg.right_door_command
        self.internal_light_state = msg.internal_light_command
        self.external_light_state = msg.external_light_command
        self.authority.append(msg.authority)
        self.announce_command = msg.announce_command
        self.service_brake_command = msg.service_brake_command
        self.ebrake_command = msg.ebrake_command
    
    def getCurrentSpeed(self):
        return self.current_speed

    def getCommandedSpeed(self):
        return self.commanded_speed
    
    def getSuggestedSpeed(self):
        return self.suggested_speed
    
    def getTemperature(self):
        return self.temperature

    def getSpeedLimit(self):
        return self.speed_limit

    def getLeftDoorCommand(self):
        return self.left_door_state

    def getRightDoorCommand(self):
        return self.right_door_state

    def getInternalLightCommand(self):
        return self.internal_light_state

    def getExternalLightCommand(self):
        return self.external_light_state

    def getAuthority(self):
        return self.authority

    def getAnnounceCommand(self):
        return self.announce_command

    def getServiceBrakeCommand(self):
        return self.service_brake_command

    def getEbrakeCommand(self):
        return self.ebrake_command

    def spin(self):
        self.node.spin()
    
    def spinOnce(self):
        self.node.spinOnce()

if __name__ == '__main__':
    input = TrainData()
    input.spin()