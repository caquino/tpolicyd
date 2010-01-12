# coding: utf-8

from twisted.internet import defer

@defer.inlineCallbacks
def geoip_lookup(addr):
    yield 1
    defer.returnValue("BR")
