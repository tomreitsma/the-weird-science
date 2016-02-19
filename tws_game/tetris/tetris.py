from twisted.internet import reactor

from tws_game.base_classes import BaseGame
from pieces import *
from pprint import pprint

import time
import random


GAME_STATE_NOT_STARTED = 0
GAME_STATE_STARTED = 100
GAME_STATE_FINISHED = 200

GAME_STATES = (
    GAME_STATE_NOT_STARTED,
    GAME_STATE_STARTED,
    GAME_STATE_FINISHED,
)


class Tetris(BaseGame):

    """ Internals
    """
    GAME_STATE = None
    VALID_GAME_PIECES = (
        PieceI,
        PieceT,
    )

    state_data = {}

    """ Game config
    """
    max_players = 2
    field_size = (10, 22, )  # w/h

    def __init__(self, lobby):
        BaseGame.__init__(self)

        self.lobby = lobby

        self.GAME_STATE = GAME_STATE_NOT_STARTED
        self.heartbeat()

    def heartbeat(self):
        for client in self.lobby.clients:
            self.lobby.factory.send_command(
                client,
                'heartbeat', {
                    'heartbeat': time.time()
                }
            )

        # reactor.callLater(1, self.heartbeat)

    def _reset_playfield(self):
        self.playfield = [[0 for x in range(self.field_size[0])] for y in range(self.field_size[1])]
        pprint(self.playfield)

    def _get_random_piece(self):
        piece = random.choice(self.VALID_GAME_PIECES)
        return piece()

    """ Overwriting
    """
    def _update_field(self):

        # Resetting field for now
        self._reset_playfield()

        for client in self.lobby.clients:
            piece = client.current_piece

            for y in range(0, piece.square_size):
                for x in range(0, piece.square_size):
                    if piece.current_rotation()[y][x] == 1:
                        new_x = piece.offset_left + x
                        new_y = piece.offset_top + y
                        self.playfield[new_y][new_x] = 1

    def _render_board(self):
        pprint(self.playfield)

    def _gameplay_tick(self):

        for client in self.lobby.clients:
            if not client.current_piece:
                client.current_piece = self._get_random_piece()

            client.current_piece.offset_top += 1
            client.current_piece.rotate()

        self._update_field()
        self._render_board()

        for client in self.lobby.clients:
            self.lobby.factory.send_command(
                client,
                'update_board',
                self.playfield
            )

        reactor.callLater(1, self._gameplay_tick)

    def start(self, client):
        self._reset_playfield()
        self.GAME_STATE = GAME_STATE_STARTED

        for client in self.lobby.clients:
            client.current_piece = None

        reactor.callLater(0, self._gameplay_tick)

        print "Game started by client %s" % client
