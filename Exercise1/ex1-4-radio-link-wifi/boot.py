# boot.py -- run on boot-up
from _pybytes import Pybytes
import pycom
import time

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

pycom.pybytes_on_boot(False)
time.sleep(1)
pycom.rgbled(0x00FF00)
time.sleep(1)