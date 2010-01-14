# coding: utf-8

import types, struct, socket
from twisted.internet import defer, reactor, protocol

class _Protocol(protocol.Protocol):
    def connectionMade(self):
        self.sendRequest(*self.factory.request)

    def sendRequest(self, saddr, daddr, sport=0, dport=25):
        query = struct.pack("IBI4s4sHH", 0x0defaced, 1, 0x12345678,
            socket.inet_aton(saddr), socket.inet_aton(daddr), sport, dport)
        self.transport.write(query)

    def dataReceived(self, data):
        result = []
        for i in struct.unpack("I I B 20s 40s b 30s 30s B B B h H i", data):
            if isinstance(i, types.StringType) and i.find("\x00") != -1:
                result.append(i[:i.find("\x00")])
            else:
                result.append(i)
        self.factory.deferred.callback(result)
        self.factory.deferred = None
        self.transport.loseConnection()

class _Factory(protocol.ClientFactory):
    protocol = _Protocol

    def __init__(self, *request):
        self.request = request
        self.deferred = defer.Deferred()

    def error(self, why):
        if self.deferred:
            self.deferred.errback(why)
            self.deferred = None

    def clientConnectionLost(self, conn, why):
        self.error(why)
        protocol.ClientFactory.clientConnectionLost(self, conn, why)

    def clientConnectionFailed(self, conn, why):
        self.error(why)
        protocol.ClientFactory.clientConnectionFailed(self, conn, why)

def makeRequest(saddr, daddr, sport, dport, filename="/var/run/p0f.sock"):
    factory = _Factory(saddr, daddr, sport, dport)
    reactor.connectUNIX(filename, factory)
    return factory.deferred
