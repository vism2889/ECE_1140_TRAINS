from train import Train
from winserver import winserver
from to_TC import to_TC
from from_TC import from_TC
import time


class MyPub:
    def __init__(self, t):
        self.train = t
        self.node =  winserver('TrainModelPublisher')

        #message for train controllers
        self.tc_msg = to_TC()
        self.tc_pub = self.node.advertise('To_Train_Controller', to_TC, 1, "192.168.0.15")    
    def publish(self):
        self.tc_msg.current_speed = self.train.pm.curr_vel
        self.tc_msg.authority = self.train.authority
        self.tc_msg.commanded_speed = self.train.cmd_speed
        self.tc_msg.speed_limit = self.train.speed_limit
        self.tc_msg.next_station = self.train.next_station
        self.tc_msg.brake_failure = self.train.brake_failure
        self.tc_msg.signalPickup_failure = self.train.signal_pickup_failure
        self.tc_msg.engine_failure = self.train.train_engine_failure
       
        self.tc_pub.publish(self.tc_msg)

# class MySub:
#     def __init__(self):
#         self.node = winserver('TrainControllerSubscriber')
#         self.msg = from_TC()
#         self.sub = self.node.subscribe('To_Train_Model', from_TC , 1, "192.168.0.10")
    
#     def call_back(self, msg):
#         self.power = self.msg.power
#         self.temperature = self.msg.temperature
#         self.announcement_states = self.msg.announcement_states
#         self.left_door_state = self.left_door_state
#         self.right_door_state = self.right_door_state
#         self.internal_light_state = self.internal_light_state
#         self.external_light_state = self.external_light_state
#         self.service_brake_command = self.service_brake_command
#         self.ebrake_command = self.msg.ebrake_command
#         print(self.msg.ebrake_command)
    
#     def spinOnce(self):
#         self.node.spinOnce()
        

if __name__ == "__main__":
    t = Train()
    t.dispatch()
    mp = MyPub(t)
    # ms = MySub()
    train_dict = {}
    while True:
        time.sleep(2)
        p = 120000
        print('setting power')
        t.set_power(p)
        time.sleep(1)
        print(f"before publisher train.pm.curr_vel = {t.pm.curr_vel}")
        mp.publish()
        print("done")



        # ms.spinOnce()
