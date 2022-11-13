from msg import msg 

class TrackMsg(msg):
    def __init__(self):
        super().__init__()
        self.__vars__ = []
        self.occupancy = [] # bool array
        self.__vars__.append(self.occupancy)
        self.switchStates = [] # bool array
        self.__vars__.append(self.switchStates)
        self.maintenance = [] # bool array 
        self.__vars__.append(self.maintenance)
        self.failures = [] # integer array
        self.__vars__.append(self.failures)
        #self.line = None # string
        #self.__vars__.append(self.line)

        self.__data_types__.append("bool[]")
        self.__data_types__.append("bool[]")
        self.__data_types__.append("bool[]")
        self.__data_types__.append("int[]")
        #self.__data_types__.append("string")

    def serialize(self):
        self.__vars__[0] = self.occupancy
        self.__vars__[1] = self.switchStates
        self.__vars__[2] = self.maintenance
        self.__vars__[3] = self.failures
        #self.__vars__[4] = self.line
        return self.__serialize__(self.__vars__)

    def deserialize(self, buffer):
        self.__deserialize__(buffer, self.__vars__)
        self.occupancy = self.__vars__[0]
        self.switchStates = self.__vars__[1]
        self.maintenance = self.__vars__[2]
        self.failures = self.__vars__[3]
        #self.line = self.__vars__[4]



