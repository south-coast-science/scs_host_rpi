"""
Created on 11 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pypi.python.org/pypi/paho-mqtt
http://www.hivemq.com/blog/mqtt-client-library-paho-python
http://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels

mosquitto_pub -h mqtt.opensensors.io -i <DeviceID> -t /users/<UserName>/<TopicName> \
-m 'This is a test message' -u <UserName> -P <Device Password>

mosquitto_pub -h mqtt.opensensors.io -i 5402 -t /users/southcoastscience-dev/test/text \
-m 'hello' -u southcoastscience-dev -P cPhbitmp
"""

import time

import paho.mqtt.client as paho


# --------------------------------------------------------------------------------------------------------------------

class MQTTClient(object):
    """
    classdocs
    """

    __PORT =        1883
    __TIMEOUT =     120

    __PUB_QOS =     1
    __SUB_QOS =     1


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, subscription=None, on_message=None):
        """
        Constructor
        """
        self.__client = None

        self.__subscription = subscription
        self.__on_message = on_message


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, host, client_id, username, password):
        # paho client...
        self.__client = paho.Client(client_id)

        # event handling...
        self.__client.on_connect = self.on_connect
        self.__client.on_message = self.on_message

        # connect...
        self.__client.username_pw_set(username, password)
        self.__client.connect(host, MQTTClient.__PORT)

        # start thread...
        self.__client.loop_start()


    def disconnect(self):
        self.__client.loop_stop()


    # ----------------------------------------------------------------------------------------------------------------

    def publish(self, topic, payload, timeout):
        msg_info = self.__client.publish(topic, str(payload), MQTTClient.__PUB_QOS)

        end_time = time.time() + timeout

        while time.time() < end_time:
            if msg_info.is_published():
                return True

            time.sleep(0.1)

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def on_connect(self, client, userdata, flags, rc):
        # print("on_connect: client: %s userdata: %s flags: %s, rc: %s" % (client, userdata, flags, rc))

        if self.__subscription:
            self.__client.subscribe(self.__subscription, qos=MQTTClient.__SUB_QOS)


    def on_message(self, client, userdata, msg):
        # print("on_message: client: %s userdata: %s msg: %s" % (client, userdata, msg.payload))

        if self.__subscription and self.__on_message:
            self.__on_message(msg.payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTClient:{subscription:%s}" % self.__subscription
