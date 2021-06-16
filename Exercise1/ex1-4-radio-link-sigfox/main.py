# main.py -- put your code here!
################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
from network import Sigfox
import socket
import ubinascii
from machine import Timer
import pycom
import time
pycom.heartbeat(False)
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

# init Sigfox for RCZ4 (Taiwan)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
print("sigfox frequency:"+str(sigfox.frequencies()))
# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(False)

# configure it as DOWNLINK specified by 'True'
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
socket.timeout(20)
s.settimeout(20)



print("sigfox send")
s.send(bytes([1, 2, 3]))
print("send finished")
# await DOWNLINK message
r = s.recv(32)
print(ubinascii.hexlify(r))
rssi = sigfox.rssi()
print("rssi = "+str(rssi))
index = (rssi)/(-150)*85
col = getColor(index)
pycom.rgbled(col)
time.sleep(10)



