from winserver import winserver
from tc_msg import tc_msg

class TrainData:
    def __init__(self):

        ## Instantiate the MySub class as a 
        #   node with a name of 'my_subscriber'
        self.node = winserver('my_subscriber')

        ## Create a subscriber that listens to the topic 'my_topic'
        self.sub = self.node.subscribe('my_topic', tc_msg, self.my_callback, 1)

    def my_callback(self, msg):
        
        ## Do things with the data coming in 
        #   Here we just print the values of 
        #   each variable found in my_msg.msg
        print(msg.my_int)
        print(msg.my_str)
        print(msg.my_float)
        print(msg.my_bool)
    
    def spin(self):

        ## Loopback to check the subscribe queue
        #   and process the callback. This function
        #   loops infinitely until the program exits
        self.node.spin()
    
    def spinOnce(self):

        ## Loopback to check the subscribe queue
        #   and process the callback. This function
        #   loops ONCE and then finishes 
        self.node.spinOnce()        