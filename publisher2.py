import network, utime, machine

# Replace the following with your WIFI Credentials
SSID = "tsm"
SSID_PASSWORD = "123456789"


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()



# main.py
from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep
import math
### --- same as before ---
CLIENT_NAME = 'blue'
BROKER_ADDR = '192.168.137.1'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()
### ----------------------
SEN_TOPIC = CLIENT_NAME.encode() + b'/sensor/0'
# button setup
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/0'
btn = False
count = 0
t = 0
while True:
    btn = not btn
    t = t + count/100
    fx = math.sin(t)
    print(fx)
    mqttc.publish( BTN_TOPIC, str(btn).encode())
    mqttc.publish( SEN_TOPIC, str(fx).encode())
    sleep(0.5)
    print("Publishing...")
    count = count + 1
    print(count)
