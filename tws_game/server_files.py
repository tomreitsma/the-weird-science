from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from tws_game.lobby import Lobby
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
        lobby = Lobby()
        lobby.add_client(client)

        client.sendMessage()

    def join_lobby(self, client, data):
        pass

    def list_lobbies(self, client, data):
        pass

    def leave_lobby(self, client, data):
        pass

    def start_game(self, client, data):
        pass

    def set_nickname(self, client, data):
        print "Setting nickname"

        pprint(data)

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
            commands[command](client, data)
