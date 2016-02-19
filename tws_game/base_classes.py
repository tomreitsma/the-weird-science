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

    def set_factory(self):
        pass
