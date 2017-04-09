#!/usr/bin/env python3

"""
Created on 11 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
mosquitto_pub -h mqtt.opensensors.io -i <DeviceID> -t /users/<UserName>/<TopicName> \
 -m 'This is a test message' -u <UserName> -P <Device Password>

mosquitto_pub -h mqtt.opensensors.io -i 5402 -t /users/southcoastscience-dev/test/text \
 -m 'hello' -u southcoastscience-dev -P cPhbitmp

"""

import time

from scs_host.client.mqtt_client import MQTTClient


# --------------------------------------------------------------------------------------------------------------------

def print_message(payload):
    print("payload: %s" % payload)


# --------------------------------------------------------------------------------------------------------------------

username = "southcoastscience-dev"
print("username:%s" % username)

client_id = "5895"                      # scs-rpi-007
print("client_id:%s" % client_id)

password = "9jNlykys"
print("password:%s" % password)

print("-")

host = "mqtt.opensensors.io"
print("host:%s" % host)

topic = "/orgs/south-coast-science-dev/development/device/alpha-pi-eng-000006/control"
print("topic:%s" % topic)

print("-")


# --------------------------------------------------------------------------------------------------------------------

client = MQTTClient(topic, print_message)
client.connect(host, client_id, username, password)
print(client)
print("-")

while True:
    time.sleep(1)
