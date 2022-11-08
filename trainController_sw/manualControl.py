import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from simple_pid import PID

class ManualControl(object):
    def __init__(self):
        self.current_speed = 0
        self.commanded_speed = 0
        self.suggested_speed = 0
        self.temperature = 0
        self.speed_limit = 100
        self.door_state_left = False
        self.door_state_right = False
        self.light_state_internal = False
        self.light_state_external = False
        self.authority = [True, True, True, True, True, True]
        self.announce_state = False
        self.advertisement_state = False
        self.service_brake_state = False
        self.emergency_brake_state = False
        
        self.k_p = 0
        self.k_i = 0
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed) # initialize pid with fixed values
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW
        self.power = 0
    
    def initializePID(self, kp_val, ki_val):
        self.k_p = kp_val
        self.k_i = ki_val
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed)
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW
    
    # Sets
    def setCommandedSpeed(self, commanded_speed):
        self.commanded_speed = commanded_speed
        print(self.commanded_speed)
    
    def setServiceBrake(self, brake_state):
        self.service_brake_state = brake_state
        print(self.service_brake_state)
    
    def setEmergencyBrake(self, brake_state):
        self.emergency_brake_state = brake_state
        print(self.emergency_brake_state)
    
    def setTemperature(self, temperature):
        self.temperature = temperature
        print(self.temperature)
            
    def setInternalLights(self, light_state):
        self.light_state_internal = light_state
        
    def setExternalLights(self, light_state):
        self.light_state_external = light_state

    def setLeftDoor(self, door_state):
        self.door_state_left = door_state

    def setRightDoor(self, door_state):
        self.door_state_right = door_state

    def setAdvertisements(self, advertisement_state):
        self.advertisement_state = advertisement_state
    
    def setAnnouncements(self, announcements_state):
        self.announce_state = announcements_state
    
    # Gets
    def getCommandedSpeed(self):
        return self.commanded_speed
    
    def getServiceBrake(self):
        return self.service_brake_state
    
    def getEmergencyBrake(self):
        return self.emergency_brake_state
    
    def getTemperature(self):
        return self.temperature
            
    def getInternalLights(self):
        return self.light_state_internal
        
    def getExternalLights(self):
        return self.light_state_external

    def getLeftDoor(self):
        return self.door_state_left

    def getRightDoor(self):
        return self.door_state_right

    def getAdvertisements(self):
        return self.advertisement_state
    
    def getAnnouncements(self):
        return self.announce_state
        
    # Power Calculations
    def setSpeed(self, speed):
        if(self.limitSpeed(self, speed)):
            self.commanded_speed = speed
            #output.setCommandedSpeed(output, self.commanded_speed)
            #output.setSpeedLimit(output, self.speed_limit)
    
    def setPower(self, power):
        self.power = power

    def limitSpeed(self, speed):
        if(speed > self.speed_limit):
            return False
        
        else: return True

    def checkAuthority(self):
        if self.authority == 0:
            self.deployEbrake(self)
        #output.setAuthority(output, self.authority)
    
    def set_kp_ki(kp_val, ki_val, self):
        self.k_p = kp_val
        self.k_i = ki_val

    def get_kp_ki(self):
        return self.k_p, self.k_i

    def getPowerOutput(self):
        self.pid.setpoint = self.commanded_speed
        self.power = self.pid(self.current_speed)
        if self.power > 0:
            return self.power
        
        else:
            self.power = 0
            return self.power

    def publish(self):
        #output.publish(output)
        pass