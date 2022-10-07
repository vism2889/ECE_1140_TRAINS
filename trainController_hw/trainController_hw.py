import RPi.GPIO as GPIO
from time import sleep
from simple_pid import PID

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)

class Control():
    def __init__(self):
        self.speed = 0
        self.suggested_speed = 50
        self.temperature = 0
        self.power = 0

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
        self.speed = speed
        print(self.speed)

    def getSpeed(self):
        return self.speed

    def setTemperature(self, temperature):
        self.temperature = temperature
        print(self.temperature)

    def getSuggestedSpeed(self):
        return self.suggested_speed
       
    def deployEbrake(self):
        self.speed = 0
    
    def limitSpeed(self):
        if(self.getSpeed(self) > self.getSuggestedSpeed(self)):
            self.setSpeed(self.getSuggestedSpeed(self))
            print("called: ", self.getSpeed(self))

    def getPowerOutput(k_p, k_i, k_d, self):
        pid = PID(k_p, k_i, k_d, setpoint = self.speed)
        pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

        return pid(self.speed)