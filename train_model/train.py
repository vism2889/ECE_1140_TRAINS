##############################################################################
# AUTHOR(S):    Sushmit Acharya
# DATE:         12/15/2022
# FILENAME:     train.py
# DESCRIPTION:
# Train Class representing a Train Object
##############################################################################
from dataclasses import dataclass
from tokenize import Double
from tracemalloc import start
import time
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal
import random
sys.path.append("../SystemSignals")
from Signals import Signals




@dataclass
class TrainData():
    #dimensions in meters
    length = float = 1267.717
    width = float = 104.3307
    height = float = 134.6457 
    mass_empty = float = 40.9*907.185

    #passengers
    max_passengers_seated = int =74
    max_passengers = int = 148

    #limits
    max_gradient = int = 0.06 #Percentage
    motor_pwr = float = 120000  #Watts
    max_speed = float = 70000/3600  #m/s
    
    #accelerations
    med_accel = float =  0.5    #m/s^2
    serv_brake = float = 1.2  #m/s^2
    emergency_brake = 2.73    #m/s^2

    kinetic_fric_constant = float = 0.09 #Newtons
    static_fric_constant = float = 0.4
    


class PointMassModel():
    def __init__(self):
        self.suggSpeed = 0
        self.cmdSpeed = 0
        self.grade = 0
        self.count = 0
        self.ctc_authority = []
        self.speedUp = 1
        self.waysideAuthority = []
        self.train_authority = 0
        self.stationStop = False
        self.ctcStopBlock = None
        self.stopAtStation = False

        self.suggested_speed = 0
        self.speedLimit = 0

        self._td = TrainData()

        self.curr_block = None
        self.prev_block = None
        self.curr_block = None
        self.BlockModels = None

        self.ctcStationStop = []

        #time independent values
        self.power = 0
        self.force = 0
        self.mass = 0

        #previous and current time for proper time based calculations
        self.prev_time = 0
        self.curr_time = 0
        self.elapsed_time = 0
        
        #acceleration
        self.prev_accel = 0
        self.curr_accel = 0

        #velocity(m/s) and speed(mph)
        self.prev_vel = 0
        self.curr_vel = 0
        self.curr_speed = 0

        #position(m)
        self.prev_pos = 0
        self.curr_pos = 0
    
    def setPower(self, power, t):
        self.mass = self._td.mass_empty
        if self.prev_time == 0:
            self.prev_time = t
            self.curr_time = time.time()
        else:
            #setting time values
            self.prev_time = self.curr_time
            self.curr_time = t

        self.elapsed_time = (self.curr_time-self.prev_time) * self.speedUp

        self.power = power

        self.calcForce()
        self.calcAccel()
        self.calcVel()
        self.calcPos()
    
    def brake(self, val):
        #if val is 0 it is service brake
        #if val is 1 it is e brake
        self.power = 0
        #setting time values
        self.prev_time = self.curr_time
        self.curr_time = time.time()
        self.elapsed_time = (self.curr_time-self.prev_time) * self.speedUp
        
        if self.curr_vel > 0:
            self.prev_accel = self.curr_accel
            self.curr_accel = self.dec_force(val)
            self.calcVel()
            self.calcPos()
            if self.curr_vel <= 0:
                self.curr_vel = 0
        else:
            self.calcPos()
            self.power = 0  
            self.force = 0
            self.prev_accel = 0
            self.curr_accel = 0
            self.curr_vel = 0
            self.prev_vel = 0
            self.prev_time = 0


    def dec_force(self, val):
        if val == 0:
            dec_force = self._td.mass_empty * self._td.serv_brake
        else:
            dec_force = self._td.mass_empty * self._td.emergency_brake

        kinetic_friction_force = self._td.mass_empty*9.8*self._td.kinetic_fric_constant

        self.force = self.force-dec_force-kinetic_friction_force
            
        self.curr_accel = self.force/self._td.mass_empty
        return self.curr_accel

    def calcForce(self, brake = False):
        if self.curr_block:
            self.grade = float(self.BlockModels[self.curr_block-1].grade)/100
        if self.power != 0:
            kinetic_friction_force = self._td.mass_empty*9.8*self._td.kinetic_fric_constant*0.01
        else:
            kinetic_friction_force = self._td.mass_empty*9.8*self._td.kinetic_fric_constant
        gradeForce = self._td.mass_empty*9.8*(self.grade)/(1+self.grade**2)**0.5

        if self.curr_vel > 0:
            self.force = float(self.power)/float(self.curr_vel)
            self.force -= kinetic_friction_force
            self.force -= gradeForce
        else:
            self.force = self.power*2
            static_friction_force = self._td.mass_empty*9.8*self._td.static_fric_constant
            self.force -= static_friction_force
            self.force -= gradeForce
    
    def calcAccel(self):
        self.prev_accel = self.curr_accel
        self.curr_accel = float(self.force)/float(self._td.mass_empty)
    
    def calcVel(self):
        self.prev_vel = self.curr_vel
        self.curr_vel = self.prev_vel + ((self.elapsed_time)/2)*(self.prev_accel+self.curr_accel)
        if self.curr_vel < 0:
            self.curr_vel = 0
        if self.curr_vel > 19.444444:
            self.curr_vel = 19.44444

        self.curr_speed = round(self.curr_vel * (1/1000) * (0.62) * (3600))
        if self.curr_speed < 0:
            self.curr_speed = 0
        if self.curr_speed > 45:
            self.curr_speed = 45


    
    def calcPos(self):
        self.train_authority = 0
        
        #position calculation
        if self.curr_vel != 0:
            self.prev_pos = self.curr_pos
            self.curr_pos = self.prev_pos + (self.elapsed_time/2)*(self.prev_vel +self.curr_vel)

        #block object length calculation
        curr_block_object = self.BlockModels[self.curr_block-1]
        self.curr_block_len = curr_block_object.blockLength
        self.curr_block_len = float(self.curr_block_len)

    
        if self.curr_pos >= self.curr_block_len and self.curr_block != 0:
            #resetting position
            self.curr_pos = self.curr_pos-self.curr_block_len
            self.prev_pos = 0

            if len(self.waysideAuthority) > 1:
                self.curr_block = self.waysideAuthority[1]
                self.prev_block = self.waysideAuthority[0]
                if self.curr_block == 0:
                    self.train_authority = 0
                    return
            if len(self.waysideAuthority) == 1:
                self.curr_block = self.waysideAuthority[0]
                self.prev_block = self.prev_block
            elif self.curr_block == 0:
                self.train_authority = 0
                return
        elif self.curr_block == 0:
            self.train_authority = 0
            return 
                
        
        
        for c_bl in self.ctc_authority:
            if c_bl in self.waysideAuthority:
                ind = self.waysideAuthority.index(c_bl)
                
                if self.curr_vel != 0 and not self.stationStop:
                    self.waysideAuthority = self.waysideAuthority[0:ind+1]
                if c_bl == self.curr_block and self.curr_vel == 0:
                    self.stationStop = True
                elif c_bl == self.prev_block:
                    self.stationStop = False
                    self.stopAtStation = False
                    self.ctc_authority.remove(c_bl)
                
                if self.ctcStationStop != c_bl:
                    self.ctcStationStop = c_bl
            


        #Calculating Authority distance when train not at stopping block               
        if len(self.waysideAuthority) > 1:
            if self.curr_block == self.waysideAuthority[0]:
                wayside = self.waysideAuthority[1:len(self.waysideAuthority)]
            elif self.curr_block == self.waysideAuthority[1]:
                wayside = self.waysideAuthority[2:len(self.waysideAuthority)]
            
            self.train_authority += float(self.BlockModels[self.curr_block-1].blockLength)-self.curr_pos
            for b in wayside[0:len(wayside)-1]:
                self.train_authority += float(self.BlockModels[b-1].blockLength)
            
            if len(wayside) > 0 and wayside[-1] != 0:
                lastBlock = wayside[-1]
                self.train_authority += float(self.BlockModels[lastBlock-1].blockLength)/4
        elif len(self.waysideAuthority) == 1 and self.curr_vel != 0:
            if self.prev_vel != 0:
                self.train_authority = 0
        
      
        self.speedLimit = float(self.BlockModels[self.curr_block-1].speedLimit)*0.277778
        if self.speedLimit >= self.suggSpeed:
            self.cmdSpeed = self.suggSpeed
        else:
            self.cmdSpeed = self.speedLimit

        

