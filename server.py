import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import listenWS

from tws_game.server import TwsServerFactory, TwsServerProtocol


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    ServerFactory = TwsServerFactory

    factory = ServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = TwsServerProtocol
    listenWS(factory)

    webdir = File("public")
    web = Site(webdir)
    reactor.listenTCP(8080, web)

    reactor.run()
