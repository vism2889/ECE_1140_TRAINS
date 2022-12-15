class PIController:
    def __init__(self, kp, ki, kd, output_min, output_max, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max
        self.setpoint = setpoint
        self.error_sum = 0.0
        self.prev_error = 0.0

    def setSetpoint(self, setpoint):
        self.setpoint = setpoint

    # using two different update methods provides diversity and redundancy to the power calculation
    def update1(self, measurement):
        self.error = self.setpoint - measurement
        derivative = self.error - self.prev_error
        self.error_sum += self.error
        output = self.kp * self.error + self.ki * self.error_sum + self.kd * derivative
        output = min(output, self.output_max)
        output = max(output, self.output_min)
        self.prev_error = self.error
        return output

    def update2(self, measurement):
        self.error = self.setpoint - measurement
        derivative = self.error - self.prev_error
        self.error_sum += self.error
        output = self.kp * self.error + self.ki * derivative + self.kd * self.error_sum
        output = min(output, self.output_max)
        output = max(output, self.output_min)
        self.prev_error = self.error
        return output