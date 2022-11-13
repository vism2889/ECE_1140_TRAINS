## Imports for the winserver library
from winserver import winserver
from TrackMsg import TrackMsg

class MySub:
    def __init__(self):

        ## Instantiate the MySub class as a 
        #   node with a name of 'my_subscriber'
        self.node = winserver('my_subscriber')

        ## Create a subscriber that listens to the topic 'my_topic'
        self.sub = self.node.subscribe('TrackMsg', TrackMsg, self.my_callback, 1)

    def my_callback(self, msg):
        
        ## Do things with the data coming in 
        #   Here we just print the values of 
        #   each variable found in my_msg.msg
        print(TrackMsg.line)
    
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