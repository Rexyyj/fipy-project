import paho.mqtt.client as PahoMQTT
import json
import time
class MyMqtt:
    def __init__(self, clientId,userName):
        self.broker = "test.mosquitto.org"
        self.port = 1883
        self.notifier = self.notify
        self.clientID = clientId
        self.userName = userName
        self._topic = ""
        self._isSubscriber = False
        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(self.clientID,True)
        # register the callback
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
        self.__msg={"from":self.userName, "msg":""}

    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
        print ("Connected to %s with result code: %d" % (self.broker, rc))

    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
        # A new message is received
        self.notifier(msg.topic, msg.payload)

    def myPublish (self, target, content):
        msg = self.__msg
        msg["msg"]=content
        if target == "all":
            self._paho_mqtt.publish("user/broadcast/rx", json.dumps(msg), 2)
        else:
            self._paho_mqtt.publish("user/"+target+"/rx", json.dumps(msg), 2)
    

    def mySubscribe (self, topic):

        # subscribe for a topic
        self._paho_mqtt.subscribe(topic, 2)
        # just to remember that it works also as a subscriber
        self._isSubscriber = True
        self._topic = topic
        print ("subscribed to %s" % (topic))

    def start(self):
        #manage connection to broker
        self._paho_mqtt.connect(self.broker , self.port)
        self._paho_mqtt.loop_start()
        self.mySubscribe("user/broadcast/rx")
        self.mySubscribe("user/"+self.userName+"/rx")

    def unsubscribe(self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

    def stop (self):
        if (self._isSubscriber):
            # remember to unsuscribe if it is working also as subscriber
            self._paho_mqtt.unsubscribe(self._topic)

        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()
    
    def notify(self,topic,msg):
        payload = json.loads(msg)
        if payload["from"]==self.userName:
            pass
        else:
            print("From "+payload["from"]+": "+payload["msg"])

    

if __name__ == "__main__":
    myMqtt = MyMqtt("desktop0", "rexYu_desktop")
    myMqtt.start()
    time.sleep(3)
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
                myMqtt.myPublish(msglist[1], msgToSend)
            else:
                print("Command not exsit!")