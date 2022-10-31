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

last_read = 0
tolerance = 250

def remap_range(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    valueScaled = int(value - left_min) / int(left_span)

    return int(right_min + (valueScaled * right_span))

def getSliderValue():
    set_value = 0
    trim_pot_changed = False
    trim_pot = chan0.value
    pot_adjust = abs(trim_pot - last_read)

    if pot_adjust > tolerance:
        trim_pot_changed = True

    if trim_pot_changed:
        set_value = remap_range(trim_pot, 0, 65535, 0, 100)

    time.sleep(.1)

    return set_value