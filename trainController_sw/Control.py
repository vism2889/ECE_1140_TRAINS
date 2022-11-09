import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from simple_pid import PID

from outputData import OutputData
from trainData import TrainData

class Control():
    def __init__(self):
        self.input = TrainData()
        self.output = OutputData()
        
        self.authority = [True, True, True, True, True, True]
        self.light_state_internal = False
        self.light_state_external = False
        self.door_state_left = False
        self.door_state_right = False
        self.announce_state = False
        self.advertisement_state = False
        self.commanded_speed = 0
        self.service_brake = False
        self.emergency_brake = False
        self.current_speed = 0
        self.suggested_speed = 0
        self.speed_limit = 100
        self.temperature = 0
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
    def setAuthority(self, authority=None):
        if(authority==None):
            self.authority = self.input.getAuthority()
            return
        self.authority = authority
    
    def setInternalLights(self, light_state=None):
        if(light_state == None):
            self.light_state_internal = self.input.getInternalLightCommand()
        else: self.light_state_internal = light_state
        self.output.setInternalLightState(self.light_state_internal)
        
    def setExternalLights(self, light_state=None):
        if(light_state == None):
            self.light_state_external = self.input.getInternalLightCommand()

        else: self.light_state_external = light_state
        self.output.setExternalLightState(self.light_state_external)

    def setLeftDoor(self, door_state=None):
        if(door_state == None):
            self.door_state_left = input.getLeftDoorCommand(input)

        else: self.door_state_left = door_state
        self.output.setLeftDoor(self.door_state_left)

    def setRightDoor(self, door_state=None):
        if(door_state==None):
            self.door_state_right = input.getRightDoorCommand(input)

        else: self.door_state_right = door_state
        self.output.setRightDoorState(self.door_state_right)
        
    def setSpeed(self, speed=None):
        if(speed==None):
            self.commanded_speed = self.input.getCommandedSpeed(input)

        if(self.limitSpeed(self, speed)):
            self.getPowerOutput(speed, self.input.getCurrentSpeed()) # function sends power data out

    def setServiceBrake(self, brake=None):
        if(brake == None):
            self.service_brake = self.input.getServiceBrakeCommand()
        else:
            self.service_brake = brake
        self.output.setServiceBrakeState(self.service_brake)
    
    def setTemperature(self, temperature=None):
        if(temperature == None):
            self.temperature = input.getTemperature(input)

        else: self.temperature = temperature

        self.output.setTemperature(self.setTemperature)

    
    def setAdvertisements(self, advertisement=None):
        if(advertisement == None):
            #self.advertisement_state = input.getAdvertisement(input)
            pass
        else: 
            self.advertisement_state = advertisement
        self.output.setAdvertisementState(self.advertisement_state)
    
    def setAnnouncements(self, announcement=None):
        if(announcement == None):
            self.announce_state = input.getAnnounceCommand(input)
        else:
            self.announce_state = announcement
        self.output.setAnnounceState(self.announce_state)
    
    def setEmergencyBrake(self, ebrake=None):
        if(ebrake == None):
            self.emergency_brake = self.input.getEbrakeCommand()
        else:
            self.emergency_brake = ebrake
        self.output.setEbrakeState(self.emergency_brake)

####### Can remove after Testing
    def setSpeedLimit(self, speed_limit=None):
        if(speed_limit==None):
            self.speed_limit = self.input.getSpeedLimit()
            return

        self.speed_limit = speed_limit
        self.output.setSpeedLimit(self.speed_limit)

    def setCurrentSpeed(self, current_speed=None):
        if(current_speed==None):
            self.current_speed = self.input.getCurrentSpeed()
            return

        self.current_speed = current_speed
        
    def setSuggestedSpeed(self, suggested_speed=None):
        if(suggested_speed == None):
            self.suggested_speed = self.input.getSuggestedSpeed()
            return 

        self.suggested_speed = suggested_speed

    # need to refactor to take in next station data from train model
    def announceStation(self, start, file_idx):
        self.output.setAnnounceState(start)

    def deployEbrake(self):
        # may have to consider case where if in auto mode and ebrake is deployed, stop taking in commanded speed data 
        self.output.setEbrakeState(True)
        self.output.setPower(0)


    def limitSpeed(self, speed):
        speed_limit = self.input.getSpeedLimit()
        if(speed > speed_limit):
            return False
        
        else: return True

    def checkAuthority(self):
        if self.authority == 0:
            self.deployEbrake(self)
        self.output.setAuthority(self.authority)
    
    def set_kp_ki(kp_val, ki_val, self):
        self.k_p = kp_val
        self.k_i = ki_val

    # Gets
    def getAuthority(self):
        return self.authority
    
    def getInternalLights(self):
        return self.light_state_internal
        
    def getExternalLights(self):
        return self.light_state_external

    def getLeftDoor(self):
        return self.door_state_left

    def getRightDoor(self):
        return self.door_state_right
        
    def getTemperature(self):
        return self.setTemperature

    def getServiceBrake(self):
        return self.service_brake
    
    def getAdvertisements(self):
        return self.advertisement_state
    
    def getAnnouncements(self):
        return self.announce_state

    def getEmergencyBrake(self):
        return self.emergency_brake
    
    def getSpeedLimit(self):
        return self.speed_limit

    def getCurrentSpeed(self):
        return self.current_speed
        
    def getSuggestedSpeed(self):
        return self.suggested_speed

    def getCommandedSpeed(self):
        return self.commanded_speed

    def get_kp_ki(self):
        return self.k_p, self.k_i
    
    def getSpeed(self): 
        return self.commanded_speed

    def getPowerOutput(self, commanded_speed, current_speed):
        self.pid.setpoint = commanded_speed
        self.power = self.pid(current_speed)
        if self.power > 0:
            self.output.setPower(self.power)
        
        else:
            self.power = 0
            self.output.setPower(self.power)
    
    # We need to get values for the faults!
    
    #Winserver
    def publish(self):
        self.output.publish()

    def subscribe(self):
        self.input.spinOnce()