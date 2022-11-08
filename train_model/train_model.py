from train import Train
from winserver import winserver
from to_TC import to_TC
from from_TC import from_TC

class MyPub:
    def __init__(self, t):
        self.train = t
        self.node =  winserver('TrainModelPublisher')
        self.msg = to_TC()
        self.tc_pub = self.node.advertise('To_Train_Controller', to_TC, 1)
        # self.tm_pub = self.node.advertise('To_Track_Model')
    
    def publish(self):
        self.msg.current_speed = self.train.pm.curr_vel
        self.msg.authority = self.train.authority
        self.msg.commanded_speed = self.train.cmd_speed
        self.msg.speed_limit = self.train.speed_limit
        self.msg.suggested_speed = 0
        self.msg.left_door_command = False
        self.msg.right_door_command = False
        self.msg.ebrake_command = False
        self.msg.service_brake_command = False

        self.tc_pub.publish(self.msg)

class MySub:
    def __init__(self, t):
        self.train = t
        self.node = winserver('TrainControllerSubscriber')
        self.msg = from_TC()
        self.sub = self.node.subscribe('my_topic', self.msg, 1, "192.168.0.10")
    
    def call_back(self, msg):
        print(msg.power)
        print(msg.temperature)
        




def tc_inputs():
    pass
def tm_inputs():
    pass
def tc_outputs():
    pass
def tm_outputs():
    pass

if __name__ == "__main__":
    t = Train()
    mp = MyPub(t)
    train_dict = {}
    print("done")

