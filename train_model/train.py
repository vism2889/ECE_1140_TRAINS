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
    def __init__(self):
        
        self.suggested_speed = 0
        #track model to train comms
        self.speed_limit = 0
        
        self.id = None

        self._td = TrainData()

        self.glBlockModels = None
        # fname = open(f'{os.getcwd()}/trackblocks', 'rb')
        # self.glBlockMOdels = pickle.load(fname)
        # fname.close()

        # self.blocks          = [i for i in range(150)]
        self.curr_block = 0
        sec1 = [i for i in range(63, 101)]
        sec2 = [i for i in range(85, 76, -1)]
        sec3 = [i for i in range(101, 150)]
        sec4 = [i for i in range(29, 0, -1)]
        sec5 = [i for i in range(13, 58)]

        self.blocks = sec1 + sec2 + sec3 + sec4 + sec5
        # self.blockLens = [random.randint(10,25) for i in range(len(self.blocks))]        
        self.occ_list = [0 for i in range(150)]
        self.occ_index = self.blocks[0]


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

        self.elapsed_time = (self.curr_time-self.prev_time)

        self.power = power
        
        self.calcForce()
        self.calcAccel()
        self.calcVel()
        self.calcPos()

    def e_brake(self):
        self.curr_accel = self._td.emergency_brake
        
        #setting time values
        self.prev_time = self.curr_time
        self.curr_time = time.time()
        self.elapsed_time = self.curr_time-self.prev_time

        if self.curr_vel > 0:
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
    
    def brake(self, val):

        self.power = 0

        #setting time values
        self.prev_time = self.curr_time
        self.curr_time = time.time()
        self.elapsed_time = self.curr_time-self.prev_time

        temp_start_t = 0
        print(f'Serv Brake velocity before decleration:{self.curr_speed}')
        print(f'Serv Brake force before deceleration: {self.force}')
        print(f'Deceleration force is: {self._td.mass_empty * self._td.serv_brake}')
        print(f'Train acceleration before stop seqeuence: {self.curr_accel}')
        print(f'Friction Force: {self._td.mass_empty*self._td.kinetic_fric_constant}\n')
        if self.curr_vel > 0:
            self.prev_accel = self.curr_accel
            if self.elapsed_time > 0.5:
                self.curr_accel = self.dec_force(val)
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
                print(f'Serv Brake decreasing velocity:{self.curr_speed} in {self.elapsed_time}\n')
                temp_start_t = time.time()
                    
        self.force = 0
        self.prev_accel = 0
        self.curr_accel = 0

    def dec_force(self, val):
        # print(f"Current force is: {self.force}")
        if val == 0:
            dec_force = self._td.mass_empty * self._td.serv_brake
        else:
            dec_force = self._td.mass_empty * self._td.emergency_brake

        kinetic_friction_force = self._td.mass_empty*9.8*self._td.kinetic_fric_constant

        # if self.force > 0: 
        self.force = self.force-dec_force
        # else:
        #     self.force -= kinetic_friction_force
            
        self.curr_accel = self.force/self._td.mass_empty
        return self.curr_accel

    def calcForce(self):
        static_friction_force = self._td.mass_empty*9.8*self._td.static_fric_constant
        if self.curr_vel > 0:
            self.force = float(self.power)/float(self.curr_vel)
        else:
            self.force = 120000 * 2
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
        
        #position calculation
        self.prev_pos = self.curr_pos
        self.curr_pos = self.prev_pos + (self.elapsed_time/2)*(self.prev_vel +self.curr_vel)

        #block object length calculation
        curr_block_object = self.glBlockModels[self.occ_index]
        self.curr_block_len = curr_block_object.blockLength
        self.curr_block_len = float(self.curr_block_len)

        #getting block values for speed
        self.speed_limit = float(curr_block_object.speedLimit)
        if self.suggested_speed > self.speed_limit:
            self.speed_limit = self.speed_limit
        else:
            self.speed_limit = self.suggested_speed

        
        print(f'-------------------Position: {self.curr_pos}-----------------------------')
        if self.curr_pos >= self.curr_block_len:
            self.occ_list[self.occ_index] = 0
            
            #resetting position
            self.curr_pos = self.curr_pos-self.curr_block_len
            self.prev_pos = 0

            #incrementing curr_block
            self.curr_block += 1
        
        if self.occ_index > 147:
            print(self.occ_index)

        self.occ_index = self.blocks[self.curr_block]
        self.occ_list[self.occ_index] = 1
        
        
        
        


        

class Train():
    def __init__ (self):

        self.speed_limit = 0
        
        #block list
        self.blocks          = [i for i in range(150)]
        self.blockLens       = [random.randint(10,25) for i in range(150)]

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
        self.line = 'blue'
        
        #Brake Values
        self.e_brake = False
        self.service_brake = False

        self.curr_power = 0
        self.curr_speed = 0
        self.cmd_speed = 30.22


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

        self.authority = [False,False,False,False,False,True,False,False]
        self.grade = 0
        self.switch = 0

        currentTime = time.time() * 10
        
    # def launch_ui(self):
    #     app = QtWidgets.QApplication(sys.argv)
    #     window = TrainModel(self)
    #     app.exec_()
    def get_temperature(self):
        return self.temperature

    def get_int_light_state(self):
        return self.int

    def e_brake_func(self):
        if self.e_brake == True and self.pm.curr_vel > 0:
            self.pm.e_brake()
    
    def serv_brake_func(self):
        print('inside service brake')
        if self.service_brake == True and self.pm.curr_vel > 0:
            self.pm.serv_brake()

    def dispatch(self):
        self.dispatched = True
        self.pm.power = 120000
        self.set_power(120000, time.time())

    def set_power(self, power, t = None):

        self.curr_speed = self.pm.curr_speed
        self.curr_power = power

        for f in (self.Failures):
            if self.Failures[f]:
                print(f"Error {f} failure")
                return 
        
        if(self.dispatched):
            if self.service_brake == True and self.pm.curr_vel > 0:
                self.serv_brake_func()
            elif self.e_brake == True and self.pm.curr_vel>0:
                self.e_brake_func()
            else:
                self.pm.setPower(self.curr_power, time.time() )

                print('\nTrain Model Object Values')
                print(f'time_elapsed: {self.pm.elapsed_time}')
                print(f'Current Power: {self.curr_power}')
                # print(f'Previous Vel:{self.pm.prev_vel}')
                # print(f'Force: {self.pm.force}')
                # print(f'Previous Accel:{self.pm.prev_accel}')
                # print(f'Current Accel:{self.pm.curr_accel}')
                print(f'Current_Vel: {self.pm.curr_vel}')
                print(f'Current Speed: {self.pm.curr_speed} mph')
                # print(f'Current Position: {self.pm.curr_pos} m \n')
            
                
            




