# main.py -- put your code here!
################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
import pycom
from network import WLAN
import machine
import time

# calculate color according to index in [0,90]
# when index become lager, color change from green to red
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



while True:
  data =wlan.scan(ssid='Rex_YYJ')
  print("rssi: "+str(data[0].rssi)+" channel: "+str(data[0].channel))
  col = getColor(data[0].rssi/(-100)*90)
  pycom.rgbled(col)
  time.sleep(1)
