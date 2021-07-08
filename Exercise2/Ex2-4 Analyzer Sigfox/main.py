# main.py -- put your code here!
################################
# @Time    : 5/30/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : The main code is in boot.py
################################
from network import WLAN
import ubinascii
import time
import ujson as json
class Analyzer():
    
    def __init__(self,mode="STA_AP"):
        self.wlan= None
        self.wlan_init(mode)
        self.connectedDevDict = {}
        counter = 0 
        if mode == "STA_AP":
            while True:
                if self.wlan.isconnected()==True:
                    print("Connected to wlan")
                    break
                else:
                    counter+=1
                if counter>10:
                    raise Exception("wlan connection fail")
                time.sleep(1)

    def wlan_init(self,mode):
        if self.wlan != None:
            raise ValueError()

        if mode == "STA_AP":
            self.wlan = WLAN(mode = WLAN.STA_AP,ssid = 'fipy_AP')
            self.wlan.connect(ssid = 'Rex_YYJ',auth = (WLAN.WPA2,'11111111'))
        elif mode =="AP":
            self.wlan = WLAN(mode = WLAN.AP,ssid = 'fipy_AP')
        else:
            raise ValueError()

    def analyser(self):
        staList = self.wlan.ap_sta_list()
        currentTimestamp = time.time()
        existKeys = self.connectedDevDict.keys()
        tempDict = self.connectedDevDict.copy()
        newDev = []
        inactivateDev = []
        # Update dictionay
        for sta in staList:
            mac = ubinascii.hexlify(sta.mac).decode()
            if mac in existKeys:
                self.connectedDevDict[mac]=currentTimestamp
                del tempDict[mac]
            else:
                self.connectedDevDict[mac]=currentTimestamp
                newDev.append(mac)
        # Check inactive device
        for key in tempDict.keys():
            passedTime =(currentTimestamp - tempDict[key])/60.0
            if passedTime>5:
                inactivateDev.append(key)
                del self.connectedDevDict[key]
        
        return newDev,inactivateDev


from network import Sigfox
import socket

class SigfoxSender():
    def __init__(self):
        self.sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ4)
        self.s = None
        self.socketConfig(False, False)

    def socketConfig(self,blocking,downLink):
        if self.s == None:
            self.s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
            self.s.setblocking(blocking)
            self.s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, downLink)
            socket.timeout(20)
            self.s.settimeout(20)
        else:
            raise ValueError()

    def send_message(self,msg):
        self.s.send(msg)



if __name__ == "__main__":
    analyser = Analyzer(mode="AP")
    sigfoxSender = SigfoxSender()
    while True:
        newDev,inactivateDev = analyser.analyser()
        print("new device:")
        print(newDev)
        if len(newDev)!=0:
            for dev in newDev:
                sigfoxSender.send_message(dev)
                time.sleep(5)
        time.sleep(5)


