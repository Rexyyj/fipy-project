# boot.py -- run on boot-up
import pycom
import time

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

time.sleep(1)
pycom.rgbled(0x00FF00)
time.sleep(1)
