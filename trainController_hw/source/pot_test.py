import spidev

while(True):
    bus, device = 0, 0
    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = 1000000
    spi.mode = 0
    msg = [0x00, 0x00]
    spi.xfer2(msg)
    res = spi.xfer2(msg)
    val = (res[0] * 256 + res[1]) >> 6
    print(val * 3.3 / 1024.0)