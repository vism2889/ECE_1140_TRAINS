from msg import msg

class out_msg(msg):
	def __init__(self):
		super().__init__()
		self.__vars__ = []
		self.power = None
		self.__vars__.append(self.power)
		self.temperature = None
		self.__vars__.append(self.temperature)
		self.announcement_states = None
		self.__vars__.append(self.announcement_states)
		self.left_door_state = None
		self.__vars__.append(self.left_door_state)
		self.right_door_state = None
		self.__vars__.append(self.right_door_state)
		self.internal_light_state = None
		self.__vars__.append(self.internal_light_state)
		self.external_light_state = None
		self.__vars__.append(self.external_light_state)
		self.service_brake_command = None
		self.__vars__.append(self.service_brake_command)
		self.ebrake_command = None
		self.__vars__.append(self.ebrake_command)
		self.__data_types__.append("float")
		self.__data_types__.append("int")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")
		self.__data_types__.append("bool")


	def serialize(self):
		self.__vars__[0] = self.power
		self.__vars__[1] = self.temperature
		self.__vars__[2] = self.announcement_states
		self.__vars__[3] = self.left_door_state
		self.__vars__[4] = self.right_door_state
		self.__vars__[5] = self.internal_light_state
		self.__vars__[6] = self.external_light_state
		self.__vars__[7] = self.service_brake_command
		self.__vars__[8] = self.ebrake_command
		return self.__serialize__(self.__vars__)

	def deserialize(self, buffer):
		self.__deserialize__(buffer, self.__vars__)
		self.power = self.__vars__[0]
		self.temperature = self.__vars__[1]
		self.announcement_states = self.__vars__[2]
		self.left_door_state = self.__vars__[3]
		self.right_door_state = self.__vars__[4]
		self.internal_light_state = self.__vars__[5]
		self.external_light_state = self.__vars__[6]
		self.service_brake_command = self.__vars__[7]
		self.ebrake_command = self.__vars__[8]