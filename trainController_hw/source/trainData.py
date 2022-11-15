from winserver import winserver
from in_msg import in_msg
import random 
import time

class TrainData:
    def __init__(self):
        self.node = winserver('my_subscriber', "192.168.0.15")
        self.sub = self.node.subscribe('input', in_msg, self.my_callback, 1)
        self.current_speed = None
        self.commanded_speed = None
        self.speed_limit = None
        self.authority = []
        self.brake_failure = None
        self.engine_failure = None
        self.signalPickup_failure = None

    def my_callback(self, msg): 
        self.current_speed = msg.current_speed
        self.commanded_speed = msg.commanded_speed
        self.speed_limit = msg.speed_limit
        self.authority.append(msg.authority)
        self.announce_command = msg.announce_command
        self.brake_failure = msg.brake_failure
        self.engine_failure = msg.engine_failure
        self.signalPickup_failure = msg.signalPickup_failure

    
    def getCurrentSpeed(self):
        return self.current_speed

    def getCommandedSpeed(self):
        return self.commanded_speed
    
    def getSpeedLimit(self):
        return self.speed_limit

    def getAuthority(self):
        return self.authority

    def getFailure(self):
        failure_states = [self.brake_failure, self.engine_failure, self.signalPickup_failure]
        return failure_states

    def spin(self):
        self.node.spin()
    
    def spinOnce(self):
        self.node.spinOnce()

if __name__ == '__main__':
    input = TrainData()
    while True:
        input.spinOnce()
        time.sleep(.1)
