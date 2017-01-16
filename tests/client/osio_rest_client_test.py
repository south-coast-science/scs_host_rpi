#!/usr/bin/env python3

"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.osio.client.rest_client import RESTClient

from scs_host.client.http_client import HTTPClient


# --------------------------------------------------------------------------------------------------------------------

api_key = "43308b72-ad41-4555-b075-b4245c1971db"
path = "/v1/orgs/south-coast-science-dev/topics"

http_client = HTTPClient()


# --------------------------------------------------------------------------------------------------------------------

rest_client = RESTClient(http_client, api_key)
rest_client.connect()
print(rest_client)


data = rest_client.get(path)
print(data)
