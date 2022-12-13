from train import Train
from winserver import winserver
from to_TC import to_TC
from from_TC import from_TC
import time


class MyPub:
    def __init__(self, t):
        self.train = t
        self.node =  winserver('TrainModelPublisher')
        # message for train controller hw
        self.tc_message = to_TC()
        self.tc_pub = self.node.advertise('To_Train_Controller', to_TC, 1, "192.168.0.15")    
        
    def publish(self):
        self.tc_message.current_speed = self.train.pm.curr_vel
        self.tc_message.authority = self.train.pm.train_authority
        self.tc_message.commanded_speed = self.train.pm.cmdSpeed
        self.tc_message.speed_limit = self.train.pm.speedLimit
        self.tc_message.next_station = self.train.next_station
        self.tc_message.brake_failure = self.train.brake_failure
        self.tc_message.signalPickup_failure = self.train.signal_pickup_failure
        self.tc_message.engine_failure = self.train.train_engine_failure
       
        self.tc_pub.publish(self.tc_message)

class MySub:
    def __init__(self, t):
        self.train = t
        self.node = winserver('TrainControllerSubscriber')
        self.msg = from_TC()
        self.sub = self.node.subscribe('To_Train_Model', from_TC, self.call_back, 1)

        self.power = 0.0
    
    def call_back(self, msg):
        
        self.train.pm.power = msg.power
        self.power = msg.power

        self.train.temperature = msg.temperature

        self.train.announcements = msg.announcement_states
        
        self.train.left_doors = msg.left_door_state
        
        self.train.right_doors = msg.right_door_state
        
        self.train.int_lights = msg.internal_light_state
        
        self.train.ext_lights = msg.external_light_state
        
        self.train.service_brake = msg.service_brake_command
        
        self.train.e_brake = msg.ebrake_command

    def spinOnce(self):
        self.node.spinOnce()

    def get_power(self):
        return self.power
       

if __name__ == "__main__":
    t = Train()
    t.dispatch()
    mp = MyPub(t)
    ms = MySub(t)
    train_dict = {}
    while True:
        ms.spinOnce()
        t.set_power(ms.get_power())
        time.sleep(.1)
        print("train.pm.curr_vel = %5.2f" % t.pm.curr_vel)
        mp.publish()
        time.sleep(.1)
