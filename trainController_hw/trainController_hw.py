# import RPi.GPIO as GPIO
# from time import sleep
from simple_pid import PID
from pygame import mixer

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(10, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)

mixer.init()

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
        self.pid = PID(self.k_p, self.k_i, 0.1, setpoint=self.commanded_speed)
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    def setInternalLights(light_state):
        # if(light_state): GPIO.output(8, GPIO.HIGH)
        # if(not light_state): GPIO.output(8, GPIO.LOW) 
        return

    def setExternalLights(light_state):
        # if(light_state): GPIO.output(10, GPIO.HIGH)
        # if(not light_state): GPIO.output(10, GPIO.LOW)
        return

    def setLeftDoor(door_state):
        # if(door_state): GPIO.output(16, GPIO.HIGH)
        # if(not door_state): GPIO.output(16, GPIO.LOW)
        return

    def setRightDoor(door_state):
        # if(door_state): GPIO.output(18, GPIO.HIGH)
        # if(not door_state): GPIO.output(18, GPIO.LOW)
        return  

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

    def announceStation(self, start, file_idx):
        mixer.music.load(self.station_audio[file_idx])
        if(start) : mixer.music.play()
        if(not start) : mixer.music.stop()

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