# main.py -- put your code here!
################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
import pycom
import time
from machine import Timer
from pycoproc_2 import Pycoproc
from network import Bluetooth

from SI7006A20 import SI7006A20
from LIS2HH12 import LIS2HH12

pycom.heartbeat(False)

ble_ready = False
wifi_ready = False
temp=0.0
hum=0.0
# check device
py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
  raise Exception('Not a Pysense')
# check pybyte
if 'pybytes' in globals():
  if(pybytes.isconnected()):
    wifi_ready=True
    print('Pybytes is connected, sending signals to Pybytes')

# enable BLE
def conn_cb(chr):
  global ble_ready
  events = chr.events()
  if events & Bluetooth.CLIENT_CONNECTED:
    print('client connected')
  elif events & Bluetooth.CLIENT_DISCONNECTED:
    print('client disconnected')
    ble_ready = False

def chr1_handler(chr, data):
  global temp
  global hum
  global ble_ready
  events = chr.events()
  print("events: ",events)
  if events & (Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT):
    val ="temp:"+str(round(temp, 2))+" hum:"+str(round(hum,2))
    chr.value(val)
    if (events & Bluetooth.CHAR_SUBSCRIBE_EVENT):
      ble_ready = True

bluetooth = Bluetooth()
bluetooth.set_advertisement(name='fiPy_rex', manufacturer_data="Pycom", service_uuid=0xec00)

bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)
bluetooth.advertise(True)
srv1 = bluetooth.service(uuid=0xec00, isprimary=True,nbr_chars=1)
chr1 = srv1.characteristic(uuid=0xec0e, value='read_from_here') #client reads from here
chr1.callback(trigger=(Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_SUBSCRIBE_EVENT), handler=chr1_handler)


counter = 0
si = SI7006A20(py)
li = LIS2HH12(py)

def get_col(roll,pitch):
  if roll > 5 :
    r = 0xFF0000
  elif roll < -5:
    r = 0x0F0000
  else:
    r = 0x0000FF

  if pitch > 5:
    g = 0xFF00
  elif pitch<-5:
    g = 0x0F00
  else:
    g = 0x0000 
  return r+g


# define handlers
def data_update_handler(update_alarm):
  global temp
  global hum
  temp = si.temperature()
  hum = si.humidity()

def wifi_handler(update_alarm):
  global wifi_ready
  global temp
  global hum
  print("wifi handler running")
  if wifi_ready:
    pybytes.send_signal(2,temp)
    pybytes.send_signal(3,hum)
    

def ble_handler(update_alarm):
  global ble_ready
  global temp
  global hum
  print("ble handler running")
  if ble_ready:
    chr1.value("temp:"+str(round(temp, 2))+" hum:"+str(round(hum,2)))

def led_handler(update_alarm):
  col = get_col(li.roll(),li.pitch())
  pycom.rgbled(col)

update_alarm1 = Timer.Alarm(data_update_handler,s=1, periodic=True)
update_alarm2 = Timer.Alarm(led_handler,ms=500, periodic=True) 
update_alarm3 = Timer.Alarm(ble_handler,s=5, periodic=True) 
update_alarm4 = Timer.Alarm(wifi_handler,s=10, periodic=True) 





