from network import WLAN
from network import Sigfox
import machine
from machine import Pin
import socket
from ltr329als01 import LTR329ALS01
import time
import json

light_sensor = LTR329ALS01(integration = LTR329ALS01.ALS_INT_50, rate = LTR329ALS01.ALS_RATE_50)

transmissions = 0

def sense_light():
    return light_sensor.light()

def average(data_structure):
    return sum(value for value in data_structure) / len(data_structure)

def init_socket():
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
    s.setblocking(True)
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    return s

def init_temp():
    p_out = Pin('G6', mode=Pin.OUT)
    p_out.value(1)

    adc = machine.ADC()
    pin = adc.channel(pin='G3')
    return pin

pin = init_temp()
socket = init_socket()

while True:
    light_value = sense_light()
    avg_value = average(light_value)
    val = pin.voltage()
    temp = (val - 500) / 10
    socket.send(str(avg_value) + " " + str(temp) + " " + str(transmissions))
    print("Message sent: " + str(avg_value) + " " + str(temp) + " " + str(transmissions))
    transmissions += 1
    time.sleep(10)