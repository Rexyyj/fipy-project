# boot.py -- run on boot-up
################################
# @Time    : 5/25/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
from _pybytes import Pybytes
from _pybytes_config import PybytesConfig
import pycom
import time

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)
time.sleep(3)
pycom.rgbled(0x00FF00)
