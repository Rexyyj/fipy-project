# main.py -- put your code here!
################################
# @Time    : 6/15/2021
# @Author  : Yenchia Yu
# @Mail    : jiafish@outlook.com
# @Github  : https://github.com/Rexyyj
################################
import machine
import time
import ujson as json
import _thread
from network import Bluetooth
from SI7006A20 import SI7006A20
from pycoproc_2 import Pycoproc
class MyBleServer():
   
    def __init__(self,userName):
        self.userName = userName
        self.__msg={"from":self.userName, "msg":""}
        
        py = Pycoproc()
        if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
            raise Exception('Not a Pysense')
        self.si = SI7006A20(py)
        
        bluetooth = Bluetooth()
        bluetooth.set_advertisement(name=self.userName, manufacturer_data="Pycom", service_uuid=0xec00)
        bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.conn_cb)
        bluetooth.advertise(True)
        srv1 = bluetooth.service(uuid=0xec00, isprimary=True,nbr_chars=1)
        chr1 = srv1.characteristic(uuid=0xec0e, value='read_from_here')
        chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=self.chr1_handler)
        print('Start BLE service')

    def conn_cb(self,chr):
        events = chr.events()
        if events & Bluetooth.CLIENT_CONNECTED:
            print('client connected')
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            print('client disconnected')
            update = False


    def chr1_handler(self,chr, data):
        events, value = data
        print(data)
        payload = json.loads(value.decode())
        print(payload)
        print("From "+payload["from"]+": "+payload["msg"])
        if events & Bluetooth.CHAR_WRITE_EVENT:
            if payload["msg"].replace(" ","")=="diagnostic":
                    msg = self.get_msg(self.get_disgnostic_content())
                    chr.value(msg)
            else: 
                msglist= payload["msg"].split(" ")
                for submsg in msglist:
                    if submsg == "hello":
                        msg = self.get_msg("Hi I am here!")
                        chr.value(msg)
                        break

    def get_msg(self,content):
        msg = self.__msg
        msg["msg"]=content
        return json.dumps(msg)

    # def publish(self,target,content):
    #     msg = self.__msg
    #     msg["msg"]=content
    #     if target == "all":
    #         self.client.publish(topic="user/broadcast/rx",msg=json.dumps(msg))
    #     else:
    #         self.client.publish(topic="user/"+target+"/rx",msg= json.dumps(msg))


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

    myBleServer  = MyBleServer("Rex_fipy")

    while True:
        time.sleep(1)

    # while True:
    #     msg = input("> ")
    #     if len(msg)>0:
    #         msglist=msg.split(" ")
    #         if len(msglist)>2:
    #             if msglist[0]!="sendto":
    #                 print("Command not exsit!")
    #                 continue
    #             msgToSend = ""
    #             msgLen = len(msglist)
    #             for i in range(2,msgLen):
    #                 msgToSend = msgToSend+msglist[i]+" "
            
    #             myMqtt.publish(msglist[1], msgToSend)
    #         else:
    #             print("Command not exsit!")
        
    