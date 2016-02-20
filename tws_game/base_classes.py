from uuid import uuid4


class BaseLobby(object):
    id = None
    clients = []
    game = None
    factory = None

    def __init__(self):
        self.id = str(uuid4())

    def set_factory(self, factory):
        self.factory = factory


class BaseGame(object):
    factory = []

    commands = {

    }

    def handle_command(self, client, command, data):
        if command in self.commands:
            self.commands[command](client, data)
