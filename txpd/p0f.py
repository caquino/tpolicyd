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
    def __init__(self):
        self.queue = defer.DeferredQueue()

    def connectionMade(self):
        self.factory.append(self)

    def connectionLost(self, why):
        self.factory.remove(self)
        protocol.Protocol.connectionLost(self, why)

    def dataReceived(self, data):
        result = []
        for i in struct.unpack("I I B 20s 40s b 30s 30s B B B h H i", data):
            if isinstance(i, types.StringType) and i.find("\x00") != -1:
                result.append(i[:i.find("\x00")])
            else:
                result.append(i)
        self.queue.put(result)

    def sendRequest(self, saddr, daddr, sport=0, dport=25):
        query = struct.pack("IBI4s4sHH", 0x0defaced, 1, 0x12345678,
            socket.inet_aton(saddr), socket.inet_aton(daddr), sport, dport)
        self.transport.write(query)
        return self.queue.get()

class _Factory(protocol.ReconnectingClientFactory):
    maxDelay = 10
    protocol = _Protocol

    def __init__(self, pool_size):
        self.idx = 0
        self.size = 0
        self.pool = []
        self.pool_size = pool_size
        self.deferred = defer.Deferred()
        self.API = _API(self)

    def append(self, conn):
        self.pool.append(conn)
        self.size += 1
        if self.deferred and self.size == self.pool_size:
            self.deferred.callback(self.API)
            self.deferred = None

    def remove(self, conn):
        try:
            self.pool.remove(conn)
        except:
            pass
        self.size = len(self.pool)

    @property
    def connection(self):
        assert self.size
        conn = self.pool[self.idx % self.size]
        self.idx += 1
        return conn

def _Connection(filename, reconnect, pool_size, lazy):
    factory = _Factory(pool_size)
    factory.continueTrying = reconnect
    endpoint = filename or "/var/run/p0f.sock"
    for x in xrange(pool_size):
        reactor.connectUNIX(endpoint, factory)
    return (lazy is True) and factory.API or factory.deferred

def p0fConnection(filename=None, reconnect=True):
    return _Connection(filename, reconnect, pool_size=1, lazy=False)

def p0fConnectionPool(filename=None, reconnect=True, pool_size=10):
    return _Connection(filename, reconnect, pool_size, lazy=False)

def lazyp0fConnection(filename=None, reconnect=True):
    return _Connection(filename, reconnect, pool_size=1, lazy=True)

def lazyp0fConnectionPool(filename=None, reconnect=True, pool_size=10):
    return _Connection(filename, reconnect, pool_size, lazy=True)
