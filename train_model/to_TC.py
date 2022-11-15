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
		self.suggested_speed = None
		self.__vars__.append(self.suggested_speed)
		self.authority = []
		self.__vars__.append(self.authority)
		self.left_door_command = None
		self.__vars__.append(self.left_door_command)
		self.right_door_command = None
		self.__vars__.append(self.right_door_command)
		self.ebrake_command = None
		self.__vars__.append(self.ebrake_command)
		self.service_brake_command = None
		self.__vars__.append(self.service_brake_command)
		self.__data_types__.append("float")
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("bool[]")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")


	def serialize(self):
		self.__vars__[0] = self.current_speed
		self.__vars__[1] = self.commanded_speed
		self.__vars__[2] = self.speed_limit
		self.__vars__[3] = self.suggested_speed
		self.__vars__[4] = self.authority
		self.__vars__[5] = self.left_door_command
		self.__vars__[6] = self.right_door_command
		self.__vars__[7] = self.ebrake_command
		self.__vars__[8] = self.service_brake_command
		return self.__serialize__(self.__vars__)

	def deserialize(self, buffer):
		self.__deserialize__(buffer, self.__vars__)
		self.current_speed = self.__vars__[0]
		self.commanded_speed = self.__vars__[1]
		self.speed_limit = self.__vars__[2]
		self.suggested_speed = self.__vars__[3]
		self.authority = self.__vars__[4]
		self.left_door_command = self.__vars__[5]
		self.right_door_command = self.__vars__[6]
		self.ebrake_command = self.__vars__[7]
		self.service_brake_command = self.__vars__[8]
