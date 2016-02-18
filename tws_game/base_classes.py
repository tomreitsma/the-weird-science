from uuid import uuid4


class BaseLobby:
    id = uuid4()
    clients = []
    game = None

    def __init__(self):
        pass


class BaseGame:
    def __init__(self):
        pass
