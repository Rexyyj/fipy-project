# main.py -- put your code here!
################################
# @Time    : 5/7/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : None
################################
from network import Bluetooth
from machine import Timer
import ubinascii
import pycom
import time
class BluetoothTest():

    def __init__(self):
        self.chrono = Timer.Chrono()
        self.led_on=False
        self.bluetooth = Bluetooth()
        self.bluetooth.start_scan(-1)    # start scanning with no timeout

    # calculate color according to index in [0,90]
    # when index become lager, color change from green to red
    def getColor(self,val):
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

    def led_handler(self,update_alarm):
        if self.led_on:
            adv = self.bluetooth.get_adv()
            if adv and self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)=='Rex':
                print("rssi = "+str(adv.rssi))
                index = (adv.rssi)/(-150)*90
                col = self.getColor(index)
                pycom.rgbled(col)
    
    def bluetooth_scan(self,t):
        self.led_on=False
        print("Start printing scaning...")
        self.chrono.start()
        while self.bluetooth.isscanning():
            adv = self.bluetooth.get_adv()
            if adv:
                name = self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
                if name is not None:
                    print(self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
                    print(adv)
            
            if self.chrono.read() > t:
                self.chrono.stop()
                break
        print("Stop printing scanning")

    def main(self):
        update_alarm = Timer.Alarm(self.led_handler,ms=200, periodic=True)
        
        self.bluetooth_scan(3)

        while self.bluetooth.isscanning():
            adv = self.bluetooth.get_adv()
            if adv and self.bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)=='Rex':
                print("Find device,connecting...")
                try:
                    self.bluetooth.connect(adv.mac)
                    pass
                except:
                    print("Fail to connect to target")
                    continue
                print("Connected to device with addr = {}".format(ubinascii.hexlify(adv.mac)))
                self.led_on=True
                while True:
                    pass
            else:
                pass
            time.sleep(0.1)

if __name__=="__main__":
    pycom.heartbeat(False)
    btTest =BluetoothTest()
    btTest.main()
