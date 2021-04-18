import json
import network
import time
from umqtt.simple import MQTTClient

class SmokeyController():
    def __init__(self,envFile,envBackupFile,maxWifiTries = 10, maxMQTTTries = 3):
        self.nic = network.WLAN(network.STA_IF)
        self.env = None
        self.currentEnvFile = envFile
        self.currentEnvBackupFile = envBackupFile
        self.loadEnv(envFile)
        while not self.connectWifi(maxWifiTries):
            self.currentEnvBackupFile = self.currentEnvFile
            self.loadEnv(self.currentEnvFile)
            envBackupFile = self.currentEnvFile



        if not self.connectMQTT(maxMQTTTries):
            self

    def run(self):
        print("Starting SmokeyController")

    def loadEnv(self,file):
        with open(file) as envFile:
            envFile.seek(0)
            self.env=json.load(envFile)           
    def connectWifi(self,maxWifiTries):
        if not self.nic.active():
            self.nic.active(True)
        if not self.nic.isconnected():
            for i in range(0,maxWifiTries):
                print("try {n} to connect to wifi {wifiname}".format(n=i,wifiname=self.env['WIFINAME']))
                self.nic.connect(self.env['WIFINAME'],self.env['WIFIPW'])
                time.sleep(1)
                if self.nic.isconnected():
                    print("Connected to {wifiname} with ip {ip}".format(wifiname=self.env['WIFINAME'],ip=self.nic.ifconfig()[0]))
                    return True
        print("Connection to {wifiname} failed".format(wifiname=self.env['WIFINAME']))
        return False

    def connectMQTT(self,maxMQTTTries):
        self.mqtt = MQTTClient(self.env['MQTTCLIENTNAME'], self.env['MQTTSERVER'])
        for i in range(0,maxMQTTTries):
            try:
                print("try {n} to connect to MQTTServer {host}".format(n=i,host=self.env['MQTTSERVER']))
                self.mqtt.connect()
                return True
            except OSError as e:
                print("Try {n}:MQTTServer {host} not reached: {e}".format(n=i,host=self.env['MQTTSERVER'],e=e))
        print("Connection to MQTT Server{host} failed".format(host=self.env['MQTTSERVER']))
        return False




class TempSensor():
    def __init__(self,name,cs=0,en=0):
        self.name = name
        self.cs = cs
        self.en = en
        self.internal = 0
        self.external = 0
        self.error = None
    def getTemperature(self):
        if not self.error:
            return self.external
        return 0

class Servo():
    def __init__(self,name,cs=0,en=0,minAngle=0,maxAngle=90,minValue=0,maxValue=100):
        self.name = name
        self.cs = cs
        self.en = en
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.minValue = minValue
        self.maxValue = maxValue
