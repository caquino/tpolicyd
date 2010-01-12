#!/usr/bin/env python
# coding: utf-8
# testing:
# twistd -ny pdserver.tac
#
# production:
# twistd --pidfile=/var/run/pdserver.pid --logfile=/var/log/pdserver.log \
#        --reactor=epoll --uid=nobody --gid=nobody --python=pdserver.tac

SERVER_PORT = 8888

import rules
from txpd import protocol
from twisted.application import service, internet

application = service.Application("TXPD")
srv = internet.TCPServer(SERVER_PORT, protocol.PDFactory(rules.process))
srv.setServiceParent(application)
