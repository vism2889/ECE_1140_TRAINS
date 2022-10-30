import RPi.GPIO as GPIO
from time import sleep
from pygame import mixer
from control import Control

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# inputs
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # internal lights
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # external lights
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # left door
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # right door
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # announce
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # ebrake

mixer.init()

# class that handles gpio for manual input from train driver
def ManualControl(control_object):

    def __init__(self):
        self.light_state_internal = False
        self.light_state_external = False
        self.door_state_left = False
        self.door_state_right = False
        self.announce_state = False
        self.station_audio = ["shadyside_herron.mp3", "herron_swissvale.mp3", 
                              "swissvale_penn.mp3", "penn_steelplaza.mp3", 
                              "steelplaza_first.mp3","first_stationSquare.mp3", 
                              "stationSquare_southHills.mp3"]

    def lightsButton(self):
        if GPIO.input(22) == GPIO.HIGH:
            self.light_state_internal = not self.light_state_internal
            control_object.setInternalLights(self.light_state_internal)
            sleep(.5)

        if GPIO.input(24) == GPIO.HIGH:
            self.light_state_external = not self.light_state_external
            control_object.setExternalLights(self.light_state_external)
            sleep(.5)

    def doorsButton(self):
        if GPIO.input(26) == GPIO.HIGH:
            self.door_state_left = not self.door_state_left
            control_object.setLeftDoor(self.door_state_left)
            sleep(.5)

        if GPIO.input(36) == GPIO.HIGH:
            self.door_state_right = not self.door_state_right
            control_object.setRightDoor(self.door_state_right)
            sleep(.5)

    def announceButton(self, station_idx):
        if GPIO.input(37) == GPIO.HIGH:
            self.announce_state = not self.announce_state
            control_object.announceStation(control_object, self.announce_state, station_idx)
            sleep(.5)

    def ebrake_button(self):
        if GPIO.input(29) == GPIO.LOW:
            control_object.deployEbrake(control_object)

