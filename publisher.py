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

### --- same as before ---
CLIENT_NAME = 'blue'
BROKER_ADDR = '192.168.137.1'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.connect()
### ----------------------

# button setup
btn = Pin(2, Pin.IN)
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/0'
btn1 = True

while True:
    btn1 = not btn1
    mqttc.publish( BTN_TOPIC, str(btn1).encode())
    sleep(0.75)
    print("Publishing...")
