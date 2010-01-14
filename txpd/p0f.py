# coding: utf-8

import struct, socket
from twisted.internet import task, defer, reactor, protocol

class _API(object):
    def __init__(self, factory):
        self._factory = factory
        self._connected = factory.deferred

    def __disconnected(self, *args, **kwargs):
        deferred = defer.Deferred()
        deferred.errback(RuntimeWarning("not connected"))
        return deferred

    def __getattr__(self, method):
        try:
            return getattr(self._factory.connection, method)
        except:
            return self.__disconnected

    def __connection_lost(self, deferred):
        if self._factory.size == 0:
            self.__task.stop()
            deferred.callback(True)

    def disconnect(self):
        self._factory.continueTrying = 0
        for conn in self._factory.pool:
            try:
                conn.transport.loseConnection()
            except:
                pass

        d = defer.Deferred()
        self.__task = task.LoopingCall(self.__connection_lost, d)
        self.__task.start(1)
        return d

    def __repr__(self):
        return "<p0f: %d connection(s)>" % self._factory.size

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
        self.transport.loseConnection()

class _Factory(protocol.ClientFactory):
    protocol = _Protocol

    def __init__(self, *request):
        self.request = request
        self.deferred = defer.Deferred()

    def ready(self, conn):
        conn.sendRequest(*self.request)

def makeRequest(saddr, daddr, sport, dport, filename="/var/run/p0f.sock"):
    factory = _Factory(saddr, daddr, sport, dport)
    reactor.connectUNIX(filename, factory)
    return factory.deferred
