from winserver import winserver
from TrackMsg import TrackMsg

class MySub:
    def __init__(self):
        self.node = winserver('TrackMsg Subscriber')

        self.TrainModelSub = self.node.subscribe('TrackMsg Topic', TrackMsg, self.my_callback, 1)

    def my_callback(self, msg):
        print(msg.occupancy)
        print(msg.switchStates)
        print(msg.maintenance)
        print(msg.failures)
        print(msg.line)
    
    def spin(self):
        self.node.spin()
    
    def spinOnce(self):
        self.node.spinOnce()        

if __name__ == '__main__':
    ms = MySub()
    ms.spin()