from base_classes import BaseLobby, BaseGame


class Lobby(BaseLobby):
    clients = []
    game = None

    def __init__(self, game):
        self.game = game(self)
        self.name = None
        self.clients = []

        BaseLobby.__init__(self)

    def add_client(self, client):
        self.clients.append(client)
        client.lobby = self

        self.game.add_client(client)

        print "Added client to lobby %s" % (self.id, )

    def remove_client(self, client):
        self.clients.remove(client)
        client.lobby = None

        print "Removed client from lobby %s" % (self.id, )

    def start_game(self, client):
        self.game.start(client)
