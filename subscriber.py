import network, utime, machine
from machine import Pin
from time import sleep
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

led = Pin(2, Pin.OUT)
# Functions mqtt
def sub_cb(topic, msg):
    print((topic, msg))
    print(msg.decode())
    if msg.decode()=="true":
        led.value(1)    
    else:
        if msg.decode()=="false":
            led.value(0)
def reset():
    print("Resetting...")
    sleep(5)
    machine.reset()

# main.py
from umqtt.simple import MQTTClient


### --- same as before ---
CLIENT_NAME = 'node'
BROKER_ADDR = '192.168.137.1'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.set_callback(sub_cb)
mqttc.connect()

### ----------------------

# Subscriber topic setup
CLICK_TOPIC = CLIENT_NAME.encode() + b'/btn/0'
mqttc.subscribe(CLICK_TOPIC)

while True:
    try:
        mqttc.check_msg()
        
    except OSError as e:
        print(e)
        reset()
    sleep(0.05)
    #print("Waiting...")
    
mqttClient.disconnect()
