"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/33770129/how-do-i-disable-the-ssl-check-in-python-3-x
"""

import ssl

import http.client

import urllib.parse

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.http_status import HTTPStatus


# --------------------------------------------------------------------------------------------------------------------

class HTTPClient(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__conn = None
        self.__host = None


    def connect(self, host, secure=True, verified=True, timeout=None):
        if secure:
            # print("verified: %s" % verified)

            if verified:
                context = None
            else:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE

            # print("context: %s" % context)

            if timeout:
                self.__conn = http.client.HTTPSConnection(host, context=context, timeout=timeout)
            else:
                self.__conn = http.client.HTTPSConnection(host, context=context)

        else:
            if timeout:
                self.__conn = http.client.HTTPConnection(host, timeout=timeout)
            else:
                self.__conn = http.client.HTTPConnection(host)

        self.__host = host


    def close(self):
        if self.__conn:
            self.__conn.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, path, payload, headers):
        # data...
        params = None if payload is None else urllib.parse.urlencode(payload)
        query = path if params is None else path + '?' + params

        # request...
        self.__conn.request("GET", query, None, headers)

        # response...
        response = self.__conn.getresponse()
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK:
            raise HTTPException.construct(response, data)

        return data.decode()


    def post(self, path, payload, headers):
        # request...
        self.__conn.request("POST", path, payload, headers)

        # response...
        response = self.__conn.getresponse()
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK and response.status != HTTPStatus.CREATED:
            raise HTTPException.construct(response, data)

        return data.decode()


    def put(self, path, payload, headers):
        # request...
        self.__conn.request("PUT", path, payload, headers)

        # response...
        response = self.__conn.getresponse()
        data = response.read()

        # error...
        if response.status != HTTPStatus.OK and response.status != HTTPStatus.NO_CONTENT:
            raise HTTPException.construct(response, data)

        return data.decode()


    def delete(self, path, headers):
        # request...
        self.__conn.request("DELETE", path, "", headers)

        # response...
        response = self.__conn.getresponse()
        data = response.read()

        # error...

        if response.status != HTTPStatus.OK and response.status != HTTPStatus.NO_CONTENT:
            raise HTTPException.construct(response, data)

        return data.decode()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HTTPClient:{host:%s}" % self.__host
