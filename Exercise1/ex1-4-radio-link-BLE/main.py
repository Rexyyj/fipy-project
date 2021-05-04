# main.py -- put your code here!
from network import Bluetooth
from machine import Timer
import ubinascii
import pycom
pycom.heartbeat(False)
chrono = Timer.Chrono()
led_on=False

bluetooth = Bluetooth()
bluetooth.start_scan(-1)    # start scanning with no timeout

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

def led_handler(update_alarm):
    global led_on
    if led_on:
        adv = bluetooth.get_adv()
        
        if adv and bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)=='Rex':
            print("set color")
            index = (adv.rssi+30)/(-100)*85
            if index > 0 and index<90:
                col = getColor(index)
            else:
                col = getColor(90)
            pycom.rgbled(col)

update_alarm = Timer.Alarm(led_handler,ms=200, periodic=True)


print("Start printing scaning...")
chrono.start()
while bluetooth.isscanning():
    adv = bluetooth.get_adv()
    if adv:
        name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        if name is not None:
            print(adv)
    
    if chrono.read() > 5:
        led_on=True
        chrono.stop()
        break
print("Stop printing scanning")

# while bluetooth.isscanning():
#     adv = bluetooth.get_adv()
#     if adv and bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)=='Rex':
#         # try:
#         #     bluetooth.connect(adv.mac)
#         # except:
#         #     print("Fail to connect to target")
#         #     continue
#         # print("Connected to device with addr = {}".format(ubinascii.hexlify(target.mac)))
#         pass
#     else:
#         pass
