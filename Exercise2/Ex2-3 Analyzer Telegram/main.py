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
import urequest
import ujson as json
class Analyzer():
    
    def __init__(self,mode="STA_AP"):
        self.wlan= None
        self.wlan_init(mode)
        self.connectedDevDict = {}
        counter = 0 
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


class Telebot():
    
    def __init__(self,token):
        self.chats=set()
        self.url = "https://api.telegram.org/bot"+token


    def update_chats(self):
        info = urequest.request("POST",self.url+"/getUpdates").json()
        for update in info["result"]:
            self.chats.add(update["message"]["chat"]["id"])

    def send_message(self,message):
        msglist = message.split(" ")
        msg = msglist[0]
        if len(msglist)>1:
            for i in range(len(msglist)-1):
                msg = msg+"+"+msglist[i+1]
        
        for chat in self.chats:
            single_msg =self.url+"/sendMessage?chat_id="+str(chat)+"&text="+msg
            response=urequest.request("POST",single_msg).json()
            if response["ok"]=="false":
                self.chats.remove(chat)
    





if __name__ == "__main__":
    analyser = Analyzer()
    telebot = Telebot("1896597789:AAFItPt0tAY3EoLrJ64XNJdEMnPqQBzXRB8")
    telebot.update_chats()
    while True:
        newDev,inactivateDev = analyser.analyser()
        print("new device:")
        print(newDev)
        if len(newDev)!=0:
            for dev in newDev:
                telebot.send_message("Found new device: "+str(dev))
                time.sleep(0.5)
        print("inactive device")
        print(inactivateDev)
        if len(inactivateDev)!=0:
            for dev in inactivateDev:
                telebot.send_message("Device offline: "+str(dev))
                time.sleep(0.5)
        time.sleep(5)


