import paho.mqtt.client as mqtt
import BTvehicle
import sys
import socket
import ipaddress
import subprocess
import time
import sys
import json
sys.path.append('./assets')

import findIP

vehicleData = json.load(open('PI/CONFIG.json'))
uid     = vehicleData["uid"]
typ     = vehicleData["type"]
loc     = vehicleData["location"]
status  = vehicleData["status"]
pos     = vehicleData["position"]

VehiDetailArg=[uid,typ,loc,status,pos]
class CarClient:
    def __init__(self):
        self.vehi=BTvehicle.BTvehicle()
        self.PORT=10250
        self.HOST=False
        while not self.HOST:
            self.HOST=self.findHost()
            time.sleep(10)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
        self.client.subscribe("ASST/"+uid)
        # self.vehi.connect() #currently dont in init itsef

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        self.msgParser(msg.payload)

    def connect(self):
        self.client.connect(self.HOST, port=self.PORT, keepalive=60)
        self.client.loop_forever()
    def findHost(self):
        print("Finding connected devices")
        connectedHosts= findIP.getIPs()
        print(connectedHosts)
        self.serveClient = mqtt.Client()
        for i in connectedHosts:
            try:
                self.serveClient.connect(i, port=self.PORT, keepalive=1)
                self.serveClient.publish('register',VehiDetailArg, qos=1)
                print('HOST selected: ',i)
                return str(i)
            except:
                pass
        try:
            self.serveClient.connect('127.0.0.1', port=self.PORT, keepalive=1)
            self.serveClient.publish('register',VehiDetailArg, qos=1)
            print('HOST: 127.0.0.1')
            return '127.0.0.1'
        except:
            return False
    def msgParser(self,msg):
        self.vehi.sendMsg(str(msg.payload))
        


print(uid,typ,loc,status,pos)

cl=CarClient()
cl.connect()
print("done")