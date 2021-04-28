# boot.py -- run on boot-up
from _pybytes import Pybytes
from _pybytes_config import PybytesConfig
import pycom
import time

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)

conf = PybytesConfig().read_config()
pybytes = Pybytes(conf)
pybytes.start()
while not pybytes.isconnected():
  pass

pycom.rgbled(0x00FF00)
time.sleep(3)