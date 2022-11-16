import random
from time import sleep

## Imports for the winserver library
from winserver import winserver
from track_model_msg import track_model_msg ## Generated Message

class MyPub:
    def __init__(self):
        
        ## Instantiate the MySub class as a 
        #   node with a name of 'my_publisher'
        self.node = winserver('my_publisher')
        
        ## Create an instance of the message
        #   that we will send over the server
        self.msg = my_msg()

        ## Create a publisher object for us
        #   to advertise on 
        self.pub = self.node.advertise('my_topic', my_msg, 1)

    def publishRand(self):
        
        ## Randomize a list of booleans
        for i in range(10):
            self.msg.my_bool_arr.append(random.choice([True, False]))
        
        ## Generate a random float between
        #   0 and 1
        self.msg.my_float = random.random()

        ## Generate a random number string
        self.msg.my_str = f'string number {random.randint(0, 5)}'
        
        ## Generate a random integer between
        #   0 and 1000
        self.msg.my_int = random.randint(0, 1000)

        ## Publish the message to any subscribers
        self.pub.publish(self.msg)


if __name__ == '__main__':

    mp = MyPub()

    while True:
        mp.publishRand()        
        sleep(1.0) ## Publish every 1.0 seconds