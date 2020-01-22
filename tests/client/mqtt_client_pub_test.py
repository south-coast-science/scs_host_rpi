#!/usr/bin/env python3

"""
Created on 11 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


import time

from scs_core.data.publication import Publication

from scs_host.client.mqtt_client import MQTTClient


# ------------------------------------------------------------------------------------------------------------
# config...

host = "mqtt.opensensors.io"
print("host: %s" % host)

username = "southcoastscience-dev"
print("username: %s" % username)

client_id = "6067"                      # scs-rpi-009
print("client_id: %s" % client_id)

password = "kbCbu2g8"
print("password: %s" % password)

print("-")


topic = "/orgs/south-coast-science-dev/development/device/alpha-pi-eng-000006/control"
print("topic:%s" % topic)

message = "python message "
print("message:%s" % message)

print("-")


# ------------------------------------------------------------------------------------------------------------
# resources...

client = MQTTClient()
client.connect(host, client_id, username, password)

print(client)
print("-")


# --------------------------------------------------------------------------------------------------------------------
# run...

for i in range(10):
    payload = {'msg': message + str(i)}
    success = client.publish(Publication(topic, payload), 10.0)

    print("success: %s payload: %s" % (success, payload))

    time.sleep(1)

client.disconnect()
