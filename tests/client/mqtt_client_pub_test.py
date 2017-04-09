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


import sys
import time

from scs_core.data.json import JSONify
from scs_core.osio.client.client_auth import ClientAuth

from scs_host.client.mqtt_client import MQTTClient
from scs_host.sys.host import Host


# ------------------------------------------------------------------------------------------------------------
# resource...

auth = ClientAuth.load_from_host(Host)

if auth is None:
    print("ClientAuth not available.", file=sys.stderr)
    exit()

client = MQTTClient()
client.connect(ClientAuth.MQTT_HOST, auth.client_id, auth.user_id, auth.client_password)

print(client)
print("-")


# --------------------------------------------------------------------------------------------------------------------


topic = "/orgs/south-coast-science-dev/development/device/alpha-pi-eng-000006/control"
print("topic:%s" % topic)

message = "python message "
print("message:%s" % message)

print("-")


# --------------------------------------------------------------------------------------------------------------------

for i in range(10):
    payload = JSONify.dumps(message + str(i))
    success = client.publish(topic, payload, 10.0)

    print("success: %s payload: %s" % (success, payload))

    time.sleep(1)

client.disconnect()
