##############################################################################
# AUTHOR:   Juin Sommer
# DATE:     11/17/2022
# FILENAME: manualControl.py
# DESCRIPTION:
# Class to define manual control functionality for the Train Driver UI
# interfacing with hardware (RPi GPIO). Defines inputs to RPi.
##############################################################################

import RPi.GPIO as GPIO
from time import sleep
from pygame import mixer
from control import Control
from analogInput import AnalogIn # class that handles analog input
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# inputs
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # internal lights
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # external lights
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # left door
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # right door
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # announce
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # ebrake

mixer.init()

# class that handles gpio for manual input from train driver
class ManualControl():

    def __init__(self, obj):
        self.c = obj
        self.anal_in = AnalogIn()
        self.commandedSpeed = 0
        self.c.setInternalLights(True)
        self.c.deployServiceBrake(False)
        self.station_audio = ["shadyside_herron.mp3", "herron_swissvale.mp3", 
                              "swissvale_penn.mp3", "penn_steelplaza.mp3", 
                              "steelplaza_first.mp3","first_stationSquare.mp3", 
                              "stationSquare_southHills.mp3"]

    def setCommandedSpeed(self):
        if self.c.ebrakeCommand == False and self.c.vital_override == False:
            speed = self.anal_in.getSpeedValue() / 2.3694
            if self.c.limitSpeed(self.c.current_speed): 
                self.commandedSpeed = speed 
        
            if self.c.operating_mode == False:
                self.c.getPowerOutput(self.commandedSpeed)
 
        else: self.commandedSpeed = 0

    def setServiceBrake(self):
        if self.c.vital_override == False and self.c.operating_mode == False:
            self.c.deployServiceBrake(self.anal_in.getBrakingValue())

    def lightsButton(self):
        if not self.c.operating_mode:
            if GPIO.input(25) == GPIO.HIGH:
                self.c.light_state_internal = not self.c.light_state_internal
                self.c.setInternalLights(self.c.light_state_internal)
                sleep(.5)

            if GPIO.input(8) == GPIO.HIGH:
                self.c.light_state_external = not self.c.light_state_external
                self.c.setExternalLights(self.c.light_state_external)
                sleep(.5)

    def doorsButton(self):
        if not self.c.operating_mode:
            if GPIO.input(7) == GPIO.HIGH:
                self.c.door_state_left = not self.c.door_state_left
                self.c.setLeftDoor(self.c.door_state_left)
                sleep(.5)

            if GPIO.input(16) == GPIO.HIGH:
                self.c.door_state_right = not self.c.door_state_right
                self.c.setRightDoor(self.c.door_state_right)
                sleep(.5)

    def announceButton(self, station_idx):
        if GPIO.input(26) == GPIO.HIGH:
            self.c.announce_state = not self.c.announce_state
            self.c.announceStation(self.c.announce_state, station_idx)
            sleep(.5)

    def ebrake_button(self):
        if self.c.vital_override == True and self.c.operating_mode == False:
            if GPIO.input(5) == GPIO.LOW:
                self.c.ebrakeCommand = True
                self.c.deployEbrake(True)

            if GPIO.input(5) == GPIO.HIGH:
                self.c.ebrakeCommand = False
                self.c.deployEbrake(False)
                 
    def setTemperature_manual(self):
        temp = self.anal_in.getTemperatureValue()
        self.c.setTemperature(temp)

    def checkFailures_manual(self):
        brake = self.c.checkFailures()
        self.c.deployEbrake(brake)
