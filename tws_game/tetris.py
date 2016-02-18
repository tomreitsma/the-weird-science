from twisted.internet import reactor
from base_classes import BaseGame

import time


GAME_STATE_NOT_STARTED = 0
GAME_STATE_STARTED = 100
GAME_STATE_FINISHED = 200

GAME_STATES = (
    GAME_STATE_NOT_STARTED,
    GAME_STATE_STARTED,
    GAME_STATE_FINISHED,
)


class Tetris(BaseGame):
    max_players = 2
    GAME_STATE = None

    def __init__(self, lobby):
        BaseGame.__init__(self)

        self.lobby = lobby

        self.GAME_STATE = GAME_STATE_NOT_STARTED
        self.heartbeat()

    def heartbeat(self):
        for client in self.lobby.clients:
            self.lobby.factory.send_command(client, 'heartbeat', {'heartbeat': time.time()})

        reactor.callLater(1, self.heartbeat)

    def add_client(self, client):
        self.clients.append(client)

    def start(self, client):
        self.GAME_STATE = GAME_STATE_STARTED
        print "Game started by client %s" % client