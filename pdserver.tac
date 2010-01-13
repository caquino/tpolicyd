#!/usr/bin/env python
# coding: utf-8
# testing:
# twistd -ny pdserver.tac
#
# production:
# twistd --pidfile=/var/run/pdserver.pid --logfile=/var/log/pdserver.log \
#        --reactor=epoll --uid=nobody --gid=nobody --python=pdserver.tac

SERVER_PORT = 8888
IPDB_PATH = "tools/ipdb.sqlite"

import sys
import os.path
from txpd import helper
from txpd import protocol
from twisted.application import service, internet

cwd = os.path.dirname(__file__)
sys.path.append(cwd)
import rules

tools = helper.Tools(os.path.join(cwd, IPDB_PATH))
application = service.Application("TXPD")
srv = internet.TCPServer(SERVER_PORT, protocol.PDFactory(tools, rules.process))
srv.setServiceParent(application)
