#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("mosquitto",1883,60)
client.publish("microlab/nicla_gas_01", "Hello world!")
client.disconnect()