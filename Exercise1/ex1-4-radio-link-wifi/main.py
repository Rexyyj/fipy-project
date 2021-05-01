# main.py -- put your code here!
import pycom
from network import WLAN
import machine
import time

pycom.heartbeat(False)

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

for net in nets:
  print(net)

wlan.connect(ssid='Rex_YYJ', auth=(WLAN.WPA2, '11111111'))
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())

def getColor(val):
  one = (255 + 255) / 60
  r=0
  g=0
  b=0
  if val < 30:
    r = int(one * val)
    g = 255
  elif val >= 30 and val < 60:
    r = 255
    g = 255 - (int)((val - 30) * one)
  else:
    r = 255
  return r*0x010000+g*0x0100+b*0x01


while True:
  data =wlan.scan(ssid='Rex_YYJ')
  print(data[0].rssi)
  col = getColor(data[0].rssi/(-100)*90)
  pycom.rgbled(col)
  time.sleep(1)
