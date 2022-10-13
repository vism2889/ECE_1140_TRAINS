from dataclasses import dataclass
from tokenize import Double
from tracemalloc import start
import time



class Train():
    def __init__ (self):

        #dispatch
        self.dispatched = False

        #Failure States
        self.brake_failure = False
        self.signal_pickup_failure = False
        self.train_engine_failure = False
        self.Failures = {'Brake':self.brake_failure, 'Signal':self.signal_pickup_failure, 'Train_Engine': self.train_engine_failure}
        #Current Line
        self.line = 'blue'
        
        #num cars
        self.num_cars = 1

        #length of 1 car
        self.length = 1267.717*self.num_cars

        #width of 1 car
        self.width = 104.3307

        #height of 1 car
        self.height = 134.6457 

        #Note mass in kilograms
        self.mass_empty = 40.9* self.num_cars * 907.185*1000
        self.max_passengers_seated = self.num_cars *74
        self.max_passengers = self.num_cars*148
        self.max_gradient = 60

        #Power in Kilo Watts
        self.motor_power = 120000
        #Max Speed in m/s
        self.max_speed = 70000/3600
        #Medium Acceleration in m/s^2
        self.med_accel =  0.5
        #service brake deceleration in m/s^2
        self.serv_brake = -1.2
        self.emergency_brake = -2.73
        self.e_brake = 'Off'
        self.service_brake = 'Off'


        #Train Current States
        self.curr_mass = self.mass_empty
        self.curr_power = 0
        self.curr_accel = 0
        self.curr_vel = 0
        self.curr_force = 0
        self.curr_pos = 0
        self.curr_time = None
        self.curr_pos = 0
        self.cmd_speed = 0

        #Train Previous States
        self.prev_accel = 0
        self.prev_vel = 0
        self.prev_pos = 0
        self.prev_time = 0
        self.prev_pos = 0

        self.int_lights = 'ON'
        self.ext_lights = 'ON'
        self.crew_count = 0
        self.curr_speed = None
        self.passenger_count = 0
        self.temperature = 0
        self.left_doors = 'Closed'
        self.right_doors = 'Closed'

        self.last_station = 'Pitt'
        self.next_station = 'Phil'

        self.authority = 0
        self.grade = 0
        self.switch = 0
        
        
    
    def get_speed(self):
        speed = round(self.curr_vel * (1/1000) * (0.62) * (3600))
        return speed

    def ebrake(self):
        if self.e_brake == 'On':
            self.curr_accel = self.emergency_brake
            time_elapsed = self.curr_time - self.prev_time
            while self.curr_vel > 0:
                temp_curr_vel = self.curr_vel
                self.curr_vel = self.prev_vel + (time_elapsed/2)*(self.prev_accel+self.curr_accel)
                
                if self.curr_vel < 0:
                    self.curr_vel = 0
                    
                self.prev_accel = self.curr_accel
                self.prev_vel = temp_curr_vel

                self.prev_time = self.curr_time
                self.curr_time = time.time()
    
    def serv_brake_func(self):
        print('inside service brake')
        if self.service_brake == 'On':
            self.curr_accel = self.serv_brake
            time_elapsed = self.curr_time - self.prev_time
            while self.curr_vel > 0:
                temp_curr_vel = self.curr_vel
                self.curr_vel = self.prev_vel + (time_elapsed/2)*(self.prev_accel+self.curr_accel)
                
                if self.curr_vel < 0:
                    self.curr_vel = 0
                    
                self.prev_accel = self.curr_accel
                self.prev_vel = temp_curr_vel

                self.prev_time = self.curr_time
                self.curr_time = time.time()



    def dispatch(self):
        self.dispatched = True
        self.set_power(120000, time.time())

    def set_power(self, power, t = None):
        for f in (self.Failures):
            if self.Failures[f]:
                print("Error {f} failure")
                return 
        
        if(self.dispatched):
            #time updates
            if self.prev_time == 0:
                self.prev_time = t
            else:
                self.prev_time = self.curr_time
            
            self.curr_time = time.time()

            time_elapsed = self.curr_time - self.prev_time
            # if time_elapsed > 0:
            #putting current power into last power and updating current power
            self.curr_power = power

            #current force
            if self.curr_force == 0 or self.prev_vel == 0:
                self.curr_force = self.curr_mass * self.med_accel
            else:
                self.curr_force = float(self.curr_power)/float(self.prev_vel)

            #acceleration
            temp_curr_accel = self.curr_accel
            self.curr_accel = self.curr_force/self.curr_mass

            #updating current velocity and last velocity
            temp_curr_vel = self.curr_vel
            self.curr_vel = self.prev_vel + (time_elapsed/2)*(self.prev_accel+self.curr_accel)
            if self.curr_vel < 0:
                self.curr_vel = 0

            #updating position
            if temp_curr_vel > 0:
                temp_curr_pos = self.curr_pos
                self.curr_pos = self.prev_pos + (time_elapsed/2)*(self.prev_vel +self.curr_vel)
                self.prev_pos = temp_curr_pos
                # print (f'from module:\n{}')
                #updating previous states with current states
                self.prev_vel = temp_curr_vel
                self.prev_accel = temp_curr_accel
            else:
                self.prev_accel = self.curr_accel
                self.prev_vel = self.curr_vel

                
            




