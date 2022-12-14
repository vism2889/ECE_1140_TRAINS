from msg import msg

class to_TC(msg):
	def __init__(self):
		super().__init__()
		self.__vars__ = []
		self.current_speed = None
		self.__vars__.append(self.current_speed)
		self.commanded_speed = None
		self.__vars__.append(self.commanded_speed)
		self.speed_limit = None
		self.__vars__.append(self.speed_limit)
		self.authority = None
		self.__vars__.append(self.authority)
		self.next_station = None
		self.__vars__.append(self.next_station)
		self.brake_failure = None
		self.__vars__.append(self.brake_failure)
		self.engine_failure = None
		self.__vars__.append(self.engine_failure)
		self.signalPickup_failure = None
		self.__vars__.append(self.signalPickup_failure)
		self.__data_types__.append("float")
		self.__data_types__.append("float")
		self.__data_types__.append("float")
		self.__data_types__.append("float")
		self.__data_types__.append("string")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")


	def serialize(self):
		self.__vars__[0] = self.current_speed
		self.__vars__[1] = self.commanded_speed
		self.__vars__[2] = self.speed_limit
		self.__vars__[3] = self.authority
		self.__vars__[4] = self.next_station
		self.__vars__[5] = self.brake_failure
		self.__vars__[6] = self.engine_failure
		self.__vars__[7] = self.signalPickup_failure
		return self.__serialize__(self.__vars__)

	def deserialize(self, buffer):
		self.__deserialize__(buffer, self.__vars__)
		self.current_speed = self.__vars__[0]
		self.commanded_speed = self.__vars__[1]
		self.speed_limit = self.__vars__[2]
		self.authority = self.__vars__[3]
		self.next_station = self.__vars__[4]
		self.brake_failure = self.__vars__[5]
		self.engine_failure = self.__vars__[6]
		self.signalPickup_failure = self.__vars__[7]