class Train():
    def __init__ (self):

        self.id = None
        self.stationSide = ''
        self.underground = ''
        self.stationName = ''

        #point Mass model
        self.pm = PointMassModel()

        #dispatch
        self.dispatched = False
        #Failure States
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.train_engine_failure = False
        self.Failures = {'Brake':self.brake_failure, 'Signal':self.signal_pickup_failure, 'Train_Engine': self.train_engine_failure}
        
        #Current Line
        self.line = None
        
        #Brake Values
        self.e_brake = False
        self.service_brake = False

        self.curr_power = 0
        self.curr_speed = 0
        


        self.int_lights = False
        self.ext_lights = False
        self.crew_count = 0
        self.curr_speed = self.pm.curr_speed
        self.passenger_count = 0
        self.temperature = 0
        self.left_doors = False
        self.right_doors = False
        self.announcements = False

        self.last_station = 'Pitt'
        self.next_station = 'Phil'

        self.ctcAuthority = []
        self.authority = 20
        self.grade = 0
   
    def get_temperature(self):
        return self.temperature

    def get_int_light_state(self):
        return self.int

    def set_power(self, power, t = None):

        self.curr_speed = self.pm.curr_speed
        self.curr_power = power

        for f in (self.Failures):
            if self.Failures[f]:
                return 
        
        if(self.dispatched):
            self.pm.setPower(self.curr_power, time.time() )
            
                
            




