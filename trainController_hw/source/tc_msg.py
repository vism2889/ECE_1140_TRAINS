from msg import msg

class tc_msg(msg):
	def __init__(self):
		super().__init__()
		self.__vars__ = []
		self.commandedSpeed = None
		self.__vars__.append(self.commandedSpeed)
		self.currentSpeed = None
		self.__vars__.append(self.currentSpeed)
		self.speedLimit = None
		self.__vars__.append(self.speedLimit)
		self.announcements = None
		self.__vars__.append(self.announcements)
		self.authority = []
		self.__vars__.append(self.authority)
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool[]")


	def serialize(self):
		self.__vars__[0] = self.commandedSpeed
		self.__vars__[1] = self.currentSpeed
		self.__vars__[2] = self.speedLimit
		self.__vars__[3] = self.announcements
		self.__vars__[4] = self.authority
		return self.__serialize__(self.__vars__)

	def deserialize(self, buffer):
		self.__deserialize__(buffer, self.__vars__)
		self.commandedSpeed = self.__vars__[0]
		self.currentSpeed = self.__vars__[1]
		self.speedLimit = self.__vars__[2]
		self.announcements = self.__vars__[3]
		self.authority = self.__vars__[4]
