# main.py -- put your code here!
################################
# @Time    : 5/25/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
# @Note    : The main code is in boot.py
################################
from mqtt import MQTTClient
from network import WLAN
import machine
import time
import ujson as json
import _thread

class MyMqtt():
   
    def __init__(self,clientId,userName):
        self.clientId = clientId
        self.userName = userName
        self.client = MQTTClient(self.clientId, "test.mosquitto.org",port=1883)
        self.client.set_callback(self.sub_cb)
        self.__msg={"from":self.userName, "msg":""}
        
    def check_msg_update(self):
        while True:
            self.client.check_msg()
            time.sleep(1)

    def start(self):
        self.client.connect()
        self.client.subscribe(topic="user/"+self.userName+"/rx")
        self.client.subscribe(topic="user/broadcast/rx")
        _thread.start_new_thread(self.check_msg_update,())


    def publish(self,target,content):
        msg = self.__msg
        msg["msg"]=content
        if target == "all":
            self.client.publish(topic="user/broadcast/rx",msg=json.dumps(msg))
        else:
            self.client.publish(topic="user/"+target+"/rx",msg= json.dumps(msg))

    def sub_cb(self,topic, msg):
        payload = json.loads(msg)
        if payload["from"]==self.userName:
            pass
        else:
            print("From "+payload["from"]+": "+payload["msg"])

if __name__ == "__main__":
    wlan = WLAN(mode=WLAN.STA)
    wlan.connect("Rex_YYJ", auth=(WLAN.WPA2, "11111111"), timeout=5000)

    while not wlan.isconnected():  
        machine.idle()
    print("Connected to WiFi\n")

    myMqtt = MyMqtt("fipy0","rexYu_Fipy")
    myMqtt.start()

    while True:
        msg = input("> ")
        if len(msg)>0:
            msglist=msg.split(" ")
            if len(msglist)>2:
                if msglist[0]!="sendto":
                    print("Command not exsit!")
                    continue
                msgToSend = ""
                msgLen = len(msglist)
                for i in range(2,msgLen):
                    msgToSend = msgToSend+msglist[i]+" "
            
                myMqtt.publish(msglist[1], msgToSend)
            else:
                print("Command not exsit!")
        
    