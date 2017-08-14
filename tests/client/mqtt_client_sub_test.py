#!/usr/bin/env python3

"""
Created on 11 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.osio.client.client_auth import ClientAuth

from scs_host.client.mqtt_client import MQTTClient
from scs_host.client.mqtt_client import MQTTSubscriber
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------
# handler...

def print_message(publication):
    print("publication: %s" % publication)
    sys.stdout.flush()


# --------------------------------------------------------------------------------------------------------------------
# config...

topic = "/orgs/south-coast-science-dev/development/device/alpha-pi-eng-000006/control"
print("topic: %s" % topic)

subscriber = MQTTSubscriber(topic, print_message)
print("subscriber: %s" % subscriber)
print("-")


# --------------------------------------------------------------------------------------------------------------------
# resources...

# ClientAuth...
auth = ClientAuth.load_from_host(Host)

if auth is None:
    print("ClientAuth not available.", file=sys.stderr)
    exit(1)

print("auth: %s" % auth)
print("-")


# --------------------------------------------------------------------------------------------------------------------
# run...

client = MQTTClient(subscriber)
client.connect(ClientAuth.MQTT_HOST, auth.client_id, auth.user_id, auth.client_password)
print(client)
print("-")

while True:
    time.sleep(0.1)
