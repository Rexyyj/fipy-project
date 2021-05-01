# main.py -- put your code here!

import pycom
import time
import machine
from pycoproc_2 import Pycoproc

from SI7006A20 import SI7006A20
from LIS2HH12 import LIS2HH12

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
li = LIS2HH12(py)

def get_col(roll,pitch):
  # deg in range [-180,180]
  # roll_biased = float(roll) + 180
  # ratio_r = int((roll_biased/360)*255)
  # r=65536*ratio_r
  if roll > 5 :
    r = 0xFF0000
  elif roll < -5:
    r = 0x0F0000
  else:
    r = 0x0000FF

  # pitch_baised =float(pitch)+180
  # ratio_p = int((pitch_baised/360)*255)
  # g = 256*ratio_p
  if pitch > 5:
    g = 0xFF00
  elif pitch<-5:
    g = 0x0F00
  else:
    g = 0x0000 


  return r+g

# send data to screen
if pybytes_enabled:
  while True:
    counter = counter+1
    col = get_col(li.roll(),li.pitch())
    pycom.rgbled(col)
    if counter % 100 ==0:
      pass
      # pybytes.send_signal(2,si.temperature())
      # pybytes.send_signal(3,si.humidity())
    time.sleep(0.2)
    



