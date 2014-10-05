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

    def setShootMode(self, shootmode):
        raise NotImplemented

    def getShootMode(self):
        raise NotImplemented

    def getSupportedShootMode(self):
        raise NotImplemented

    def getAvailableShootMode(self):
        raise NotImplemented

    def actTakePicture(self):
        raise NotImplemented

    def awaitTakePicture(self):
        raise NotImplemented

    def startContShooting(self):
        raise NotImplemented

    def stopContShooting(self):
        raise NotImplemented

    def startMovieRec(self):
        raise NotImplemented

    def stopMovieRec(self):
        raise NotImplemented

    def startAudioRec(self):
        raise NotImplemented

    def stopAudioRec(self):
        raise NotImplemented

    def startIntervalStillRec(self):
        raise NotImplemented

    def stopIntervalStillRec(self):
        raise NotImplemented

    def startLiveview(self):
        raise NotImplemented

    def stopLiveview(self):
        raise NotImplemented

    def startLiveviewWithSize(self):
        raise NotImplemented

    def getLiveviewSize(self):
        raise NotImplemented

    def getSupportedLiveviewSize(self):
        raise NotImplemented

    def getAvailableLiveviewSize(self):
        raise NotImplemented

    def setLiveviewFrameInfo(self):
        raise NotImplemented

    def getLiveviewFrameInfo(self):
        raise NotImplemented

    def actZoom(self):
        raise NotImplemented

    def setZoomSetting(self):
        raise NotImplemented

    def getZoomSetting(self):
        raise NotImplemented

    def getSupportedZoomSetting(self):
        raise NotImplemented

    def getAvailableZoomSetting(self):
        raise NotImplemented

    def actHalfPressShutter(self):
        raise NotImplemented

    def cancelHalfPressShutter(self):
        raise NotImplemented

    def setTouchAFPosition(self):
        raise NotImplemented

    def getTouchAFPosition(self):
        raise NotImplemented

    def cancelTouchAFPosition(self):
        raise NotImplemented

    def actTrackingFocus(self):
        raise NotImplemented

    def cancelTrackingFocus(self):
        raise NotImplemented

    def setTrackingFocus(self):
        raise NotImplemented

    def getTrackingFocus(self):
        raise NotImplemented

    def getSupportedTrackingFocus(self):
        raise NotImplemented

    def getAvailableTrackingFocus(self):
        raise NotImplemented

    def setContShootingMode(self):
        raise NotImplemented

    def getContShootingMode(self):
        raise NotImplemented

    def getSupportedContShootingMode(self):
        raise NotImplemented

    def getAvailableContShootingMode(self):
        raise NotImplemented

    def setContShootingSpeed(self):
        raise NotImplemented

    def getContShootingSpeed(self):
        raise NotImplemented

    def getSupportedContShootingSpeed(self):
        raise NotImplemented

    def getAvailableContShootingSpeed(self):
        raise NotImplemented

    def setSelfTimer(self):
        raise NotImplemented

    def getSelfTimer(self):
        raise NotImplemented

    def getSupportedSelfTimer(self):
        raise NotImplemented

    def getAvailableSelfTimer(self):
        raise NotImplemented

    def setExposureMode(self):
        raise NotImplemented

    def getExposureMode(self):
        raise NotImplemented

    def getSupportedExposureMode(self):
        raise NotImplemented

    def getAvailableExposureMode(self):
        raise NotImplemented

    def setFocusMode(self):
        raise NotImplemented

    def getFocusMode(self):
        raise NotImplemented

    def getSupportedFocusMode(self):
        raise NotImplemented

    def getAvailableFocusMode(self):
        raise NotImplemented

    def getExposureCompensation(self):
        raise NotImplemented

    def setExposureCompensation(self):
        raise NotImplemented

    def getSupportedExposureCompensation(self):
        raise NotImplemented

    def getAvailableExposureCompensation(self):
        raise NotImplemented

    def setFNumber(self):
        raise NotImplemented

    def getFNumber(self):
        raise NotImplemented

    def getSupportedFNumber(self):
        raise NotImplemented

    def getAvailableFNumber(self):
        raise NotImplemented

    def setShutterSpeed(self):
        raise NotImplemented

    def getShutterSpeed(self):
        raise NotImplemented

    def getSupportedShutterSpeed(self):
        raise NotImplemented

    def getAvailableShutterSpeed(self):
        raise NotImplemented

    def setIsoSpeedRate(self):
        raise NotImplemented

    def getIsoSpeedRate(self):
        raise NotImplemented

    def getSupportedIsoSpeedRate(self):
        raise NotImplemented

    def getAvailableIsoSpeedRate(self):
        raise NotImplemented

    def setWhiteBalance(self):
        raise NotImplemented

    def getWhiteBalance(self):
        raise NotImplemented

    def getSupportedWhiteBalance(self):
        raise NotImplemented

    def getAvailableWhiteBalance(self):
        raise NotImplemented

    def setProgramShift(self):
        raise NotImplemented

    def getSupportedProgramShift(self):
        raise NotImplemented

    def setFlashMode(self):
        raise NotImplemented

    def getFlashMode(self):
        raise NotImplemented

    def getSupportedFlashMode(self):
        raise NotImplemented

    def getAvailableFlashMode(self):
        raise NotImplemented

    def setStillSize(self):
        raise NotImplemented

    def getStillSize(self):
        raise NotImplemented

    def getSupportedStillSize(self):
        raise NotImplemented

    def getAvailableStillSize(self):
        raise NotImplemented

    def setStillQuality(self):
        raise NotImplemented

    def getStillQuality(self):
        raise NotImplemented

    def getSupportedStillQuality(self):
        raise NotImplemented

    def getAvailableStillQuality(self):
        raise NotImplemented

    def setPostviewImageSize(self):
        raise NotImplemented

    def getPostviewImageSize(self):
        raise NotImplemented

    def getSupportedPostviewImageSize(self):
        raise NotImplemented

    def getAvailablePostviewImageSize(self):
        raise NotImplemented

    def setMovieFileFormat(self):
        raise NotImplemented

    def getMovieFileFormat(self):
        raise NotImplemented

    def getSupportedMovieFileFormat(self):
        raise NotImplemented

    def getAvailableMovieFileFormat(self):
        raise NotImplemented

    def setMovieQuality(self):
        raise NotImplemented

    def getMovieQuality(self):
        raise NotImplemented

    def getSupportedMovieQuality(self):
        raise NotImplemented

    def getAvailableMovieQuality(self):
        raise NotImplemented

    def setSteadyMode(self):
        raise NotImplemented

    def getSteadyMode(self):
        raise NotImplemented

    def getSupportedSteadyMode(self):
        raise NotImplemented

    def getAvailableSteadyMode(self):
        raise NotImplemented

    ## Continue on page 145
    
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
    # FIXME: Need to figure out which interface is the right one if
    # there are more than one. This is wrong.
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
