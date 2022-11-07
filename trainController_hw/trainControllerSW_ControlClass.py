from PyQt5 import QtCore, QtGui, QtWidgets

class Control():
    def __init__(self):
        self.speed = 0
        self.suggested_speed = 50
        self.temperature = 0
        self.power = 0

    def setInternalLights(light_state):
        if(light_state): InternalLights_DisplayBox.SetChecked(True)
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

    def setTemperature(self, temperature):
        self.temperature = temperature
        print(self.temperature)

    def getSuggestedSpeed(self):
        return self.suggested_speed
       
    def deployEbrake(self):
        self.speed = 0
    