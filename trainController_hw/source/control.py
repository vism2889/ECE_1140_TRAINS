##############################################################################
# AUTHOR:   Juin Sommer
# DATE:     11/17/2022
# FILENAME: control.py
# DESCRIPTION:
# Class to define the Train Controller functionality and define GPIO outputs
# for the RPi

# TODO:
# - Generate new message files to take authority as a distance
# - implement failure states
#   + failure indicators
#   + stop train 
# - Implement speed limit 
#   + train cannot exceed speed limit
# - Implement next station
#   + display next station
#   + use next station for announcements 
# - Implement authority
#   + stop train when authority is reached
# - Implement station announcement audio for green line
##############################################################################

import RPi.GPIO as GPIO
from simple_pid import PID
from pygame import mixer
from outputData import OutputData
from trainData import TrainData

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# outputs
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW) # internal lights
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW) # external lights
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW) # left door
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) # right door

mixer.init()

class Control():
    def __init__(self):
        self.output = OutputData()
        self.input = TrainData()
        self.authority = 0
        self.light_state_internal = False
        self.light_state_external = False
        self.door_state_left = False
        self.door_state_right = False
        self.announce_state = False
        self.commanded_speed = 0
        self.ebrakeCommand = False
        self.brakeCommand = False
        self.current_speed = 0
        self.speed_limit = 100
        self.temperature = 0
        self.k_p = 24e3
        self.k_i = 100
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed) # initialize pid with fixed values
        self.pid.output_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW
        self.power = 0.0
        self.station_audio = ["shadyside_herron.mp3", "herron_swissvale.mp3", 
                              "swissvale_penn.mp3", "penn_steelplaza.mp3", 
                              "steelplaza_first.mp3","first_stationSquare.mp3", 
                              "stationSquare_southHills.mp3"]
        self.station_names = ["Shadyside", "Herron Ave.", "Swissvale", 
                              "Penn Station", "Steel Plaza", "First Ave",
                              "Station Square", "South Hills Junction"]
        
    def initializePID(self, kp_val, ki_val):
        self.k_p = kp_val
        self.k_i = ki_val
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed)
        self.pid.output_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    # need to confirm what data type authority will be
    def setAuthority(self, authority=None):
        if(authority==None):
            self.authority = self.input.getAuthority()
            return
        
        self.authority = authority
    
    def setInternalLights(self, light_state):
        self.light_state_internal = light_state

        if(self.light_state_internal): GPIO.output(14, GPIO.HIGH)
        if(not self.light_state_internal): GPIO.output(14, GPIO.LOW)

        self.output.setInternalLightState(self.light_state_internal)
        
    def setExternalLights(self, light_state):
        self.light_state_external = light_state

        if(self.light_state_external): GPIO.output(15, GPIO.HIGH)
        if(not self.light_state_external): GPIO.output(15, GPIO.LOW)

        self.output.setExternalLightState(self.light_state_external)

    def setLeftDoor(self, door_state):
        self.door_state_left = door_state

        if(self.door_state_left): GPIO.output(23, GPIO.HIGH)
        if(not self.door_state_left): GPIO.output(23, GPIO.LOW)

        self.output.setLeftDoor(self.door_state_left)

    def setRightDoor(self, door_state):
        self.door_state_right = door_state

        if(self.door_state_right): GPIO.output(24, GPIO.HIGH)
        if(not self.door_state_right): GPIO.output(24, GPIO.LOW)

        self.output.setRightDoorState(self.door_state_right)

    def setSpeed(self, commanded_speed=None):
        if(commanded_speed==None):
            speed = self.input.getCommandedSpeed()
            if(speed != None):
                self.commanded_speed = speed

        else:
            self.commanded_speed = commanded_speed
            
    # can remove after testing
    def setCurrentSpeed(self, current_speed=None):
        speed = self.input.getCurrentSpeed()
        if(current_speed==None and speed != None):
            self.current_speed = speed
            return self.current_speed
        else:
            return 0

    def setTemperature(self, temperature):
        if temperature != None:
            self.temperature = temperature
        
        self.output.setTemperatureValue(self.temperature)

    # need to refactor to take in next station data from train model
    def announceStation(self, start, file_idx):
        self.output.setAnnounceState(start)
        mixer.music.load("audio/" +  self.station_audio[file_idx])
        if(start) : mixer.music.play()
        if(not start) : mixer.music.stop()

    def deployEbrake(self, deploy=None):
        if deploy != None:
            self.ebrakeCommand = deploy
            self.output.setEbrakeState(self.ebrakeCommand)

    def deployServiceBrake(self, deploy=None):
        if deploy != None:
            self.brakeCommand = deploy
            self.output.setServiceBrakeState(self.brakeCommand)

    # TODO: implement speed limit
    def limitSpeed(self, speed):
        speed_limit = self.input.getSpeedLimit()
        if(speed > speed_limit):
            return False
        
        else: return True

    def getSpeedLimit(self):
        limit = self.input.getSpeedLimit()
        if limit != None:
            print("\nSpeed Limit: %5.2f" % limit)

    # TODO: implement authority
    def checkAuthority(self):
        if self.authority == 0:
            self.deployEbrake(self)
    
    def set_kp_ki(kp_val, ki_val, self):
        self.k_p = kp_val
        self.k_i = ki_val

    def get_kp_ki(self):
        return self.k_p, self.k_i

    def getPowerOutput(self, commanded_speed=None):
        if self.ebrakeCommand == True or self.brakeCommand == True:
            self.output.setPower(0.0)
            return self.power
        
        if commanded_speed == None and self.input.getCommandedSpeed() != None:
            self.pid.setpoint = self.input.getCommandedSpeed()
            self.current_speed = self.input.getCurrentSpeed()

        elif commanded_speed != None:
            self.commanded_speed = commanded_speed
            self.pid.setpoint = self.commanded_speed

        self.power = self.pid(self.current_speed)
        self.output.setPower(self.power)
        return self.power

    # used for server interface testing to send dummy data to a client acting as train model
    def sendRandom(self):
        self.output.randomize()
        self.output.publish()

    def publish(self):
        self.output.publish()

    def subscribe(self):
        self.input.spinOnce()