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
        self.counter=0
        self.message=""
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
        self.chr = chr1

    def conn_cb(self,chr):
        events = chr.events()
        if events & Bluetooth.CLIENT_CONNECTED:
            print('client connected')
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            print('client disconnected')
            update = False


    def chr1_handler(self,chr, data):
        events, value = data
        payload = value.decode()
        if events & Bluetooth.CHAR_WRITE_EVENT:
            self.counter=5
            self.message+=payload
            pass

    def start_response_service(self):
        _thread.start_new_thread(self.aggrate_message, ())


    def aggrate_message(self):
        while True:
            while self.counter>0:
                self.counter=self.counter-1
                if self.counter == 0:
                    self.action_and_feedback(self.message)
                    self.message=""
                time.sleep(0.1)


    def action_and_feedback(self,payload):
        re_msg = "error"
        command,target,msg = self.split_payload(payload)
        print("Received message: "+msg)
        if command=="sendto":
            if target==self.userName:
                temp = msg.split(" ")
                if msg == "diagnostic":
                    re_msg = "From "+self.userName+": "+self.get_disgnostic_content()
                elif "hello" in temp:
                    re_msg = "From "+self.userName+": hi there"
            else:
                temp = msg.split(" ")
                if "hello" in temp:
                    re_msg = "From "+self.userName+": hay I am here too!"
            
            if len(re_msg)>20:
                sendtime =int(len(re_msg)/20)
                sendlist = []
                for i in range(sendtime):
                    temp_msg = re_msg[(i*20):(20+i*20)]
                    sendlist.append(temp_msg)
                self.chr.value(re_msg[(20*sendtime):])  
                time.sleep(0.1)
                sendlist.reverse()
                for send in sendlist:
                    self.chr.value(send)
                    time.sleep(0.1)
            else:              
                self.chr.value(re_msg)
        else:
            pass


    def split_payload(self,payload):
        payloadlist = payload.split(" ")
        command = ""
        target =""
        msg = ""
        if len(payloadlist)>=3:
            command = payloadlist[0]
            target = payloadlist[1]
            msg = payloadlist[2]
        if len(payloadlist)>3:
            for i in range(len(payloadlist)-3):
                msg = msg+" "+payloadlist[i+3]
        return command,target,msg
    


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

    myBleServer  = MyBleServer("fipy")
    myBleServer.start_response_service()
    while True:
        time.sleep(1)


        
    