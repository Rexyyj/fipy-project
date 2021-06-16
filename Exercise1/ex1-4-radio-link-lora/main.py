# main.py -- put your code here!
################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################

from network import LoRa
import socket
import time
import ubinascii
import pycom

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

# disable heartbeat led
pycom.heartbeat(False)

# Initialise LoRa in LORAWAN mode.
# Device located in Taiwan, pick Asia region: LoRa.AS923
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.AS923)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00423E5')
app_key = ubinascii.unhexlify('F4E15BEA1F605E7D8DDF1E9E87D8A499')
dev_eui = ubinascii.unhexlify('00175883753B3C44')

lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')
print('Joined')

# create a LoRa socket

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

while True:
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))

    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)
    stat = lora.stats()
    print(stat)
    print(data)
    print("tx frequency = "+str(stat.tx_frequency))
    col = (stat.rssi)/(-150)*85
    pycom.rgbled(int(col))
    time.sleep(2)
