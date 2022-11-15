import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)

class AnalogIn():
    def __init__(self):
        self.last_read1 = 0
        self.last_read2 = 0
        self.tolerance = 2000

    def remap_range(self, value, left_min, left_max, right_min, right_max):
        left_span = left_max - left_min
        right_span = right_max - right_min
        valueScaled = int(value - left_min) / int(left_span)

        return int(right_min + (valueScaled * right_span))

    # speed slider
    def getSpeedValue(self):
        set_value = 0
        trim_pot_changed = False
        trim_pot = chan0.value
        pot_adjust = abs(trim_pot - self.last_read1)

        if pot_adjust > self.tolerance:
            trim_pot_changed = True

        if trim_pot_changed:
            set_value = self.remap_range(trim_pot, 0, 65535, 0, 100)

        time.sleep(.1)
        return set_value

    def getBrakingValue(self):
        set_value = False
        trim_pot_changed = False
        trim_pot = chan0.value
        pot_adjust = abs(trim_pot - self.last_read1)

        if pot_adjust < self.tolerance:
            trim_pot_changed = True

        if trim_pot_changed:
            set_value = True
        
        time.sleep(.1)
        return set_value

    # temperature potentiometer
    def getTemperatureValue(self):
        set_value = 0
        trim_pot_changed = False
        trim_pot = chan1.value
        pot_adjust = abs(trim_pot - self.last_read2)

        if pot_adjust > self.tolerance:
            trim_pot_changed = True

        if trim_pot_changed:
            set_value = self.remap_range(trim_pot, 0, 65535, 0, 100)

        time.sleep(.1)
        return set_value