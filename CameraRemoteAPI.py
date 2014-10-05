#!/usr/bin/python

import socket
import json
import requests
import xml.etree.ElementTree as ET

CRA_SSDP_MGRP = '239.255.255.250'
CRA_SSDP_PORT = 1900
CRA_SSDP_GROUP = (CRA_SSDP_MGRP, CRA_SSDP_PORT)

CRA_SSDP_MX = 5      # Request timeout, seconds
CRA_SSDP_ST = 'urn:schemas-sony-com:service:ScalarWebAPI:1'
CRA_SSDP_MSG = "\r\n".join([
    'M-SEARCH * HTTP/1.1',
    'HOST: {h}:{p}',
    'MAN: "ssdp:discover"',
    'ST: {st}',
    'MX: 3',
    '',
    ''])

ALL = ['CameraRemoteError',
       'CameraRemoteServerError',
       'CameraRemoteAPI',
       'discover']

class SSDPResponse(object):
    class _FakeSocket(StringIO.StringIO):
        def makefile(self, *args, **kw):
            return self
    def __init__(self, response):
        r = httplib.HTTPResponse(self._FakeSocket(response))
        r.begin()
        self.location = r.getheader("location")
        self.usn = r.getheader("usn")
        self.st = r.getheader("st")
        try:
            self.cache = r.getheader("cache-control").split("=")[1]
        except:
            self.cache = None
    def __repr__(self):
        return "<SSDPResponse({location}, {st}, {usn})>".format(**self.__dict__)

class CameraRemoteError(Exception):
    """ Generic exception from within CameraRemoteAPI """
    pass

class CameraRemoteAPI:
    urls = {}
    _json_headers = {'Content-Type': "application/json",}

    def __init__(self, ddxml):
        """Initialize the CameraRemoteAPI Object with a device description XML
        file. FIXME: Reconsider this approach"""
        _x = ET.fromstring(ddxml)

        ns = "urn:schemas-sony-com:av"

        for service in _x.findall('.//{%(ns)s}X_ScalarWebAPI_ServiceList/{%(ns)s}X_ScalarWebAPI_Service' % locals()):
            servicetype = service.find('{%(ns)s}X_ScalarWebAPI_ServiceType' % locals()).text
            serviceurl = service.find('{%(ns)s}X_ScalarWebAPI_ActionList_URL' % locals()).text
            self.urls[servicetype] = serviceurl + '/' + servicetype


    # Implement methods here:
    def getVersions(self):
        vals = dict(method="getVersions",
                    params=[],
                    id=1,
                    version="1.0")

        r = requests.post(self.urls['camera'], data=json.dumps(vals), headers=self._json_headers)
        return r.json()['result'][0]

def discover():
    resp = __msearch()
    _ddurl = resp.location

    _ddr = requests.get(_ddurl)
    if _ddr.status_code != 200:
        raise CameraRemoteError("Failed to get Device Description from %s" % _ddurl)

    return CameraRemoteAPI(_ddr.text)

def __msearch(st=CRA_SSDP_ST):
    """Send a M-SEARCH * HTTP/1.1 request and return the response"""
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender.setsockopt(socket.IPPROTO_IP,
                      socket.IP_MULTICAST_TTL,
                      1)
    sender.setsockopt(socket.SOL_IP,
                      socket.IP_MULTICAST_IF,
                      socket.inet_pton(socket.AF_INET,
                                       '192.168.122.173'))
    sender.setsockopt(socket.SOL_IP,
                      socket.IP_MULTICAST_LOOP,
                      1)
    sender.sendto(CRA_SSDP_MSG.format(h=CRA_SSDP_MGRP,
                                      p=CRA_SSDP_PORT,
                                      st=st),
                  CRA_SSDP_GROUP)
    responses = {}

    _msg, _from = sender.recvfrom(1024)
    r = SSDPResponse(_msg)

    if sender:
        sender.close()

    return r
