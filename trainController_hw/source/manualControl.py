import RPi.GPIO as GPIO
from time import sleep
from pygame import mixer
from control import Control
from analogInput import getSpeedValue

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

    def __init__(self):
        Control.__init__(Control)
        self.commandedSpeed = 0
        self.ebrake_state = False
        self.light_state_internal = False
        self.light_state_external = False
        self.door_state_left = False
        self.door_state_right = False
        self.announce_state = False
        self.station_audio = ["shadyside_herron.mp3", "herron_swissvale.mp3", 
                              "swissvale_penn.mp3", "penn_steelplaza.mp3", 
                              "steelplaza_first.mp3","first_stationSquare.mp3", 
                              "stationSquare_southHills.mp3"]

    def setCommandedSpeed(self):
        if self.ebrake_state == False:
            self.commandedSpeed = getSpeedValue()
            Control.setSpeed(Control, self.commandedSpeed)
            return self.commandedSpeed

        else: return 0

    def lightsButton(self):
        if GPIO.input(25) == GPIO.HIGH:
            self.light_state_internal = not self.light_state_internal
            Control.setInternalLights(self.light_state_internal)
            sleep(.5)

        if GPIO.input(8) == GPIO.HIGH:
            self.light_state_external = not self.light_state_external
            Control.setExternalLights(self.light_state_external)
            sleep(.5)

    def doorsButton(self):
        if GPIO.input(7) == GPIO.HIGH:
            self.door_state_left = not self.door_state_left
            Control.setLeftDoor(self.door_state_left)
            sleep(.5)

        if GPIO.input(16) == GPIO.HIGH:
            self.door_state_right = not self.door_state_right
            Control.setRightDoor(self.door_state_right)
            sleep(.5)

    def announceButton(self, station_idx):
        if GPIO.input(26) == GPIO.HIGH:
            self.announce_state = not self.announce_state
            Control.announceStation(Control, self.announce_state, station_idx)
            sleep(.5)

    def ebrake_button(self):
        if GPIO.input(5) == GPIO.LOW:
            Control.deployEbrake(Control)
            self.ebrake_state = True

        else: self.ebrake_state = False


