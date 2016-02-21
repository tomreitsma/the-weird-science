#!/usr/bin/env python

import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import listenWS
from tws_game.server import TwsServerFactory, ClientConnection
from settings import *

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    ServerFactory = TwsServerFactory

    factory = ServerFactory(u"ws://%s:%s" % (WEBSOCKET_HOST, WEBSOCKET_PORT, ))
    factory.protocol = ClientConnection
    listenWS(factory)

    webdir = File("public")
    web = Site(webdir)
    reactor.listenTCP(8080, web)

    reactor.run()
