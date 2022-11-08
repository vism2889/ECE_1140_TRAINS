import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from simple_pid import PID

from outputData import OutputData as output
from trainData import TrainData as input

class Control():
    def __init__(self):
        output.__init__(output)
        input.__init__(input)
        
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
            self.authority = input.getAuthority(input)
            return
        self.authority = authority
    
    def setInternalLights(self, light_state=None):
        if(light_state == None):
            self.light_state_internal = input.getInternalLightCommand(input)
        else: self.light_state_internal = light_state
        output.setInternalLightState(output, self.light_state_internal)
        
    def setExternalLights(self, light_state=None):
        if(light_state == None):
            self.light_state_external = input.getInternalLightCommand(input)

        else: self.light_state_external = light_state
        output.setExternalLightState(output, self.light_state_external)

    def setLeftDoor(self, door_state=None):
        if(door_state == None):
            self.door_state_left = input.getLeftDoorCommand(input)

        else: self.door_state_left = door_state
        output.setLeftDoor(output, self.door_state_left)

    def setRightDoor(self, door_state=None):
        if(door_state==None):
            self.door_state_right = input.getRightDoorCommand(input)

        else: self.door_state_right = door_state
        output.setRightDoorState(output, self.door_state_right)
        
    def setSpeed(self, speed=None):
        if(speed==None):
            speed = input.getCommandedSpeed(input)

        if(self.limitSpeed(self, speed)):
            self.getPowerOutput(speed, input.getCurrentSpeed(input)) # function sends power data out

    def setServiceBrake(self, brake=None):
        if(brake == None):
            self.service_brake = input.getServiceBrakeCommand(input)
        else:
            self.service_brake = brake
        output.setServiceBrakeState(output, self.service_brake)
    
    def setTemperature(self, temperature=None):
        if(temperature == None):
            self.temperature = input.getTemperature(input)

        else: self.temperature = temperature

        output.setTemperature(self.setTemperature)

    
    def setAdvertisements(self, advertisement=None):
        if(advertisement == None):
            #self.advertisement_state = input.getAdvertisement(input)
            pass
        else: 
            self.advertisement_state = advertisement
        #output.setAdvertisementState(output, self.advertisement_state)
    
    def setAnnouncements(self, announcement=None):
        if(announcement == None):
            self.announce_state = input.getAnnounceCommand(input)
        else:
            self.announce_state = announcement
        output.setAnnounceState(output, self.announce_state)
    
    def setEmergencyBrake(self, ebrake=None):
        if(ebrake == None):
            self.emergency_brake = input.getEbrakeCommand(input)
        else:
            self.emergency_brake = ebrake
        output.setEbrakeState(output, self.emergency_brake)

####### Can remove after Testing
    def setSpeedLimit(self, speed_limit=None):
        if(speed_limit==None):
            self.speed_limit = input.getSpeedLimit(input)
            return

        self.speed_limit = speed_limit
        output.setSpeedLimit(output, self.speed_limit)

    def setCurrentSpeed(self, current_speed=None):
        if(current_speed==None):
            self.current_speed = input.getCurrentSpeed(input)
            return

        self.current_speed = current_speed
        
    def setSuggestedSpeed(self, suggested_speed=None):
        if(suggested_speed == None):
            self.suggested_speed = input.getSuggestedSpeed(input)
            return 

        self.suggested_speed = suggested_speed

    # need to refactor to take in next station data from train model
    def announceStation(self, start, file_idx):
        output.setAnnounceState(output, start)

    def deployEbrake(self):
        # may have to consider case where if in auto mode and ebrake is deployed, stop taking in commanded speed data 
        output.setEbrakeState(output, True)
        output.setPower(output, 0)


    def limitSpeed(self, speed):
        speed_limit = input.getSpeedLimit(input)
        if(speed > speed_limit):
            return False
        
        else: return True

    def checkAuthority(self):
        if self.authority == 0:
            self.deployEbrake(self)
        output.setAuthority(output, self.authority)
    
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
            output.setPower(output, self.power)
        
        else:
            self.power = 0
            output.setPower(output, self.power)
    
    # We need to get values for the faults!
    
    #Winserver
    def publish(self):
        output.publish(output)

    def subscribe(self):
        input.spinOnce(input)