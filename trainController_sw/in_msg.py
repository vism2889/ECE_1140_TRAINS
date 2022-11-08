from msg import msg

class in_msg(msg):
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
		self.temperature_command = None
		self.__vars__.append(self.temperature_command)
		self.authority = []
		self.__vars__.append(self.authority)
		self.left_door_command = None
		self.__vars__.append(self.left_door_command)
		self.right_door_command = None
		self.__vars__.append(self.right_door_command)
		self.internal_light_command = None
		self.__vars__.append(self.internal_light_command)
		self.external_light_command = None
		self.__vars__.append(self.external_light_command)
		self.announce_command = None
		self.__vars__.append(self.announce_command)
		self.ebrake_command = None
		self.__vars__.append(self.ebrake_command)
		self.service_brake_command = None
		self.__vars__.append(self.service_brake_command)
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("int")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")


	def serialize(self):
		self.__vars__[0] = self.current_speed
		self.__vars__[1] = self.commanded_speed
		self.__vars__[2] = self.speed_limit
		self.__vars__[3] = self.suggested_speed
		self.__vars__[4] = self.temperature_command
		self.__vars__[5] = self.authority
		self.__vars__[6] = self.left_door_command
		self.__vars__[7] = self.right_door_command
		self.__vars__[8] = self.internal_light_command
		self.__vars__[9] = self.external_light_command
		self.__vars__[10] = self.announce_command
		self.__vars__[11] = self.ebrake_command
		self.__vars__[12] = self.service_brake_command
		return self.__serialize__(self.__vars__)

	def deserialize(self, buffer):
		self.__deserialize__(buffer, self.__vars__)
		self.current_speed = self.__vars__[0]
		self.commanded_speed = self.__vars__[1]
		self.speed_limit = self.__vars__[2]
		self.suggested_speed = self.__vars__[3]
		self.temperature_command = self.__vars__[4]
		self.authority = self.__vars__[5]
		self.left_door_command = self.__vars__[6]
		self.right_door_command = self.__vars__[7]
		self.internal_light_command = self.__vars__[8]
		self.external_light_command = self.__vars__[9]
		self.announce_command = self.__vars__[10]
		self.ebrake_command = self.__vars__[11]
		self.service_brake_command = self.__vars__[12]