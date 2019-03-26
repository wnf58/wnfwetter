#!/usr/bin/env python3

import paho.mqtt.client as mqtt

BONE2013 = '192.168.80.106'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("computer/esp1")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BONE2013, 1883, 60)

client.loop_forever()
