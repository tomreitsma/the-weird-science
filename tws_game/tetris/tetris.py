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

KEY_ARROW_UP = 38
KEY_ARROW_DOWN = 40
KEY_ARROW_LEFT = 37
KEY_ARROW_RIGHT = 39
KEY_SPACE = 32
KEY_RETURN = 13


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

        self.state_data = {}

        self._reset_playfield()
        self._reset_fallen_piece_data()

        self.state_data['score'] = {}

        self.commands = {
            'keypress': self.handle_keypress
        }

    def heartbeat(self):
        for client in self.lobby.clients:
            self.lobby.factory.send_command(
                client,
                'heartbeat', {
                    'heartbeat': time.time()
                }
            )

        # reactor.callLater(1, self.heartbeat)

    def handle_keypress(self, client, data):
        print "Handling keypress"

        if not self._handle_falling_piece(client):
            self._broadcast_board()
            return False

        if data['key'] == KEY_ARROW_LEFT:
            client.current_piece.offset_left -= 1
        elif data['key'] == KEY_ARROW_RIGHT:
            client.current_piece.offset_left += 1
        elif data['key'] == KEY_ARROW_UP:
            client.current_piece.rotate()
        elif data['key'] == KEY_ARROW_DOWN:
            client.current_piece.offset_top += 1

        self._update_field()
        self._broadcast_board()

    def _reset_fallen_piece_data(self):
        self.state_data['fallen_piece_data'] = []

        for y in range(self.field_size[1]):
            self.state_data['fallen_piece_data'].append([])
            for x in range(self.field_size[0]):
                self.state_data['fallen_piece_data'][y].append(0)

    def _reset_playfield(self):
        self.state_data['playfield'] = []

        for y in range(self.field_size[1]):
            self.state_data['playfield'].append([])
            for x in range(self.field_size[0]):
                self.state_data['playfield'][y].append(0)

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

                        print "New xy: %d, %d" % (new_x, new_y,)

                        self.state_data['playfield'][new_y][new_x] = 1

    def _render_board(self):
        pprint(self._get_complete_field())
        pass

    def _get_complete_field(self):
        complete = []

        for y in range(self.field_size[1]):
            complete.append([])
            for x in range(self.field_size[0]):
                if self.state_data['playfield'][y][x] == 1 or \
                        self.state_data['fallen_piece_data'][y][x] == 1:
                    complete[y].append(1)
                else:
                    complete[y].append(0)

        return complete

    def _broadcast_board(self):
        print self.lobby.id
        print self.lobby.clients
        for client in self.lobby.clients:
            self.lobby.factory.send_command(
                client,
                'update_board',
                self._get_complete_field()
            )

    def _add_falling_piece_to_fallen_pieces(self, client):
        active_coordinates = client.current_piece.get_active_coordinates()

        for ac in active_coordinates:
            self.state_data['fallen_piece_data'][ac[1]][ac[0]] = 1

        client.current_piece = self._get_random_piece()

    def _handle_falling_piece(self, client):
        active_coordinates = client.current_piece.get_active_coordinates()

        for ac in active_coordinates:
            """ Check if the piece hit the bottom boundary
            """
            if ac[1] >= self.field_size[1] - 1:
                self._add_falling_piece_to_fallen_pieces(client)
                return False

            """ Check if the piece hit an already fallen piece
            """
            if self.state_data['fallen_piece_data'][ac[1]+1][ac[0]] == 1:
                self._add_falling_piece_to_fallen_pieces(client)
                return False

        return True

    def _gameplay_tick(self):

        for client in self.lobby.clients:
            if not client.current_piece:
                client.current_piece = self._get_random_piece()

            if self._handle_falling_piece(client):
                client.current_piece.offset_top += 1

        self._update_field()
        self._render_board()
        self._broadcast_board()

        reactor.callLater(1, self._gameplay_tick)

    def start(self, client):
        self._reset_playfield()
        self.GAME_STATE = GAME_STATE_STARTED

        for client in self.lobby.clients:
            client.current_piece = None

        reactor.callLater(0, self._gameplay_tick)

        print "Game started by client %s" % client
