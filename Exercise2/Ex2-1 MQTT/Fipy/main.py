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
from SI7006A20 import SI7006A20
from pycoproc_2 import Pycoproc
class MyMqtt():
   
    def __init__(self,clientId,userName):
        self.clientId = clientId
        self.userName = userName
        self.client = MQTTClient(self.clientId, "test.mosquitto.org",port=1883)
        self.client.set_callback(self.sub_cb)
        self.__msg={"from":self.userName, "msg":""}
        py = Pycoproc()
        if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
            raise Exception('Not a Pysense')
        self.si = SI7006A20(py)
            
        
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
        topic = topic.decode()
        if payload["from"]==self.userName:
            pass
        else:
            print(topic)
            print("From "+payload["from"]+": "+payload["msg"])
            if topic == "user/broadcast/rx":
                if payload["msg"].replace(" ","")=="diagnostic":
                    self.publish(payload["from"], self.get_disgnostic_content())
                else: 
                    msglist= payload["msg"].split(" ")
                    for submsg in msglist:
                        if submsg == "hello":
                            self.publish(payload["from"], "Hi I am here!")
                            break

            elif topic=="user/"+self.userName+"/rx":
                if payload["msg"].replace(" ","")=="diagnostic":
                    self.publish(payload["from"], self.get_disgnostic_content())
                elif 'hello' in payload["msg"].split(" "):
                    self.publish(payload["from"], "Hi "+payload["from"]+"!")
                else:
                    pass


    def get_disgnostic_content(self):
        temp = self.si.temperature()
        status = ""
        if temp<10:
            status= "cold"
        elif temp<25:
            status= "cool"
        elif temp<35:
            status= "warm"
        else:
            status="hot"
        content = "It's "+status+" here! The temperature is "+str(round(temp,2))+" degree Celsius."
        return content
        

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
        
    