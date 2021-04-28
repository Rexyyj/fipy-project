# main.py -- put your code here!

import pycom
import time
import machine
from pycoproc_2 import Pycoproc

from SI7006A20 import SI7006A20


pycom.heartbeat(False)

py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
    raise Exception('Not a Pysense')
pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True

counter = 0
si = SI7006A20(py)

# send data to screen
if pybytes_enabled:
  while True:
    counter = counter+1
    if counter % 10 ==0:
      pybytes.send_signal(2,si.temperature())
      pybytes.send_signal(3,si.humidity())
    time.sleep(0.5)