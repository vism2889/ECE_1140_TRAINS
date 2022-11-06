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
   
    def __init__(self):
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
        self.pid.outer_limits = (0, 120000) # clamp at max power output specified in datasheet 120kW

    def getAuthority(self):
        return self.authority
    
    # need to confirm what data type authority will be
    def setAuthority(self, authority=None):
        if(authority==None):
            self.authority = input.getAuthority(input)
            return
        
        self.authority = authority
    
    def setInternalLights(self, light_state=None):
        if(light_state == None):
            self.light_state_internal = input.getInternalLightCommand(input)

        else: self.light_state_internal = light_state

        if(self.light_state_internal): GPIO.output(14, GPIO.HIGH)
        if(not self.light_state_internal): GPIO.output(14, GPIO.LOW)

        output.setInternalLightState(output, self.light_state_internal)
        
    def setExternalLights(self, light_state=None):
        if(light_state == None):
            self.light_state_external = input.getInternalLightCommand(input)

        else: self.light_state_external = light_state

        if(self.light_state_external): GPIO.output(15, GPIO.HIGH)
        if(not self.light_state_external): GPIO.output(15, GPIO.LOW)

        output.setExternalLightState(output, self.light_state_external)

    def setLeftDoor(self, door_state=None):
        if(door_state == None):
            self.door_state_left = input.getLeftDoorCommand(input)

        else: self.door_state_left = door_state

        if(self.door_state_left): GPIO.output(23, GPIO.HIGH)
        if(not self.door_state_left): GPIO.output(23, GPIO.LOW)

        output.setLeftDoor(output, self.door_state_left)

    def setRightDoor(self, door_state=None):
        if(door_state==None):
            self.door_state_right = input.getRightDoorCommand(input)

        else: self.door_state_right = door_state

        if(self.door_state_right): GPIO.output(24, GPIO.HIGH)
        if(not self.door_state_right): GPIO.output(24, GPIO.LOW)

        output.setRightDoorState(output, self.door_state_right)

    def setSpeed(self, speed=None):
        if(speed==None):
            speed = input.getCommandedSpeed(input)
            self.getPowerOutput(self, speed, input.getCurrentSpeed(input)) # function sends power data out

        else:
            currentSpeed = input.getCurrentSpeed(input)
            self.getPowerOutput(self, speed, currentSpeed)


    # can remove after testing
    def setSpeedLimit(self, speed_limit=None):
        if(speed_limit==None):
            self.speed_limit = input.getSpeedLimit(input)
            return

        self.speed_limit = speed_limit
        output.setSpeedLimit(output, self.speed_limit)

    # can remove after testing
    def setCurrentSpeed(self, current_speed=None):
        if(current_speed==None):
            self.current_speed = input.getCurrentSpeed(input)
            print(self.current_speed)

    # can remove after testing
    def getSpeed(self): return self.commanded_speed

    def setTemperature(self, temperature=None):
        if(temperature == None):
            self.temperature = input.getTemperature(input)

        else: self.temperature = temperature

        output.setTemperature(self.setTemperature)

    def setSuggestedSpeed(self, suggested_speed=None):
        if(suggested_speed == None):
            self.suggested_speed = input.getSuggestedSpeed(input)
            return 

        self.suggested_speed = suggested_speed

    # need to refactor to take in next station data from train model
    def announceStation(self, start, file_idx):
        output.setAnnounceState(output, start)
        mixer.music.load("audio/" +  self.station_audio[file_idx])
        if(start) : mixer.music.play()
        if(not start) : mixer.music.stop()

    def deployEbrake(self):
        # may have to consider case where if in auto mode and ebrake is deployed, stop taking in commanded speed data 
        output.setEbrakeState(output, True)
        output.setPower(output, 0)

    def deployServiceBrake(self):
        self.brakeCommand = not self.brakeCommand
        if self.brakeCommand:
            print("Brake Command on")

        if not self.brakeCommand:
            print("Brake Command off")

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

    def get_kp_ki(self):
        return self.k_p, self.k_i

    def getPowerOutput(self, commanded_speed, current_speed):
        self.pid.setpoint = self.commanded_speed
        self.power = self.pid(self.current_speed)
        if self.power > 0:
            output.setPower(output, self.power)
        
        else:
            self.power = 0.0
            output.setPower(output, self.power)


    def publish(self):
        output.publish(output)

    def subscribe(self):
        input.spinOnce(input)