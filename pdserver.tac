#!/usr/bin/env python
# coding: utf-8
# testing:
# twistd -ny pdserver.tac
#
# production:
# twistd --pidfile=/var/run/pdserver.pid --logfile=/var/log/pdserver.log \
#        --reactor=epoll --uid=nobody --gid=nobody --python=pdserver.tac

import os.path
cwd = os.path.dirname(__file__)

SERVER_PORT = 8888
GEOIP_CDB = os.path.join(cwd, "tools/ipdb.cdb")

import rules
from txpd import helper
from txpd import protocol
from twisted.application import service, internet

tools = helper.Tools(GEOIP_CDB)
application = service.Application("TXPD")
srv = internet.TCPServer(SERVER_PORT, protocol.PDFactory(tools, rules.process))
srv.setServiceParent(application)
