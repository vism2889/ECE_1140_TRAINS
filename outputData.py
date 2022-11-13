from winserver import winserver
from train_model_msg import in_msg
import random
import time

class OutputData():
    def __init__(self):
        self.node = winserver('my_publisher')
        self.message = in_msg()
        self.pub = self.node.advertise('input', in_msg, 1)

    def sendRandomData(self):
        self.message.announcement_command = random.choice([True, False])
        self.message.commanded_speed = random.randint(10,99)
        self.message.left_door_command = random.choice([True, False])
        self.message.right_door_command = random.choice([True, False])
        self.message.internal_lights_command =  random.choice([True, False])
        self.message.external_lights_command =  random.choice([True, False])
        self.message.ebrake_command =  random.choice([True, False])
        self.message.service_brake_command =  random.choice([True, False])
        self.message.current_speed = random.randint(10,99)
        self.message.temperature_command = random.randint(55,80)
        self.message.suggested_speed = 60
        self.message.speed_limit = 100


        for i in range(2):
            self.message.authority.append(random.choice([True, False]))

    def publish(self):
        self.pub.publish(self.message)

if __name__ == '__main__':
    output = OutputData()

    while True:
        output.sendRandomData()
        output.publish()
        time.sleep(1)
        
        