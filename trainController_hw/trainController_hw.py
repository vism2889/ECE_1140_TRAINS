import RPi.GPIO as GPIO
from time import sleep
from simple_pid import PID
from pygame import mixer
import pygame

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)

pygame.mixer.pre_init(44100, 16,2,4096)
pygame.init()
sound = mixer.Sound("applause-1.wav")

class Control():
   
    def __init__(self):
        self.commanded_speed = 0
        self.current_speed = 0
        self.suggested_speed = 0
        self.temperature = 0
        self.k_p = 0
        self.k_i = 0
        self.pid = PID(self.k_p, self.k_i, 0.1, setpoint=self.commanded_speed) # initialize pid with fixed values
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW
        self.power = 0
        
    def initializePID(self, kp_val, ki_val):
        self.k_p = kp_val
        self.k_i = ki_val
        self.pid = PID(self.k_p, self.k_i, 0.1, setpoint=self.commanded_speed)
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    def setInternalLights(light_state):
        if(light_state): GPIO.output(8, GPIO.HIGH)
        if(not light_state): GPIO.output(8, GPIO.LOW) 

    def setExternalLights(light_state):
        if(light_state): GPIO.output(10, GPIO.HIGH)
        if(not light_state): GPIO.output(10, GPIO.LOW)

    def setLeftDoor(door_state):
        if(door_state): GPIO.output(16, GPIO.HIGH)
        if(not door_state): GPIO.output(16, GPIO.LOW)

    def setRightDoor(door_state):
        if(door_state): GPIO.output(18, GPIO.HIGH)
        if(not door_state): GPIO.output(18, GPIO.LOW)  

    def setSpeed(self, speed):
        self.commanded_speed = speed
        print("Commanded Speed: ", self.commanded_speed)

    def setCurrentSpeed(self, current_speed):
        self.current_speed = current_speed

    def getSpeed(self): return self.commanded_speed

    def setTemperature(self, temperature):
        self.temperature = temperature
        print(self.temperature)

    def setSuggestedSpeed(self, suggested_speed):
        self.suggested_speed = suggested_speed

    def announceStation(self, start):
        if(start) : sound.play()
        if(not start) : sound.stop()
       
    def deployEbrake(self):
        # may have to consider case where if in auto mode and ebrake is deployed, stop taking in power data 
        self.commanded_speed = 0
        self.power = 0
    
    def limitSpeed(self):
        if(self.commanded_speed > self.suggested_speed):
            self.setSpeed(self, self.suggested_speed)
    
    def set_kp_ki(kp_val, ki_val, self):
        self.k_p = kp_val
        self.k_i = ki_val

    def get_kp_ki(self):
        return self.k_p, self.k_i

    def getPowerOutput(self):
        self.pid.setpoint = self.commanded_speed
        self.power = self.pid(self.current_speed)
        return self.power