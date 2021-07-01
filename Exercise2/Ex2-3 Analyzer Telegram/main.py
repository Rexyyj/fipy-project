# main.py -- put your code here!
################################
# @Time    : 5/28/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : The main code is in boot.py
################################
from network import WLAN
import ubinascii
import time
class Analyzer():
    
    def __init__(self,mode="STA_AP"):
        self.wlan= None
        self.wlan_init(mode)
        self.connectedDevDict = {}

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






if __name__ == "__main__":
    analyser = Analyzer()
    while True:
        newDev,inactivateDev = analyser.analyser()
        print("new device:")
        print(newDev)
        print("inactive device")
        print(inactivateDev)
        time.sleep(5)



    