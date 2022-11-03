import RPi.GPIO as GPIO
from simple_pid import PID
from pygame import mixer
from outputData import OutputData as output
from trainData import TrainData as input

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# outputs
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW) # internal lights
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW) # external lights
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW) # left door
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) # right door

mixer.init()

class Control():
   
    def __init__(self, test=True):
        if(not test):
            output.__init__(output)
            input.__init__(input)

        self.authority = 0
        self.light_state_internal = False
        self.light_state_external = False
        self.door_state_left = False
        self.door_state_right = False
        self.announce_state = False
        self.commanded_speed = 0
        self.brakeCommand = False
        self.current_speed = 0
        self.suggested_speed = 0
        self.speed_limit = 100
        self.temperature = 0
        self.k_p = 0
        self.k_i = 0
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed) # initialize pid with fixed values
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
        self.pid = PID(self.k_p, self.k_i, 0, setpoint=self.commanded_speed)
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    def getAuthority(self):
        return self.authority

    def setAuthority(self, authority=None):
        if(authority==None):
            self.authority = input.getAuthority(input)
            return
        
        self.authority = authority
    
    def setInternalLights(light_state=None):
        if(light_state == None):
            light_state = input.getInternalLightCommand(input)
            return

        if(light_state): GPIO.output(14, GPIO.HIGH)
        if(not light_state): GPIO.output(14, GPIO.LOW) 
        
    def setExternalLights(light_state=None):
        if(light_state == None):
            light_state = input.getInternalLightCommand(input)
            return

        if(light_state): GPIO.output(15, GPIO.HIGH)
        if(not light_state): GPIO.output(15, GPIO.LOW)

    def setLeftDoor(door_state=None):
        if(door_state == None):
            door_state = input.getLeftDoorCommand
            return

        if(door_state): GPIO.output(23, GPIO.HIGH)
        if(not door_state): GPIO.output(23, GPIO.LOW)

    def setRightDoor(door_state=None):
        if(door_state==None):
            door_state = input.getRightDoorCommand(input)
            return

        if(door_state): GPIO.output(24, GPIO.HIGH)
        if(not door_state): GPIO.output(24, GPIO.LOW)

    def setSpeed(self, speed=None):
        if(speed==None):
            speed = input.getCommandedSpeed(input)
            return 

        if(self.limitSpeed(self, speed)):
            self.commanded_speed = speed
            output.setCommandedSpeed(output, self.commanded_speed)
            output.setSpeedLimit(output, self.speed_limit)

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
        output.setCurrentSpeed(output, self.current_speed)

    def getSpeed(self): return self.commanded_speed

    def setTemperature(self, temperature=None):
        if(temperature == None):
            self.temperature = input.getTemperature(input)
            return

        self.temperature = temperature

    def setSuggestedSpeed(self, suggested_speed=None):
        if(suggested_speed == None):
            self.suggested_speed = input.getSuggestedSpeed(input)
            return 

        self.suggested_speed = suggested_speed

    # need to refactor to take in next station data from train model
    def announceStation(self, start, file_idx):
        # output.setAnnounceState(output, start)
        mixer.music.load("audio/" +  self.station_audio[file_idx])
        if(start) : mixer.music.play()
        if(not start) : mixer.music.stop()

    def deployEbrake(self):
        # may have to consider case where if in auto mode and ebrake is deployed, stop taking in commanded speed data 
        self.commanded_speed = 0
        self.power = 0

    def deployServiceBrake(self):
        self.brakeCommand = not self.brakeCommand
        if self.brakeCommand:
            print("Brake Command on")

        if not self.brakeCommand:
            print("Brake Command off")

    def limitSpeed(self, speed):
        if(speed > self.speed_limit):
            return False
        
        else: return True

    def checkAuthority(self):
        if self.authority == 0:
            self.deployEbrake(self)
        output.setAuthority(output, self.authority)
    
    def set_kp_ki(kp_val, ki_val, self):
        self.k_p = kp_val
        self.k_i = ki_val

    def get_kp_ki(self):
        return self.k_p, self.k_i

    def getPowerOutput(self):
        self.pid.setpoint = self.commanded_speed
        self.power = self.pid(self.current_speed)
        if self.power > 0:
            return self.power
        
        else:
            self.power = 0
            return self.power

    def publish(self):
        output.publish(output)