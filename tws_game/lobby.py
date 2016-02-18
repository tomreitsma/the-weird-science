from base_classes import BaseLobby


class Lobby(BaseLobby):
    clients = []
    game = None

    def __init__(self, game):
        self.game = game

        BaseLobby.__init__(self)

    def add_client(self, client):
        pass
