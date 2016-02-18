from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from tws_game.lobby import Lobby
from tws_game.tetris import Tetris

from pprint import pprint

import json


class TwsServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if not isBinary:
            self.factory.command(self, payload)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class TwsServerFactory(WebSocketServerFactory):

    AVAILABLE_GAMES = {
        'TETRIS': Tetris
    }

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []
        self.lobbies = {}

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    """ Message encode/decode functionality """

    def encode_message(self, command, data):
        return '|'.join([command, json.dumps(data)])

    def decode_message(self, message):
        command, data = message.split('|', 1)
        data = json.loads(data)

        return command, data

    """ Basic game commands """

    def create_lobby(self, client, data):

        if not data.has_key('game') and data['game'] in self.AVAILABLE_GAMES:
            raise Exception('Game unavailable')

        lobby = Lobby(self.AVAILABLE_GAMES[data['game']])
        lobby.set_factory(self)
        lobby.add_client(client)

        self.send_command(client, 'lobby_created', {
            'id': lobby.id
        })

    def join_lobby(self, client, data):
        pass

    def list_lobbies(self, client, data):
        pass

    def leave_lobby(self, client, data):
        pass

    def start_game(self, client, data):
        client.lobby.start_game(client)

    def set_nickname(self, client, data):
        print "Setting nickname"

        pprint(data)

    def send_command(self, client, command, data):
        msg = self.encode_message(command, data)

        print "Sending command "
        print msg

        client.sendMessage(
            msg
        )

    def command(self, client, msg):

        command, data = self.decode_message(msg)

        commands = {
            'create_lobby': self.create_lobby,
            'join_lobby': self.join_lobby,
            'list_lobbies': self.list_lobbies,
            'leave_lobby': self.leave_lobby,
            'start_game': self.start_game,
            'set_nickname': self.set_nickname
        }

        if command in commands:
            print "Executing command %s" % (command,)
            commands[command](client, data)
        else:
            print "Unrecognized command %s" % (command,)
