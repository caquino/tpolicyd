# coding: utf-8

"""Postfix Policy Daemon Protocol"""

import types
from twisted.python import log
from twisted.protocols import basic
from twisted.internet import defer, protocol

class _O(dict):
    def __getattr__(self, k):
        return dict.get(self, k, None)

class PDProtocol(basic.LineReceiver):
    delimiter = "\n\n"

    def lineReceived(self, data):
        map = _O()
        lines = data.split("\n")
        for line in lines:
            try:
                k, v = line.split("=", 1)
            except:
                pass
            else:
                map[k] = v

        d = self.factory.processor(map, self.factory.tools)
        if isinstance(d, defer.Deferred):
            d.addCallbacks(self.sendResponse, self.processFailure)
        else:
            self.sendResponse(d)

    def sendResponse(self, result):
        if isinstance(result, types.StringType):
            self.sendLine("action=%s" % (result))
        else:
            self.sendLine("action=DUNNO")

    def processFailure(self, why):
        log.err(why)
        self.transport.loseConnection()

class PDFactory(protocol.ServerFactory):
    protocol = PDProtocol
    def __init__(self, tools, processor):
        self.tools = tools
        self.processor = processor
