################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
import pycom
import time

pycom.heartbeat(False)

while True:
    pycom.rgbled(0xFF0000)
    time.sleep(1)
    pycom.rgbled(0x00FF00)
    time.sleep(1)
    pycom.rgbled(0x0000FF)
    time.sleep(1)
