import network, utime, machine
from machine import Pin
from time import sleep
import time

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

# Definir entradas y salidas
led = Pin(2, Pin.OUT)
btn = Pin(3, Pin.IN)

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
BROKER_ADDR = '192.168.1.241'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
mqttc.set_callback(sub_cb)
mqttc.connect()

### ----------------------
# Publisher topic node
BTN_TOPIC = CLIENT_NAME.encode() + b'/btn/1'
# Subscriber topic node
CLICK_TOPIC = CLIENT_NAME.encode() + b'/btn/0'   #node/btn/0
mqttc.subscribe(CLICK_TOPIC)

# Definir variables para el tiempo
last_time = 0
presente_time = 0
delay = 1000
while True:
    try:
        mqttc.check_msg()
        present_time = time.ticks_ms()
        #print(present_time)
        if present_time - last_time > delay:
            btnVar  = btn.value()  
            mqttc.publish( BTN_TOPIC, str(btnVar).encode())
            print("publishing...")
            last_time = present_time
    except OSError as e:
        print(e)
        reset()
    sleep(0.05)
    #print("Waiting...")
    
mqttClient.disconnect()
