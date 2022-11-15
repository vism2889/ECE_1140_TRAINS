from dataclasses import dataclass
from tokenize import Double
from tracemalloc import start
import time
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import pyqtSignal
import random


# class PointMassModel():
#     def __init__(self) -> None:
#         pass

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
    max_gradient = int = 60 #Percentage
    motor_pwr = float = 120000  #Watts
    max_speed = float = 70000/3600  #m/s
    
    #accelerations
    med_accel = float =  0.5    #m/s^2
    serv_brake = float = 1.2  #m/s^2
    emergency_brake = 2.73    #m/s^2

    kinetic_fric_constant = float = 0.1 #Newtons
    static_fric_constant = float = 0.6
    


class PointMassModel():
    def __init__(self, blocks, blockLens):
        
        self.id = None

        self._td = TrainData()
        
        self.blocks = blocks
        self.curr_block = 0
        self.blockLens = blockLens
        self.occ_list = [0 for i in range(len(blocks))]

        #time independent values
        self.power = 0
        self.force = 0
        self.mass = 0

        self.prev_time = 0
        self.curr_time = 0
        self.elapsed_time = 0
        
        self.prev_accel = 0
        self.curr_accel = 0

        self.prev_vel = 0
        self.curr_vel = 0
        self.curr_speed = 0

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

        self.elapsed_time = self.curr_time-self.prev_time

        self.power = power
        
        self.calcForce()
        self.calcAccel()
        self.calcVel()
        self.calcPos()

    def e_brake(self, t):
        self.curr_accel = self._td.emergency_brake
        
        #setting time values
        self.prev_time = self.curr_time
        self.curr_time = t
        self.elapsed_time = self.curr_time-self.prev_time

        while self.curr_vel > 0:
            print(f'Ebrake velocity before decleration:{self.curr_vel}')
            self.prev_vel = self.curr_vel
            self.prev_accel = self.curr_accel
            self.curr_accel = self.dec_force()
           
            self.curr_vel = self.prev_vel + (self.elapsed_time/2)*(self.prev_accel+self.curr_accel)
            self.curr_speed = round(self.curr_vel * (1/1000) * (0.62) * (3600))
            self.curr_pos = self.prev_pos + (self.elapsed_time/2)*(self.prev_vel + self.curr_vel)

            if self.curr_vel < 0:
                self.curr_vel = 0
                
            self.prev_accel = self.curr_accel

            self.prev_time = self.curr_time
            self.curr_time = time.time()
            print(f'Ebrake decreasing velocity:{self.curr_vel}')
        
        self.power = 0
        self.force = 0
        self.prev_accel = 0
        self.curr_accel = 0
    
    def serv_brake(self, t):
        self.power = 0

        #setting time values
        self.prev_time = self.curr_time
        self.curr_time = t
        self.elapsed_time = self.curr_time-self.prev_time

        temp_start_t = 0
        print(f'Serv Brake velocity before decleration:{self.curr_speed}')
        print(f'Serv Brake force before deceleration: {self.force}')
        print(f'Deceleration force is: {self._td.mass_empty * self._td.serv_brake}')
        print(f'Train acceleration before stop seqeuence: {self.curr_accel}')
        print(f'Friction Force: {self._td.mass_empty*self._td.kinetic_fric_constant}\n')
        while self.curr_vel > 0:

            self.prev_accel = self.curr_accel
            

            if self.elapsed_time > 0.5:
                self.curr_accel = self.dec_force()
                self.calcVel()
                self.calcPos()
                
                self.prev_time = self.curr_time
            
            self.curr_time = time.time()
            self.elapsed_time = self.curr_time- self.prev_time

            if self.curr_vel < 0:
                self.curr_vel = 0
                
            self.prev_accel = self.curr_accel

            
            if time.time() - temp_start_t > 2:
                print(f'Current Force is: {self.force}')
                print(f'Current Acceleration is: {self.curr_accel}')
                print(f'Current Velocity is: {self.curr_vel}')
                print(f'Serv Brake decreasing velocity:{self.curr_speed} in {time.time() - temp_start_t}\n')
                temp_start_t = time.time()
                    
        self.force = 0
        self.prev_accel = 0
        self.curr_accel = 0

    def dec_force(self):
        # print(f"Current force is: {self.force}")
        dec_force = self._td.mass_empty * self._td.serv_brake
        kinetic_friction_force = self._td.mass_empty*9.8*self._td.kinetic_fric_constant

        if self.force > 0: 
            self.force = self.force-dec_force
        else:
            self.force -= kinetic_friction_force*0.25
            
        self.curr_accel = self.force/self._td.mass_empty
        return self.curr_accel

    def calcForce(self):
        static_friction_force = self._td.mass_empty*9.8*self._td.static_fric_constant
        if self.curr_vel > 0:
            self.force = float(self.power)/float(self.curr_vel)
        else:
            self.force = self.power * 2
            self.force -= static_friction_force
            print(f'force - static force = {self.force}')

                
    
    def calcAccel(self):
        self.prev_accel = self.curr_accel
        self.curr_accel = float(self.force)/float(self._td.mass_empty)
    
    def calcVel(self):
        self.prev_vel = self.curr_vel
        self.curr_vel = self.prev_vel + (self.elapsed_time/2)*(self.prev_accel+self.curr_accel)
        self.curr_speed = round(self.curr_vel * (1/1000) * (0.62) * (3600))
    
    def calcPos(self):
        self.occ_list[self.curr_block] = 1
        self.prev_pos = self.curr_pos
        self.curr_pos = self.prev_pos + (self.elapsed_time/2)*(self.prev_vel +self.curr_vel)

        if self.curr_pos >= self.blockLens[self.curr_block]:
            self.occ_list[self.curr_block] = 0
            self.curr_pos = 0
            self.prev_pos = 0
            self.curr_block += 1
            self.occ_list[self.curr_block] = 1


        

class Train():
    def __init__ (self):
        
        #block list
        self.blocks          = [i for i in range(150)]
        self.blockLens       = [random.randint(10,25) for i in range(150)]

        #point Mass model
        self.pm = PointMassModel(self.blocks, self.blockLens)

        #dispatch
        self.dispatched = False
        self.speed_limit = 0
        #Failure States
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.train_engine_failure = False
        self.Failures = {'Brake':self.brake_failure, 'Signal':self.signal_pickup_failure, 'Train_Engine': self.train_engine_failure}
        
        #Current Line
        self.line = 'blue'
        
        #Brake Values
        self.e_brake = 'Off'
        self.service_brake = 'Off'

        self.curr_power = 0
        self.curr_speed = 0
        self.cmd_speed = 0


        self.int_lights = 'ON'
        self.ext_lights = 'ON'
        self.crew_count = 0
        self.curr_speed = self.pm.curr_speed
        self.passenger_count = 0
        self.temperature = 0
        self.left_doors = 'Closed'
        self.right_doors = 'Closed'

        self.last_station = 'Pitt'
        self.next_station = 'Phil'

        self.authority = []
        self.grade = 0
        self.switch = 0
        
    # def launch_ui(self):
    #     app = QtWidgets.QApplication(sys.argv)
    #     window = TrainModel(self)
    #     app.exec_()
          

    def e_brake_func(self):
        if self.e_brake == 'On' and self.pm.curr_vel > 0:
            self.pm.e_brake(time.time())
    
    def serv_brake_func(self):
        print('inside service brake')
        if self.service_brake == 'On' and self.pm.curr_vel > 0:
            self.pm.serv_brake(time.time())

    def dispatch(self):
        self.dispatched = True
        self.set_power(120000, time.time())

    def set_power(self, power, t = None):

        self.curr_speed = self.pm.curr_speed
        self.curr_power = power

        for f in (self.Failures):
            if self.Failures[f]:
                print(f"Error {f} failure")
                return 
        
        if(self.dispatched):
            print ('---------------------Setting Power-----------------------')
            if self.service_brake == 'On' and self.pm.curr_vel > 0:
                self.serv_brake_func()
            elif self.e_brake == 'On' and self.pm.curr_vel>0:
                self.e_brake_func()
            else:
                self.pm.setPower(self.curr_power, time.time() )
                print('\nTrain Model Object Values')
                print(f'time_elapsed: {self.pm.elapsed_time}')
                print(f'Current Power: {self.curr_power}')
                print(f'Previous Vel:{self.pm.prev_vel}')
                print(f'Force: {self.pm.force}')
                print(f'Previous Accel:{self.pm.prev_accel}')
                print(f'Current Accel:{self.pm.curr_accel}')
                print(f'Current_Vel: {self.pm.curr_vel}')
                print(f'Current Speed: {self.pm.curr_speed} mph\n')
                print(f'Current Position: {self.pm.curr_pos}')
            
                
            




